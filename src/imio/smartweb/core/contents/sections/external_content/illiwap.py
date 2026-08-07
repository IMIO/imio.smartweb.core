# -*- coding: utf-8 -*-

from datetime import date
from datetime import datetime
from datetime import timedelta
from email.utils import parsedate_to_datetime
from html import unescape
from lxml import html as lxml_html
from plone.memoize import ram
from pytz import timezone
from time import time
from unicodedata import combining
from unicodedata import normalize
from urllib.parse import urlparse
from xml.etree import ElementTree

import logging
import re
import requests

logger = logging.getLogger("imio.smartweb.core")

# Illiwap news feeds and agendas all live on this single host
ILLIWAP_NETLOC = "station.illiwap.com"
# Illiwap serves its feeds with "cache-control: max-age=3600" and publishes
# about one news item every two days : one hour is its own recommendation.
CACHE_TTL = 3600
REQUEST_TIMEOUT = 5
SUMMARY_MAX_LENGTH = 200
USER_AGENT = "imio.smartweb.core (+https://www.imio.be)"
# how far ahead the agenda is read : its json route requires a date window
AGENDA_DAYS_AHEAD = 365
# the event_date macro formats calendar days, they must be the local ones
BRUSSELS_TZ = timezone("Europe/Brussels")
# safety bound when walking the paginated public agenda listing
AGENDA_LISTING_MAX_PAGES = 10
# a card on the public agenda listing : its slug and its title
EVENT_CARD = re.compile(
    r'href="[^"]*/evenements/([a-z0-9-]+)"\s*>\s*<h3[^>]*>\s*(.*?)\s*</h3>',
    re.DOTALL,
)


def is_illiwap_url(url):
    return bool(url) and urlparse(url).netloc == ILLIWAP_NETLOC


def is_illiwap_rss_url(url):
    """News come from the rss feed advertised in the station page head"""
    return is_illiwap_url(url) and urlparse(url).path.startswith("/rss/")


def is_illiwap_agenda_url(url):
    """The agenda has no rss feed : it is the json route that illiwap's own
    fullcalendar widget reads. Accept the public agenda page too, since that
    is the url an editor actually has in the browser.
    """
    if not is_illiwap_url(url):
        return False
    path = urlparse(url).path
    return "/agenda/list" in path or "/evenements" in path


def _station_url(url):
    """Strip whichever agenda path was given, keeping the station base url"""
    parts = urlparse(url)
    path = parts.path.split("/evenements")[0].split("/agenda/list")[0]
    return f"{parts.scheme}://{parts.netloc}{path.rstrip('/')}"


def agenda_page_url(url):
    return f"{_station_url(url)}/evenements/"


def _summary_and_image(description):
    """Illiwap items carry no media metadata (no media:content, no enclosure)
    and no short summary : both the thumbnail and the excerpt have to be dug
    out of the html description, which holds the whole article.
    """
    if not description or not description.strip():
        return "", None
    doc = lxml_html.fromstring(description)
    images = doc.xpath("//img/@src")
    summary = " ".join(doc.text_content().split())
    if len(summary) > SUMMARY_MAX_LENGTH:
        summary = f"{summary[:SUMMARY_MAX_LENGTH].rstrip()}…"
    return summary, images[0] if images else None


def _effective(item):
    """RSS pubDate is RFC 822, templates expect the iso format used by the
    other sections.
    """
    pub_date = item.findtext("pubDate")
    if not pub_date:
        return ""
    try:
        return parsedate_to_datetime(pub_date).strftime("%Y-%m-%dT%H:%M:%S%z")
    except (IndexError, TypeError, ValueError):
        return ""


def _cache_key(method, url):
    return f"{url}-{time() // CACHE_TTL}"


@ram.cache(_cache_key)
def _fetch_news(url):
    """Read the whole feed. Failures are left to raise : nothing is memoized
    when an exception propagates, so a transient Illiwap outage is not cached
    for a whole hour.
    """
    response = requests.get(
        url, headers={"User-Agent": USER_AGENT}, timeout=REQUEST_TIMEOUT
    )
    response.raise_for_status()
    root = ElementTree.fromstring(response.content)
    news = []
    for item in root.findall("./channel/item"):
        summary, image = _summary_and_image(item.findtext("description"))
        news.append(
            {
                "title": (item.findtext("title") or "").strip(),
                "url": (item.findtext("link") or "").strip(),
                "description": summary,
                "effective": _effective(item),
                "has_image": image is not None,
                "image": image or "",
                # Illiwap news are read on Illiwap, not on the Smartweb site
                "open_in_new_tab": True,
                "container_id": "",
                "smartweb_type": "IlliwapNews",
            }
        )
    return news


