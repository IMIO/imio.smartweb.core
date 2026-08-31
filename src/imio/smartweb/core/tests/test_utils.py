# -*- coding: utf-8 -*-

from freezegun import freeze_time
from imio.smartweb.core import config
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.tests.utils import make_named_image
from imio.smartweb.core.tests.utils import mock_agenda_scope
from imio.smartweb.core.tests.utils import mock_newsfolder_scope
from imio.smartweb.core.utils import batch_results
from imio.smartweb.core.utils import get_agenda_scope
from imio.smartweb.core.utils import get_agenda_scope_uids
from imio.smartweb.core.utils import get_linking_events_view
from imio.smartweb.core.utils import get_linking_rest_view
from imio.smartweb.core.utils import get_newsfolder_scope
from imio.smartweb.core.utils import get_newsfolder_scope_uids
from imio.smartweb.core.utils import get_plausible_vars
from imio.smartweb.core.utils import get_scale_url
from imio.smartweb.core.utils import get_ts_api_url
from imio.smartweb.core.utils import is_valid_url
from imio.smartweb.core.utils import populate_procedure_button_text
from imio.smartweb.core.utils import remove_cache_key
from imio.smartweb.core.tests.utils import get_json
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.namedfile.file import NamedBlobImage
from plone.registry.interfaces import IRegistry
from plone.uuid.interfaces import IUUID
from unittest.mock import patch
from zope.component import getUtility

import json
import requests_mock


