# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.external_content import illiwap
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from datetime import date
from datetime import timedelta
from imio.smartweb.core.tests.utils import clear_ram_cache
from imio.smartweb.core.tests.utils import get_html
from imio.smartweb.core.tests.utils import get_json
from xml.etree import ElementTree

import requests_mock

ILLIWAP_FEED_URL = "https://station.illiwap.com/rss/commune-de-test"
ILLIWAP_AGENDA_URL = "https://station.illiwap.com/fr/public/commune-de-test/agenda/list"
ILLIWAP_AGENDA_PAGE_URL = (
    "https://station.illiwap.com/fr/public/commune-de-test/evenements/"
)


class TestIlliwap(ImioSmartwebTestCase):
    """Tests for the illiwap module"""

    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        # these are ram cached on a time bucket : without this, what another
        # test method read is still cached here
        clear_ram_cache(
            illiwap._fetch_news, illiwap._fetch_events, illiwap._fetch_event_slugs
        )
        self.feed = get_html("resources/illiwap_rss_mock.xml").encode("utf-8")
        self.agenda = get_json("resources/json_illiwap_agenda_mock.json")
        self.listing = get_html("resources/illiwap_agenda_listing_mock.html")

    def test_is_illiwap_url(self):
        self.assertTrue(illiwap.is_illiwap_url(ILLIWAP_FEED_URL))
        self.assertTrue(
            illiwap.is_illiwap_url(
                "https://station.illiwap.com/fr/public/commune-de-test/actu"
            )
        )
        self.assertFalse(illiwap.is_illiwap_url("https://www.odwb.be/api/records"))
        # a look alike host is not illiwap
        self.assertFalse(illiwap.is_illiwap_url("https://illiwap.com/rss/x"))
        self.assertFalse(illiwap.is_illiwap_url(""))
        self.assertFalse(illiwap.is_illiwap_url(None))

    def test_summary_and_image(self):
        # an empty description is not an error
        self.assertEqual(illiwap._summary_and_image(None), ("", None))
        self.assertEqual(illiwap._summary_and_image(""), ("", None))
        self.assertEqual(illiwap._summary_and_image("   "), ("", None))

        # tags are stripped and whitespace collapsed
        summary, image = illiwap._summary_and_image(
            "<p>Hello   <strong>world</strong>\n!</p>"
        )
        self.assertEqual(summary, "Hello world !")
        self.assertIsNone(image)

        # the thumbnail is the first image of the description
        summary, image = illiwap._summary_and_image(
            '<p>Texte</p><p><img src="https://station.illiwap.com/a.jpg"/>'
            '<img src="https://station.illiwap.com/b.jpg"/></p>'
        )
        self.assertEqual(summary, "Texte")
        self.assertEqual(image, "https://station.illiwap.com/a.jpg")

    def test_summary_and_image_truncates_long_text(self):
        short = "Une actu courte."
        self.assertEqual(illiwap._summary_and_image(f"<p>{short}</p>")[0], short)

        summary = illiwap._summary_and_image(f"<p>{'mot ' * 200}</p>")[0]
        self.assertTrue(summary.endswith("…"))
        self.assertLessEqual(len(summary), illiwap.SUMMARY_MAX_LENGTH + 1)

    def test_effective(self):
        item = ElementTree.fromstring(
            "<item><pubDate>Wed, 05 Aug 2026 08:59:39 +0200</pubDate></item>"
        )
        self.assertEqual(illiwap._effective(item), "2026-08-05T08:59:39+0200")
        # a missing or unreadable pubDate does not break the item
        self.assertEqual(illiwap._effective(ElementTree.fromstring("<item/>")), "")
        self.assertEqual(
            illiwap._effective(
                ElementTree.fromstring("<item><pubDate>kamoulox</pubDate></item>")
            ),
            "",
        )

    @requests_mock.Mocker()
    def test_get_news(self, m):
        m.get(ILLIWAP_FEED_URL, content=self.feed)
        news = illiwap.get_news(ILLIWAP_FEED_URL, 10)
        self.assertEqual(len(news), 4)

        first = news[0]
        self.assertEqual(first["title"], "Un coup de pouce pour réussir son permis")
        self.assertEqual(
            first["url"],
            "https://station.illiwap.com/fr/public/commune-de-test/actu/un-coup-de-pouce",
        )
        self.assertEqual(first["effective"], "2026-08-05T08:59:39+0200")
        self.assertTrue(first["has_image"])
        self.assertEqual(
            first["image"],
            "https://station.illiwap.com/media/cache/resolve/vignette_alerte_media"
            "/uploads/alertes/documents/photo.jpg",
        )
        self.assertIn("Tu as entre 17 et 25 ans", first["description"])
        # illiwap news are read on illiwap
        self.assertTrue(first["open_in_new_tab"])

        # an item whose description holds nothing but an image has no excerpt
        self.assertEqual(news[1]["description"], "")
        self.assertTrue(news[1]["has_image"])

        # an item with no image at all
        self.assertFalse(news[2]["has_image"])
        self.assertEqual(news[2]["image"], "")

        # an unreadable pubDate does not drop the item
        self.assertEqual(news[3]["title"], "Actu sans date")
        self.assertEqual(news[3]["effective"], "")

    @requests_mock.Mocker()
    def test_get_news_limit(self, m):
        m.get(ILLIWAP_FEED_URL, content=self.feed)
        self.assertEqual(len(illiwap.get_news(ILLIWAP_FEED_URL, 2)), 2)

    @requests_mock.Mocker()
    def test_get_news_on_http_error(self, m):
        m.get(ILLIWAP_FEED_URL, status_code=500)
        self.assertIsNone(illiwap.get_news(ILLIWAP_FEED_URL, 10))

    @requests_mock.Mocker()
    def test_get_news_on_invalid_xml(self, m):
        m.get(ILLIWAP_FEED_URL, text="<rss><channel><item></rss>")
        self.assertIsNone(illiwap.get_news(ILLIWAP_FEED_URL, 10))

    @requests_mock.Mocker()
    def test_successful_read_is_cached(self, m):
        m.get(ILLIWAP_FEED_URL, content=self.feed)
        illiwap.get_news(ILLIWAP_FEED_URL, 10)
        self.assertEqual(m.call_count, 1)
        illiwap.get_news(ILLIWAP_FEED_URL, 10)
        self.assertEqual(m.call_count, 1)

    @requests_mock.Mocker()
    def test_failed_read_is_not_cached(self, m):
        """A transient outage must not be memoized for the whole cache ttl"""
        m.get(ILLIWAP_FEED_URL, status_code=503)
        self.assertIsNone(illiwap.get_news(ILLIWAP_FEED_URL, 10))
        m.get(ILLIWAP_FEED_URL, content=self.feed)
        self.assertEqual(len(illiwap.get_news(ILLIWAP_FEED_URL, 10)), 4)

    def test_is_illiwap_rss_url(self):
        self.assertTrue(illiwap.is_illiwap_rss_url(ILLIWAP_FEED_URL))
        self.assertFalse(illiwap.is_illiwap_rss_url(ILLIWAP_AGENDA_URL))
        self.assertFalse(illiwap.is_illiwap_rss_url(ILLIWAP_AGENDA_PAGE_URL))
        self.assertFalse(illiwap.is_illiwap_rss_url("https://www.odwb.be/rss/x"))
        self.assertFalse(illiwap.is_illiwap_rss_url(None))

    def test_is_illiwap_agenda_url(self):
        # both the json route and the public agenda page are accepted
        self.assertTrue(illiwap.is_illiwap_agenda_url(ILLIWAP_AGENDA_URL))
        self.assertTrue(illiwap.is_illiwap_agenda_url(ILLIWAP_AGENDA_PAGE_URL))
        self.assertFalse(illiwap.is_illiwap_agenda_url(ILLIWAP_FEED_URL))
        self.assertFalse(
            illiwap.is_illiwap_agenda_url("https://www.odwb.be/x/evenements")
        )
        self.assertFalse(illiwap.is_illiwap_agenda_url(None))

    def test_agenda_page_url(self):
        # whichever agenda url was given, the see all link is the public page
        for url in (ILLIWAP_AGENDA_URL, ILLIWAP_AGENDA_PAGE_URL):
            self.assertEqual(illiwap.agenda_page_url(url), ILLIWAP_AGENDA_PAGE_URL)

    @requests_mock.Mocker()
    def test_get_events(self, m):
        m.get(ILLIWAP_AGENDA_URL, json=self.agenda)
        events = illiwap.get_events(ILLIWAP_AGENDA_PAGE_URL, 10)

        # the event with no start is dropped : the macro cannot format it
        self.assertEqual(len(events), 3)
        self.assertNotIn("Evenement sans date", [e["title"] for e in events])

        # the json route does not sort, we do
        self.assertEqual(
            [e["title"] for e in events],
            ["Enigm'Ha", "Guinguette de Fairon", "Marathon de l'Ourthe 2026"],
        )

        first = events[0]
        self.assertEqual(first["category"], "Animation")
        self.assertEqual(
            first["description"], "Un jeu de piste dans les rues du village."
        )
        # dates are real datetimes in local time, as the macro needs
        self.assertEqual(
            first["event_date"]["start"].strftime("%d/%m/%Y"), "05/07/2026"
        )
        self.assertEqual(first["event_date"]["end"].strftime("%d/%m/%Y"), "23/08/2026")
        # the small media is used as thumbnail
        self.assertTrue(first["has_image"])
        self.assertIn("vignette_agenda_media_sm", first["image"])
        # the listing was not mocked here, so no slug could be resolved and
        # None keeps tal from rendering an href="" that would reload the page
        self.assertIsNone(first["url"])
        self.assertFalse(first["open_in_new_tab"])

        # an event without media, and with a null description
        without_media = events[1]
        self.assertFalse(without_media["has_image"])
        self.assertEqual(without_media["image"], "")
        self.assertEqual(without_media["description"], "")

    @requests_mock.Mocker()
    def test_get_events_asks_for_a_date_window(self, m):
        """The json route answers 400 without start and end"""
        m.get(ILLIWAP_AGENDA_URL, json=self.agenda)
        m.get(ILLIWAP_AGENDA_PAGE_URL, text=self.listing)
        illiwap.get_events(ILLIWAP_AGENDA_PAGE_URL, 10)
        # the listing is requested too, pick the json route request
        json_request = [r for r in m.request_history if "/agenda/list" in r.path][0]
        query = json_request.qs
        today = date.today()
        self.assertEqual(query["start"], [today.isoformat()])
        self.assertEqual(
            query["end"],
            [(today + timedelta(days=illiwap.AGENDA_DAYS_AHEAD)).isoformat()],
        )

    @requests_mock.Mocker()
    def test_get_events_limit(self, m):
        m.get(ILLIWAP_AGENDA_URL, json=self.agenda)
        self.assertEqual(len(illiwap.get_events(ILLIWAP_AGENDA_URL, 2)), 2)

    @requests_mock.Mocker()
    def test_get_events_on_http_error(self, m):
        m.get(ILLIWAP_AGENDA_URL, status_code=400)
        self.assertIsNone(illiwap.get_events(ILLIWAP_AGENDA_URL, 10))

    def test_normalised_title(self):
        # the join key survives case, accents, entities and punctuation
        self.assertEqual(
            illiwap._normalised_title("Marathon de l'Ourthe 2026"),
            illiwap._normalised_title("marathon de l&#039;ourthe 2026"),
        )
        self.assertEqual(
            illiwap._normalised_title("Les Marchés de l'Eté - Hamoir"),
            "les-marches-de-l-ete-hamoir",
        )
        self.assertEqual(illiwap._normalised_title(None), "")

    @requests_mock.Mocker()
    def test_fetch_event_slugs(self, m):
        m.get(ILLIWAP_AGENDA_PAGE_URL, text=self.listing)
        slugs = illiwap._fetch_event_slugs(ILLIWAP_AGENDA_PAGE_URL)
        # illiwap suffixes duplicates and turns apostrophes into dashes, so
        # these cannot be derived from the title
        self.assertEqual(slugs["enigm-ha"], ["enigm-ha-1"])
        self.assertEqual(slugs["guinguette-de-fairon"], ["guinguette-de-fairon-1"])
        self.assertEqual(
            slugs["marathon-de-l-ourthe-2026"], ["marathon-de-l-ourthe-2026"]
        )

    @requests_mock.Mocker()
    def test_get_events_links_to_illiwap(self, m):
        m.get(ILLIWAP_AGENDA_URL, json=self.agenda)
        m.get(ILLIWAP_AGENDA_PAGE_URL, text=self.listing)
        events = illiwap.get_events(ILLIWAP_AGENDA_PAGE_URL, 10)

        self.assertEqual(
            [event["url"] for event in events],
            [
                f"{ILLIWAP_AGENDA_PAGE_URL}enigm-ha-1",
                f"{ILLIWAP_AGENDA_PAGE_URL}guinguette-de-fairon-1",
                f"{ILLIWAP_AGENDA_PAGE_URL}marathon-de-l-ourthe-2026",
            ],
        )
        # illiwap is an external site
        self.assertTrue(all(event["open_in_new_tab"] for event in events))

    @requests_mock.Mocker()
    def test_get_events_homonyms_are_told_apart_by_position(self, m):
        """Both sources are chronological, so the k-th event of a given title
        takes the k-th slug. Illiwap really does have four events named "Fête
        au village de Comblain-la-Tour".
        """
        agenda = [
            dict(
                self.agenda[0],
                title="Fete au village",
                start=f"2026-09-0{day}T10:00:00+02:00",
            )
            for day in (1, 2, 3)
        ]
        listing = "".join(
            f'<a href="/fr/public/commune-de-test/evenements/{slug}"><h3>Fete au village</h3></a>'
            for slug in ("fete-au-village", "fete-au-village-1", "fete-au-village-2")
        )
        m.get(ILLIWAP_AGENDA_URL, json=agenda)
        m.get(ILLIWAP_AGENDA_PAGE_URL, text=listing)
        events = illiwap.get_events(ILLIWAP_AGENDA_PAGE_URL, 10)
        self.assertEqual(
            [event["url"].rsplit("/", 1)[-1] for event in events],
            ["fete-au-village", "fete-au-village-1", "fete-au-village-2"],
        )

    @requests_mock.Mocker()
    def test_get_events_stay_unlinked_when_listing_fails(self, m):
        """A broken listing must not cost us the events themselves"""
        m.get(ILLIWAP_AGENDA_URL, json=self.agenda)
        m.get(ILLIWAP_AGENDA_PAGE_URL, status_code=500)
        events = illiwap.get_events(ILLIWAP_AGENDA_PAGE_URL, 10)
        self.assertEqual(len(events), 3)
        self.assertTrue(all(event["url"] is None for event in events))

    @requests_mock.Mocker()
    def test_get_events_unmatched_event_stays_unlinked(self, m):
        """Never guess : an event with no card keeps no url at all"""
        m.get(ILLIWAP_AGENDA_URL, json=self.agenda)
        m.get(
            ILLIWAP_AGENDA_PAGE_URL,
            text='<a href="/fr/public/commune-de-test/evenements/enigm-ha-1">'
            "<h3>Enigm'Ha</h3></a>",
        )
        events = illiwap.get_events(ILLIWAP_AGENDA_PAGE_URL, 10)
        linked = {event["title"]: event["url"] for event in events}
        self.assertEqual(linked["Enigm'Ha"], f"{ILLIWAP_AGENDA_PAGE_URL}enigm-ha-1")
        self.assertIsNone(linked["Guinguette de Fairon"])
        self.assertIsNone(linked["Marathon de l'Ourthe 2026"])

    @requests_mock.Mocker()
    def test_get_events_does_not_poison_the_cached_events(self, m):
        """get_events copies before linking, the cached list must stay clean"""
        m.get(ILLIWAP_AGENDA_URL, json=self.agenda)
        m.get(ILLIWAP_AGENDA_PAGE_URL, status_code=500)
        self.assertTrue(
            all(e["url"] is None for e in illiwap.get_events(ILLIWAP_AGENDA_URL, 10))
        )
        m.get(ILLIWAP_AGENDA_PAGE_URL, text=self.listing)
        events = illiwap.get_events(ILLIWAP_AGENDA_URL, 10)
        self.assertEqual(events[0]["url"], f"{ILLIWAP_AGENDA_PAGE_URL}enigm-ha-1")

    @requests_mock.Mocker()
    def test_get_events_failed_read_is_not_cached(self, m):
        m.get(ILLIWAP_AGENDA_URL, status_code=503)
        self.assertIsNone(illiwap.get_events(ILLIWAP_AGENDA_URL, 10))
        m.get(ILLIWAP_AGENDA_URL, json=self.agenda)
        self.assertEqual(len(illiwap.get_events(ILLIWAP_AGENDA_URL, 10)), 3)