def get_news(url, limit):
    """Return at most `limit` cached feed items, or None if the feed could not
    be read.
    """
    try:
        return _fetch_news(url)[:limit]
    except Exception as e:
        logger.warning(f"Could not read Illiwap news feed {url} : {e}")
        return None


def _local_datetime(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value).astimezone(BRUSSELS_TZ)
    except ValueError:
        return None


def _agenda_cache_key(method, endpoint, start, end):
    return f"{endpoint}-{start}-{end}-{time() // CACHE_TTL}"


@ram.cache(_agenda_cache_key)
def _fetch_events(endpoint, start, end):
    """Same contract as _fetch_news : failures raise so they are not cached"""
    response = requests.get(
        endpoint,
        params={"start": start, "end": end},
        headers={"User-Agent": USER_AGENT},
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    events = []
    for event in response.json():
        begin = _local_datetime(event.get("start"))
        if begin is None:
            # the event_date macro formats the start date, it cannot be None
            continue
        props = event.get("extendedProps") or {}
        medias = props.get("medias") or []
        image = medias[0].get("url_vignette") if medias else None
        events.append(
            {
                "title": (event.get("title") or "").strip(),
                "description": (props.get("description") or "").strip(),
                "category": props.get("categorieLibelle") or "",
                "event_date": {
                    "start": begin,
                    "end": _local_datetime(event.get("end")),
                },
                # filled in by _link_to_illiwap. Stays None when no matching
                # card was found, so that tal omits the href instead of
                # rendering href="" which would reload the page.
                "url": None,
                "open_in_new_tab": False,
                "has_image": image is not None,
                "image": image or "",
                "container_id": "",
                "smartweb_type": "IlliwapEvent",
            }
        )
    # the json route does not return events in chronological order
    events.sort(key=lambda event: event["event_date"]["start"])
    return events


def _normalised_title(title):
    """Join key between the json route and the public listing. Both sides go
    through this, so its exact rules do not matter, only its stability.
    """
    title = unescape(title or "").lower()
    title = "".join(c for c in normalize("NFD", title) if not combining(c))
    return re.sub(r"[^a-z0-9]+", "-", title).strip("-")


def _slugs_cache_key(method, page_url):
    return f"{page_url}-slugs-{time() // CACHE_TTL}"


@ram.cache(_slugs_cache_key)
def _fetch_event_slugs(page_url):
    """Index the real event slugs by normalised title.

    The json route carries no slug, and an event's uuid is not a public url :
    the only place the slugs exist is the public listing. Deriving them from
    the title does not work, illiwap suffixes duplicates ("-1", "-2") and
    turns apostrophes into dashes. Document order is kept so that homonyms
    can be told apart by position, both sources being chronological.
    """
    slugs = {}
    seen = set()
    for page in range(1, AGENDA_LISTING_MAX_PAGES + 1):
        response = requests.get(
            page_url,
            params={"page": page} if page > 1 else None,
            headers={"User-Agent": USER_AGENT},
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        body = response.text
        for slug, title in EVENT_CARD.findall(body):
            if slug in seen:
                continue
            seen.add(slug)
            slugs.setdefault(_normalised_title(title), []).append(slug)
        if f"?page={page + 1}" not in body:
            break
    return slugs


def _link_to_illiwap(events, page_url):
    """Give each event the url of its page on illiwap, in place.

    Best effort : if the listing cannot be read, or an event has no matching
    card, the event simply stays unlinked rather than pointing at a wrong or
    missing page.
    """
    try:
        slugs = _fetch_event_slugs(page_url)
    except Exception as e:
        logger.warning(f"Could not read Illiwap agenda listing {page_url} : {e}")
        return
    used = {}
    for event in events:
        key = _normalised_title(event["title"])
        index = used.get(key, 0)
        candidates = slugs.get(key, [])
        if index >= len(candidates):
            continue
        used[key] = index + 1
        event["url"] = f"{page_url}{candidates[index]}"
        event["open_in_new_tab"] = True


def get_events(url, limit):
    """Return at most `limit` upcoming cached events, or None if the agenda
    could not be read.
    """
    station = _station_url(url)
    today = date.today()
    end = today + timedelta(days=AGENDA_DAYS_AHEAD)
    try:
        events = _fetch_events(
            f"{station}/agenda/list", today.isoformat(), end.isoformat()
        )
    except Exception as e:
        logger.warning(f"Could not read Illiwap agenda {station} : {e}")
        return None
    # copy before linking : the cached list must stay untouched
    events = [dict(event) for event in events[:limit]]
    _link_to_illiwap(events, f"{station}/evenements/")
    return events