class TestUtils(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests"""
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_batch_results(self):
        lst = [1, 2, 3, 4, 5, 6]
        self.assertEqual(batch_results(lst, 3), [[1, 2, 3], [4, 5, 6]])
        lst = [1, 2, 3, 4, 5, 6, 7]
        self.assertEqual(batch_results(lst, 3), [[1, 2, 3], [4, 5, 6], [7]])

    @freeze_time("2021-09-14 8:00:00")
    def test_get_scale_url(self):
        content = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            id="page",
        )
        self.assertEqual(
            get_scale_url(content, self.request, "image", "preview", ""), ""
        )
        uuid = IUUID(content)
        brain = api.content.find(UID=uuid)[0]
        self.assertEqual(get_scale_url(brain, self.request, "image", "preview", ""), "")

        content.image = NamedBlobImage(**make_named_image())
        content.reindexObject()
        self.assertIn(
            "http://nohost/plone/page/@@images/image-400-",
            get_scale_url(content, self.request, "image", "preview"),
        )
        paysage_scale = get_scale_url(
            content, self.request, "image", "affiche", "paysage"
        )
        portrait_scale = get_scale_url(
            content, self.request, "image", "affiche", "portrait"
        )
        self.assertIn("http://nohost/plone/page/@@images/image-750-", paysage_scale)
        self.assertIn("http://nohost/plone/page/@@images/image-448-", portrait_scale)
        self.assertNotEqual(paysage_scale, portrait_scale)
        self.assertEqual(
            get_scale_url(content, self.request, "image", "nonexisting"), ""
        )
        self.assertEqual(
            get_scale_url(content, self.request, "nonexisting", "preview"), ""
        )
        self.assertEqual(
            get_scale_url(content, self.request, "image", ""),
            "http://nohost/plone/page/@@images/image/?cache_key=78fd1bab198354b6877aed44e2ea0b4d",
        )
        brain = api.content.find(UID=uuid)[0]
        self.assertEqual(
            get_scale_url(brain, self.request, "image", "preview"),
            "http://nohost/plone/page/@@images/image/preview?cache_key=78fd1bab198354b6877aed44e2ea0b4d",
        )
        self.assertEqual(
            get_scale_url(brain, self.request, "image", "affiche", "paysage"),
            "http://nohost/plone/page/@@images/image/paysage_affiche?cache_key=78fd1bab198354b6877aed44e2ea0b4d",
        )
        self.assertEqual(
            get_scale_url(brain, self.request, "image", "affiche", "portrait"),
            "http://nohost/plone/page/@@images/image/portrait_affiche?cache_key=78fd1bab198354b6877aed44e2ea0b4d",
        )
        self.assertEqual(
            get_scale_url(brain, self.request, "image", "nonexisting"),
            "http://nohost/plone/page/@@images/image/nonexisting?cache_key=78fd1bab198354b6877aed44e2ea0b4d",
        )
        self.assertEqual(
            get_scale_url(brain, self.request, "image", ""),
            "http://nohost/plone/page/@@images/image/?cache_key=78fd1bab198354b6877aed44e2ea0b4d",
        )
        self.assertEqual(
            get_scale_url(brain, self.request, "image", "portrait_affiche", "portrait"),
            "http://nohost/plone/page/@@images/image/portrait_affiche?cache_key=78fd1bab198354b6877aed44e2ea0b4d",
        )

    def test_remove_cache_key(self):
        self.json_news = get_json("resources/json_news_raw_mock.json")
        self.assertIn("cache_key", self.json_news["@id"])
        for key in ["@id", "first", "last", "next"]:
            if key in self.json_news["batching"] and isinstance(
                self.json_news["batching"][key], str
            ):
                self.assertIn("cache_key", self.json_news["batching"][key])
        self.json_news = remove_cache_key(self.json_news)

        self.assertNotIn("cache_key", self.json_news["@id"])
        for key in ["@id", "first", "last", "next"]:
            if key in self.json_news["batching"] and isinstance(
                self.json_news["batching"][key], str
            ):
                self.assertNotIn("cache_key", self.json_news["batching"][key])

    def test_remove_cache_key_none(self):
        result = remove_cache_key(None)
        self.assertIsNone(result)

    def test_is_valid_url(self):
        self.assertTrue(is_valid_url("https://kamoulox.be"))
        self.assertTrue(is_valid_url("http://www.kamoulox.be/path?q=1"))
        self.assertFalse(is_valid_url("not-a-url"))
        self.assertFalse(is_valid_url("ftp://kamoulox.be"))
        self.assertFalse(is_valid_url(""))

    def test_get_ts_api_url_no_registry_value(self):
        # When registry value is None, returns None
        with patch("imio.smartweb.core.utils.get_value_from_registry") as mock_registry:
            mock_registry.return_value = None
            result = get_ts_api_url("wcs")
            self.assertIsNone(result)

    def test_get_ts_api_url_invalid_url(self):
        with patch("imio.smartweb.core.utils.get_value_from_registry") as mock_registry:
            mock_registry.return_value = "not-a-valid-url"
            result = get_ts_api_url("wcs")
            self.assertIsNone(result)

    def test_get_ts_api_url_valid_url(self):
        with patch("imio.smartweb.core.utils.get_value_from_registry") as mock_registry:
            mock_registry.return_value = "https://mysite.guichet-citoyen.be"
            result = get_ts_api_url("wcs")
            self.assertIsNotNone(result)
            self.assertIn("-formulaires.guichet-citoyen.be", result)
            self.assertIn("/api", result)

    def test_get_plausible_vars_not_set(self):
        # By default, registry values are None, so get_plausible_vars returns None
        result = get_plausible_vars()
        self.assertIsNone(result)

    def test_populate_procedure_button_text(self):
        populate_procedure_button_text()
        registry = getUtility(IRegistry)
        labels = registry.get("smartweb.procedure_button_text")
        self.assertIsNotNone(labels)
        self.assertGreater(len(labels), 0)

    @requests_mock.Mocker()
    def test_get_agenda_scope(self, m):
        agenda_uid = "e73e6a81afea4a579cd0da2773af8d29"
        m.get(
            f"{config.EVENTS_URL}/@search?UID={agenda_uid}&metadata_fields=UID",
            text=json.dumps(get_json("resources/json_agenda_search_by_uid.json")),
        )
        m.get(
            "http://localhost:8080/Plone/belleville/agenda-global",
            text=json.dumps(
                get_json("resources/json_agenda_with_populating_agendas.json")
            ),
        )
        self.assertEqual(
            get_agenda_scope(agenda_uid),
            [
                ("e73e6a81afea4a579cd0da2773af8d29", "Agenda global"),
                ("7067db6012454155b8508f69b9b36fa7", "Agenda communal"),
                ("19c7a4e86f9b46be9ef93a038752a727", "CPAS"),
            ],
        )

    def test_get_agenda_scope_without_agenda(self):
        self.assertEqual(get_agenda_scope(None), [])
        self.assertEqual(get_agenda_scope(""), [])

    @requests_mock.Mocker()
    def test_get_agenda_scope_with_an_unknown_agenda(self, m):
        agenda_uid = "cccc0000cccc0000cccc0000cccc0002"
        m.get(
            f"{config.EVENTS_URL}/@search?UID={agenda_uid}&metadata_fields=UID",
            text=json.dumps({"items": [], "items_total": 0}),
        )
        self.assertEqual(get_agenda_scope(agenda_uid), [])

    @requests_mock.Mocker()
    def test_get_agenda_scope_when_remote_is_down(self, m):
        agenda_uid = "cccc0000cccc0000cccc0000cccc0003"
        m.get(
            f"{config.EVENTS_URL}/@search?UID={agenda_uid}&metadata_fields=UID",
            status_code=500,
        )
        self.assertEqual(get_agenda_scope(agenda_uid), [])

    @requests_mock.Mocker()
    def test_get_agenda_scope_when_the_agenda_itself_is_unreachable(self, m):
        # the catalog knows the agenda but the object GET fails: return no scope
        # rather than a half-built one.
        agenda_uid = "cccc0000cccc0000cccc0000cccc0004"
        m.get(
            f"{config.EVENTS_URL}/@search?UID={agenda_uid}&metadata_fields=UID",
            text=json.dumps(
                {
                    "items": [
                        {"@id": "http://localhost:8080/Plone/nope", "UID": agenda_uid}
                    ]
                }
            ),
        )
        m.get("http://localhost:8080/Plone/nope", status_code=500)
        self.assertEqual(get_agenda_scope(agenda_uid), [])

    @requests_mock.Mocker()
    def test_get_agenda_scope_is_cached(self, m):
        # this runs on every render of the events section edit form; without the
        # cache each one would hit the authentic source twice.
        agenda_uid = "cccc0000cccc0000cccc0000cccc0001"
        listing = m.get(
            f"{config.EVENTS_URL}/@search?UID={agenda_uid}&metadata_fields=UID",
            text=json.dumps(
                {"items": [{"@id": "http://localhost:8080/Plone/a", "UID": agenda_uid}]}
            ),
        )
        agenda = m.get(
            "http://localhost:8080/Plone/a",
            text=json.dumps(
                {"UID": agenda_uid, "title": "G", "populating_agendas": []}
            ),
        )
        get_agenda_scope(agenda_uid)
        get_agenda_scope(agenda_uid)
        self.assertEqual(listing.call_count, 1)
        self.assertEqual(agenda.call_count, 1)

    @requests_mock.Mocker()
    def test_get_agenda_scope_failure_is_not_cached(self, m):
        # a five-minute cache over a failed lookup would turn one blip into an
        # empty agenda dropdown for every editor, and the callers' "scope and"
        # guard leaves them no error message to explain it. Only a successful
        # scope is remembered.
        agenda_uid = "cccc0000cccc0000cccc0000cccc0005"
        listing = m.get(
            f"{config.EVENTS_URL}/@search?UID={agenda_uid}&metadata_fields=UID",
            [
                {"status_code": 503},
                {
                    "text": json.dumps(
                        {
                            "items": [
                                {
                                    "@id": "http://localhost:8080/Plone/b",
                                    "UID": agenda_uid,
                                }
                            ]
                        }
                    )
                },
            ],
        )
        m.get(
            "http://localhost:8080/Plone/b",
            text=json.dumps(
                {"UID": agenda_uid, "title": "G", "populating_agendas": []}
            ),
        )

        self.assertEqual(get_agenda_scope(agenda_uid), [])
        # same agenda, same cache window: the remote is queried again and the
        # scope comes back as soon as the remote does
        self.assertEqual(get_agenda_scope(agenda_uid), [(agenda_uid, "G")])
        self.assertEqual(listing.call_count, 2)

    @requests_mock.Mocker()
    def test_get_agenda_scope_uids(self, m):
        # the single source of truth for the rule shared by the ISectionEvents
        # invariant and the @@sections-out-of-scope report
        agenda_uid = "cccc0000cccc0000cccc0000cccc0006"
        mock_agenda_scope(m, agenda_uid, populating=[("cpas-uid", "CPAS")])
        self.assertEqual(get_agenda_scope_uids(agenda_uid), [agenda_uid, "cpas-uid"])

    def test_get_agenda_scope_uids_without_agenda(self):
        # "cannot tell", which every caller guards with "scope and"
        self.assertEqual(get_agenda_scope_uids(None), [])

    def test_get_linking_events_view_prefers_the_submitted_value(self):
        from plone.app.testing import setRoles
        from plone.app.testing import TEST_USER_ID
        from z3c.relationfield import RelationValue
        from zope.component import getUtility
        from zope.intid.interfaces import IIntIds

        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        saved_view = api.content.create(
            container=self.portal, type="imio.smartweb.EventsView", title="Enregistree"
        )
        submitted_view = api.content.create(
            container=self.portal, type="imio.smartweb.EventsView", title="Soumise"
        )
        page = api.content.create(
            container=self.portal, type="imio.smartweb.PortalPage", id="lv"
        )
        section = api.content.create(
            container=page, type="imio.smartweb.SectionEvents", title="S"
        )
        intids = getUtility(IIntIds)
        section.linking_rest_view = RelationValue(intids.getId(saved_view))

        # nothing submitted: the stored relation wins
        self.assertEqual(get_linking_events_view(section), saved_view)

        # the AJAX widget sends this key
        self.request.form["linking_rest_view"] = submitted_view.UID()
        self.assertEqual(get_linking_events_view(section), submitted_view)
        del self.request.form["linking_rest_view"]

        # the form POST sends this one, possibly as a list and ";"-separated
        self.request.form["form.widgets.linking_rest_view"] = [
            submitted_view.UID() + ";"
        ]
        self.assertEqual(get_linking_events_view(section), submitted_view)
        del self.request.form["form.widgets.linking_rest_view"]

    def test_get_linking_events_view_without_anything(self):
        # ++add++ before the editor picked a view
        self.assertIsNone(get_linking_events_view(self.portal))

    @requests_mock.Mocker()
    def test_get_newsfolder_scope(self, m):
        folder_uid = "dddd0000dddd0000dddd0000dddd0001"
        m.get(
            f"{config.NEWS_URL}/@search?UID={folder_uid}&metadata_fields=UID",
            text=json.dumps(
                {
                    "items": [
                        {
                            "@id": "http://localhost:8080/Plone/newsfolders/global",
                            "UID": folder_uid,
                        }
                    ]
                }
            ),
        )
        m.get(
            "http://localhost:8080/Plone/newsfolders/global",
            text=json.dumps(
                {
                    "UID": folder_uid,
                    "title": "Actualites globales",
                    "populating_newsfolders": [
                        {"UID": "cpas-folder", "title": "CPAS"},
                        {"UID": "biblio-folder", "title": "Bibliotheque"},
                    ],
                }
            ),
        )
        self.assertEqual(
            get_newsfolder_scope(folder_uid),
            [
                (folder_uid, "Actualites globales"),
                ("cpas-folder", "CPAS"),
                ("biblio-folder", "Bibliotheque"),
            ],
        )
        self.assertEqual(
            get_newsfolder_scope_uids(folder_uid),
            [folder_uid, "cpas-folder", "biblio-folder"],
        )

    def test_get_newsfolder_scope_without_folder(self):
        self.assertEqual(get_newsfolder_scope(None), [])
        self.assertEqual(get_newsfolder_scope(""), [])

    @requests_mock.Mocker()
    def test_get_newsfolder_scope_when_remote_is_down(self, m):
        folder_uid = "dddd0000dddd0000dddd0000dddd0002"
        m.get(
            f"{config.NEWS_URL}/@search?UID={folder_uid}&metadata_fields=UID",
            status_code=500,
        )
        self.assertEqual(get_newsfolder_scope(folder_uid), [])

    @requests_mock.Mocker()
    def test_get_newsfolder_scope_does_not_cache_a_failure(self, m):
        # a one-second blip must not blank the folder dropdown for five minutes
        folder_uid = "dddd0000dddd0000dddd0000dddd0003"
        matcher = m.get(
            f"{config.NEWS_URL}/@search?UID={folder_uid}&metadata_fields=UID",
            status_code=503,
        )
        get_newsfolder_scope(folder_uid)
        get_newsfolder_scope(folder_uid)
        self.assertEqual(matcher.call_count, 2)

    @requests_mock.Mocker()
    def test_get_newsfolder_scope_is_cached_on_success(self, m):
        folder_uid = "dddd0000dddd0000dddd0000dddd0004"
        mock_newsfolder_scope(m, folder_uid)
        get_newsfolder_scope(folder_uid)
        get_newsfolder_scope(folder_uid)
        # requests_mock lower-cases the URL before recording it (unless
        # case_sensitive=True), so the query string on request_history reads
        # "metadata_fields=uid", not "...=UID".
        listing = [
            r for r in m.request_history if "metadata_fields=uid" in (r.query or "")
        ]
        self.assertEqual(len(listing), 1)

    def test_get_linking_rest_view_refuses_a_foreign_portal_type(self):
        # the scoping premise is that the linked object carries the container
        # field; anything else must resolve to None rather than a scopeless pass
        page = api.content.create(
            container=self.portal, type="imio.smartweb.PortalPage", id="lrv"
        )
        self.request.form["linking_rest_view"] = page.UID()
        try:
            self.assertIsNone(
                get_linking_rest_view(self.portal, "imio.smartweb.NewsView")
            )
            self.assertIsNone(
                get_linking_rest_view(self.portal, "imio.smartweb.EventsView")
            )
        finally:
            del self.request.form["linking_rest_view"]
