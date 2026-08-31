# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from imio.smartweb.core import config
from imio.smartweb.core.browser.forms import SectionNewsCustomEditForm
from imio.smartweb.core.contents import ISectionNews
from imio.smartweb.core.contents.sections.views import SECTION_ITEMS_HASH_KEY
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.tests.utils import get_json
from imio.smartweb.core.tests.utils import mock_entity_newsfolders
from imio.smartweb.core.tests.utils import mock_newsfolder_scope
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.z3cform.interfaces import IPloneFormLayer
from plone.testing.zope import Browser
from time import sleep
from unittest.mock import patch
from z3c.form.browser.radio import RadioFieldWidget
from z3c.relationfield import RelationValue
from zope.annotation.interfaces import IAnnotations
from zope.component import getUtility
from zope.component import queryMultiAdapter
from zope.globalrequest import getRequest
from zope.globalrequest import setRequest
from zope.interface import alsoProvides
from zope.interface import Invalid
from zope.intid.interfaces import IIntIds
from zope.publisher.browser import TestRequest
from zope.schema.interfaces import IVocabularyFactory

import json
import re
import requests_mock
import transaction


class TestSectionNews(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

    def setUp(self):
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.portalpage = api.content.create(
            container=self.portal,
            type="imio.smartweb.PortalPage",
            id="Portal page",
        )
        self.json_news = get_json("resources/json_rest_news.json")
        self.json_specific_news = get_json("resources/json_rest_specific_news.json")
        self.rest_news_view = api.content.create(
            container=self.portal,
            type="imio.smartweb.NewsView",
            title="Rest news view",
        )
        self.news = api.content.create(
            container=self.portalpage,
            type="imio.smartweb.SectionNews",
            title="My news",
        )

    @requests_mock.Mocker()
    def test_news(self, m):
        intids = getUtility(IIntIds)
        self.news.related_news = "64f4cbee9a394a018a951f6d94452914"
        self.news.linking_rest_view = RelationValue(intids.getId(self.rest_news_view))
        self.news.link_text = "Voir toutes les actualités"
        # Juste a patch to avoid "checking entity (get_json)" in case of missing NewsFolder in auth sources
        with patch(
            "imio.smartweb.core.contents.sections.news.view.NewsView._get_news_folders_uids_and_title_from_entity",
            return_value=(
                ["64f4cbee9a394a018a951f6d94452914"],
                {"64f4cbee9a394a018a951f6d94452914": "News Folder title"},
            ),
        ):
            view = queryMultiAdapter((self.portalpage, self.request), name="full_view")
            self.assertIn("My news", view())
            news_view = queryMultiAdapter(
                (self.news, self.request), name="carousel_view"
            )
            self.assertEqual(news_view.items, [])

            url = "http://localhost:8080/Plone/@search_newsitems?selected_news_folders=64f4cbee9a394a018a951f6d94452914&portal_type=imio.news.NewsItem&metadata_fields=container_uid&metadata_fields=category_title&metadata_fields=local_category&metadata_fields=topics&metadata_fields=has_leadimage&metadata_fields=modified&metadata_fields=effective&metadata_fields=UID&sort_limit=6&translated_in_en=1&sort_on=effective&sort_order=descending"
            m.get(url, text=json.dumps(self.json_news))
            self.assertEqual(news_view.items[0][0].get("title"), "Première actualité")
            self.assertEqual(len(news_view.items[0]), 3)

            self.news.news_source = "selection"
            self.news.specific_related_newsitems = [
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "bfe2b4391a0f4a8db6d8b7fed63d1c4a",
            ]
            url = "http://localhost:8080/Plone/@search_newsitems?UID=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa&UID=bfe2b4391a0f4a8db6d8b7fed63d1c4a&portal_type=imio.news.NewsItem&metadata_fields=container_uid&metadata_fields=category_title&metadata_fields=local_category&metadata_fields=topics&metadata_fields=has_leadimage&metadata_fields=modified&metadata_fields=effective&metadata_fields=UID&sort_limit=6&translated_in_en=1"
            m.get(url, text=json.dumps(self.json_specific_news))
            self.assertEqual(len(news_view.items[0]), 2)
            self.assertEqual(
                news_view.items[0][0].get("title"), "Restauration de la piscine"
            )

            self.news.specific_related_newsitems = [
                "bfe2b4391a0f4a8db6d8b7fed63d1c4a",
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            ]
            m.get(url, text=json.dumps(self.json_specific_news))
            self.assertEqual(
                news_view.items[0][0].get("title"), "Restauration de la Bibliothèque"
            )

    @requests_mock.Mocker()
    def test_news_source(self, m):
        intids = getUtility(IIntIds)
        self.news.related_news = "64f4cbee9a394a018a951f6d94452914"
        self.news.linking_rest_view = RelationValue(intids.getId(self.rest_news_view))
        self.news.specific_related_newsitems = [
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            "bfe2b4391a0f4a8db6d8b7fed63d1c4a",
        ]
        newsfolder_url = "http://localhost:8080/Plone/@search_newsitems?selected_news_folders=64f4cbee9a394a018a951f6d94452914&portal_type=imio.news.NewsItem&metadata_fields=container_uid&metadata_fields=category_title&metadata_fields=local_category&metadata_fields=topics&metadata_fields=has_leadimage&metadata_fields=modified&metadata_fields=effective&metadata_fields=UID&sort_limit=6&translated_in_en=1&sort_on=effective&sort_order=descending"
        m.get(newsfolder_url, text=json.dumps(self.json_news))
        selection_url = "http://localhost:8080/Plone/@search_newsitems?UID=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa&UID=bfe2b4391a0f4a8db6d8b7fed63d1c4a&portal_type=imio.news.NewsItem&metadata_fields=container_uid&metadata_fields=category_title&metadata_fields=local_category&metadata_fields=topics&metadata_fields=has_leadimage&metadata_fields=modified&metadata_fields=effective&metadata_fields=UID&sort_limit=6&translated_in_en=1"
        m.get(selection_url, text=json.dumps(self.json_specific_news))
        # Juste a patch to avoid "checking entity (get_json)" in case of missing NewsFolder in auth sources
        with patch(
            "imio.smartweb.core.contents.sections.news.view.NewsView._get_news_folders_uids_and_title_from_entity",
            return_value=(
                ["64f4cbee9a394a018a951f6d94452914"],
                {"64f4cbee9a394a018a951f6d94452914": "News Folder title"},
            ),
        ):
            news_view = queryMultiAdapter(
                (self.news, self.request), name="carousel_view"
            )
            # the news folder is the default source: hand-picked items stay dormant
            self.assertEqual(self.news.news_source, "newsfolder")
            self.assertEqual(len(news_view.items[0]), 3)
            self.assertEqual(
                news_view.items[0][0].get("title"), "Premi\u00e8re actualit\u00e9"
            )
            # switching the source is what activates the hand-picked selection
            self.news.news_source = "selection"
            self.assertEqual(len(news_view.items[0]), 2)
            self.assertEqual(
                news_view.items[0][0].get("title"), "Restauration de la piscine"
            )

    @requests_mock.Mocker()
    def test_hand_picked_items_link_to_the_default_news_view(self, m):
        # A hand-picked item is put forward whatever folder it sits in, so it
        # cannot link to linking_rest_view (which shows one folder plus the ones
        # populating it). It links to the control panel's default news view, and
        # BaseNewsEndpoint retries unscoped by UID so the detail page resolves.
        intids = getUtility(IIntIds)
        self.news.related_news = "64f4cbee9a394a018a951f6d94452914"
        self.news.linking_rest_view = RelationValue(intids.getId(self.rest_news_view))
        self.news.news_source = "selection"
        self.news.specific_related_newsitems = [
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            "bfe2b4391a0f4a8db6d8b7fed63d1c4a",
        ]
        url = "http://localhost:8080/Plone/@search_newsitems?UID=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa&UID=bfe2b4391a0f4a8db6d8b7fed63d1c4a&portal_type=imio.news.NewsItem&metadata_fields=container_uid&metadata_fields=category_title&metadata_fields=local_category&metadata_fields=topics&metadata_fields=has_leadimage&metadata_fields=modified&metadata_fields=effective&metadata_fields=UID&sort_limit=6&translated_in_en=1"
        m.get(url, text=json.dumps(self.json_specific_news))
        default_view = api.content.create(
            container=self.portal,
            type="imio.smartweb.NewsView",
            title="Default news view",
        )
        news_view = queryMultiAdapter((self.news, self.request), name="carousel_view")

        # no default news view configured yet: nothing to link to. The linking
        # view is NOT used as a fallback -- it plays no part in this mode, and
        # the invariant refuses to save such a section in the first place.
        self.assertEqual(news_view.item_view_url, "")
        self.assertEqual(news_view.see_all_url, "")

        api.portal.set_registry_record("smartweb.default_news_view", default_view.UID())
        news_view = queryMultiAdapter((self.news, self.request), name="carousel_view")
        self.assertTrue(
            news_view.items[0][0]["url"].startswith(default_view.absolute_url())
        )
        # "see all" goes to the same default view, not to the linking view
        self.assertEqual(news_view.see_all_url, default_view.absolute_url())

        # a news folder section is unaffected: its items stay on the linking view
        self.news.news_source = "newsfolder"
        with patch(
            "imio.smartweb.core.contents.sections.news.view.NewsView."
            "_get_news_folders_uids_and_title_from_entity",
            return_value=(
                ["64f4cbee9a394a018a951f6d94452914"],
                {"64f4cbee9a394a018a951f6d94452914": "News Folder title"},
            ),
        ):
            m.get(
                re.compile(
                    re.escape(config.NEWS_URL)
                    + r"/@search_newsitems\?selected_news_folders="
                ),
                text=json.dumps(self.json_news),
            )
            news_view = queryMultiAdapter(
                (self.news, self.request), name="carousel_view"
            )
            self.assertTrue(
                news_view.items[0][0]["url"].startswith(
                    self.rest_news_view.absolute_url()
                )
            )
            self.assertEqual(news_view.see_all_url, self.rest_news_view.absolute_url())

    def test_news_source_invariant(self):
        class Data:
            news_source = "selection"
            linking_rest_view = None
            related_news = "64f4cbee9a394a018a951f6d94452914"
            specific_related_newsitems = []

        # "selection" without a single news item picked is not a usable section
        with self.assertRaises(Invalid):
            ISectionNews.validateInvariants(Data())

        Data.specific_related_newsitems = ["bfe2b4391a0f4a8db6d8b7fed63d1c4a"]
        # ...nor is it while the control panel has no default news view: that
        # is where a hand-picked item links, linking_rest_view plays no part
        with self.assertRaises(Invalid):
            ISectionNews.validateInvariants(Data())

        default_view = api.content.create(
            container=self.portal,
            type="imio.smartweb.NewsView",
            title="Default news view",
        )
        api.portal.set_registry_record("smartweb.default_news_view", default_view.UID())
        # a hand-picked section validates without any linking view
        ISectionNews.validateInvariants(Data())

        # "newsfolder" needs a linking view, since that is what scopes it
        Data.news_source = "newsfolder"
        with self.assertRaises(Invalid):
            ISectionNews.validateInvariants(Data())

        intids = getUtility(IIntIds)
        Data.linking_rest_view = RelationValue(intids.getId(self.rest_news_view))

        # ...and a news folder
        Data.related_news = None
        with self.assertRaises(Invalid):
            ISectionNews.validateInvariants(Data())

        Data.related_news = "64f4cbee9a394a018a951f6d94452914"
        ISectionNews.validateInvariants(Data())

    def test_linking_rest_view_comes_first(self):
        names = list(ISectionNews.names(all=False))
        self.assertLess(names.index("linking_rest_view"), names.index("news_source"))
        self.assertLess(names.index("news_source"), names.index("related_news"))
        self.assertLess(
            names.index("related_news"), names.index("specific_related_newsitems")
        )

    @requests_mock.Mocker()
    def test_news_source_invariant_rejects_an_out_of_scope_folder(self, m):
        # through the REAL form: data.linking_rest_view is the content object,
        # not a RelationValue, and a hand-built RelationValue would not catch a
        # regression here.
        folder_uid = "dddd0000dddd0000dddd0000dddd0014"
        mock_newsfolder_scope(m, folder_uid, populating=[("in-scope", "CPAS")])
        # the form binds/prunes specific_related_newsitems, which builds the
        # entity-wide NewsItemsFromEntity vocabulary
        mock_entity_newsfolders(m)
        m.get(
            re.compile(
                re.escape(config.NEWS_URL) + r"/@search\?selected_news_folders="
            ),
            text=json.dumps({"items": []}),
        )

        self.rest_news_view.selected_news_folder = folder_uid
        # ScopedNewsFoldersVocabularyFactory only keeps an out-of-scope value
        # selectable in the widget when it is the object's *currently stored*
        # related_news (so a misconfigured section's edit form can still
        # render) -- a brand new out-of-scope token that was never stored
        # would be refused by the widget itself before reaching the
        # invariant. Storing it first is what makes this a real test of the
        # invariant refusing a submission, not of the widget refusing it.
        self.news.related_news = "out-of-scope"
        previous_request = getRequest()
        self.addCleanup(setRequest, previous_request)

        def submit(related):
            request = TestRequest(
                form={
                    "form.widgets.title": "My news",
                    "form.widgets.news_source": ["newsfolder"],
                    "form.widgets.news_source-empty-marker": "1",
                    "form.widgets.linking_rest_view": [self.rest_news_view.UID()],
                    "form.widgets.related_news": [related],
                    "form.widgets.specific_related_newsitems": [],
                    "form.widgets.nb_results_by_batch": ["3"],
                    "form.widgets.max_nb_batches": "2",
                    "form.widgets.link_text": "See all news",
                    "form.widgets.ICategoryDisplay.show_categories_or_topics": [
                        "category"
                    ],
                    "form.widgets.IOrientation.orientation": ["paysage"],
                }
            )
            alsoProvides(request, IPloneFormLayer)
            # ScopedNewsFolders (behind related_news) resolves the submitted
            # linking_rest_view via zope.globalrequest.getRequest(), which a
            # bare TestRequest never becomes on its own -- a real HTTP
            # request is registered there by the publisher.
            setRequest(request)
            form = SectionNewsCustomEditForm(self.news, request)
            form.update()
            data, errors = form.extractData()
            return [getattr(error, "message", None) or str(error) for error in errors]

        self.assertEqual(submit("in-scope"), [])
        self.assertIn(
            "This news folder is not displayed by the selected news view.",
            submit("out-of-scope"),
        )

    def test_news_source_radio_widget(self):
        # browser/static/src/edit.js hides the field that does not match the
        # chosen source, addressing the radio inputs by name and switching on
        # their value, so both must keep the shape the script expects.
        widget = RadioFieldWidget(
            ISectionNews["news_source"].bind(self.news), self.request
        )
        widget.id = "form-widgets-news_source"
        widget.name = "form.widgets.news_source"
        widget.update()
        soup = BeautifulSoup(widget.render())
        radios = soup.find_all("input", {"type": "radio"})
        self.assertEqual(
            [radio["name"] for radio in radios],
            ["form.widgets.news_source", "form.widgets.news_source"],
        )
        self.assertEqual(
            [radio["value"] for radio in radios], ["newsfolder", "selection"]
        )

    @requests_mock.Mocker()
    def test_edit_js_dom_contract(self, m):
        # browser/static/src/edit.js addresses these three widgets by id and
        # relies on their pattern classes. A change here silently breaks the
        # cascade, so pin it.
        # the form binds/prunes specific_related_newsitems, which builds the
        # entity-wide NewsItemsFromEntity vocabulary
        mock_entity_newsfolders(m)
        m.get(
            re.compile(
                re.escape(config.NEWS_URL) + r"/@search\?selected_news_folders="
            ),
            text=json.dumps({"items": []}),
        )
        transaction.commit()
        browser = Browser(self.layer["app"])
        browser.handleErrors = False
        browser.addHeader(
            "Authorization", "Basic %s:%s" % (TEST_USER_NAME, TEST_USER_PASSWORD)
        )
        browser.open(
            "{}/++add++imio.smartweb.SectionNews".format(self.portalpage.absolute_url())
        )
        soup = BeautifulSoup(browser.contents, "html.parser")

        linking = soup.find(id="form-widgets-linking_rest_view")
        self.assertIn("pat-contentbrowser", linking["class"])

        related = soup.find(id="form-widgets-related_news")
        self.assertEqual(related.name, "select")
        self.assertIn("pat-select2", related["class"])

        specific = soup.find(id="form-widgets-specific_related_newsitems")
        self.assertIn("pat-select2", specific["class"])
        self.assertIn("@@getVocabulary", specific["data-pat-select2"])

    @requests_mock.Mocker()
    def test_news_source_invariant_on_edit_form(self, m):
        # the invariant must surface exactly one error on a real submission:
        # plone.z3cform validates invariants once per fieldset group and only
        # the pass carrying the source fields may judge them.
        m.get(
            f"{config.NEWS_URL}/@search?UID=7c69f9a738ec497c819725c55888ee32",
            text=json.dumps(get_json("resources/json_news_entities_raw_mock.json")),
        )
        m.get(
            f"{config.NEWS_URL}/imio-news-entity/@search?portal_type=imio.news.NewsFolder&sort_on=sortable_title&b_size=1000000&metadata_fields=UID",
            text=json.dumps(get_json("resources/json_news_newsfolder_raw_mock.json")),
        )
        # related_news is now validated against the scoped vocabulary: make
        # the submitted uid genuinely in scope for self.rest_news_view.
        related_news_uid = "64f4cbee9a394a018a951f6d94452914"
        mock_newsfolder_scope(m, related_news_uid)
        self.rest_news_view.selected_news_folder = related_news_uid
        previous_request = getRequest()
        self.addCleanup(setRequest, previous_request)

        def submit(source):
            request = TestRequest(
                form={
                    "form.widgets.title": "My news",
                    "form.widgets.news_source": [source],
                    "form.widgets.news_source-empty-marker": "1",
                    "form.widgets.related_news": [related_news_uid],
                    "form.widgets.specific_related_newsitems": [],
                    "form.widgets.linking_rest_view": [self.rest_news_view.UID()],
                    "form.widgets.nb_results_by_batch": ["3"],
                    "form.widgets.max_nb_batches": "2",
                    "form.widgets.link_text": "See all news",
                    "form.widgets.ICategoryDisplay.show_categories_or_topics": [
                        "category"
                    ],
                    "form.widgets.IOrientation.orientation": ["paysage"],
                }
            )
            alsoProvides(request, IPloneFormLayer)
            # ScopedNewsFolders (behind related_news) resolves the submitted
            # linking_rest_view via zope.globalrequest.getRequest(), which a
            # bare TestRequest never becomes on its own -- a real HTTP
            # request is registered there by the publisher.
            setRequest(request)
            form = SectionNewsCustomEditForm(self.news, request)
            form.update()
            data, errors = form.extractData()
            return [getattr(error, "message", None) or str(error) for error in errors]

        # "selection" with nothing picked is refused...
        self.assertEqual(submit("selection"), ["Please select at least one news item."])
        # ...while the very same submission on the news folder source goes through
        self.assertEqual(submit("newsfolder"), [])

    @requests_mock.Mocker()
    def test_specific_related_newsitems_survive_remote_outage(self, m):
        # WEB-4338's cleanup prunes any stored uid the vocabulary doesn't
        # recognize, merely on opening the edit form. An empty
        # NewsItemsFromEntity vocabulary means "cannot tell" -- here, the remote
        # being unreachable -- never "every stored value is invalid": it must
        # not silently wipe a hand-picked selection.
        mock_entity_newsfolders(m)
        m.get(
            re.compile(
                re.escape(config.NEWS_URL) + r"/@search\?selected_news_folders="
            ),
            status_code=503,
        )
        folder_uid = "dddd0000dddd0000dddd0000dddd0013"
        mock_newsfolder_scope(m, folder_uid)
        self.rest_news_view.selected_news_folder = folder_uid
        intids = getUtility(IIntIds)
        self.news.linking_rest_view = RelationValue(intids.getId(self.rest_news_view))
        self.news.news_source = "selection"
        self.news.specific_related_newsitems = ["kept-1", "kept-2"]
        request = TestRequest(form={})
        alsoProvides(request, IPloneFormLayer)
        form = SectionNewsCustomEditForm(self.news, request)
        form.update()
        self.assertEqual(self.news.specific_related_newsitems, ["kept-1", "kept-2"])

    @requests_mock.Mocker()
    def test_news_modified(self, m):
        intids = getUtility(IIntIds)
        self.news.related_news = "64f4cbee9a394a018a951f6d94452914"
        self.news.linking_rest_view = RelationValue(intids.getId(self.rest_news_view))
        annotations = IAnnotations(self.news)
        self.assertIsNone(annotations.get(SECTION_ITEMS_HASH_KEY))
        # Juste a patch to avoid "checking entity (get_json)" in case of missing NewsFolder in auth sources
        with patch(
            "imio.smartweb.core.contents.sections.news.view.NewsView._get_news_folders_uids_and_title_from_entity",
            return_value=(
                ["64f4cbee9a394a018a951f6d94452914"],
                {"64f4cbee9a394a018a951f6d94452914": "News Folder title"},
            ),
        ):
            news_view = queryMultiAdapter(
                (self.news, self.request), name="carousel_view"
            )
            url = "http://localhost:8080/Plone/@search_newsitems?selected_news_folders=64f4cbee9a394a018a951f6d94452914&portal_type=imio.news.NewsItem&metadata_fields=container_uid&metadata_fields=category_title&metadata_fields=local_category&metadata_fields=topics&metadata_fields=has_leadimage&metadata_fields=modified&metadata_fields=effective&metadata_fields=UID&sort_limit=6&translated_in_en=1&sort_on=effective&sort_order=descending"
            m.get(url, text=json.dumps(self.json_news))
            self.assertEqual(len(news_view.items[0]), 3)
            hash_1 = annotations.get(SECTION_ITEMS_HASH_KEY)
            self.assertIsNotNone(hash_1)
            first_modification = self.portalpage.ModificationDate()

            sleep(1)
            url = "http://localhost:8080/Plone/@search_newsitems?selected_news_folders=64f4cbee9a394a018a951f6d94452914&portal_type=imio.news.NewsItem&metadata_fields=container_uid&metadata_fields=category_title&metadata_fields=local_category&metadata_fields=topics&metadata_fields=has_leadimage&metadata_fields=modified&metadata_fields=effective&metadata_fields=UID&sort_limit=6&translated_in_en=1&sort_on=effective&sort_order=descending"
            m.get(url, text="{}")
            self.assertEqual(len(news_view.items), 0)
            next_modification = self.portalpage.ModificationDate()
            hash_2 = annotations.get(SECTION_ITEMS_HASH_KEY)
            self.assertNotEqual(hash_1, hash_2)
            self.assertNotEqual(first_modification, next_modification)

            sleep(1)
            self.assertEqual(len(news_view.items), 0)
            last_modification = self.portalpage.ModificationDate()
            hash_3 = annotations.get(SECTION_ITEMS_HASH_KEY)
            self.assertEqual(hash_2, hash_3)
            self.assertEqual(next_modification, last_modification)

            sleep(1)
            url = "http://localhost:8080/Plone/@search_newsitems?selected_news_folders=64f4cbee9a394a018a951f6d94452914&portal_type=imio.news.NewsItem&metadata_fields=container_uid&metadata_fields=category_title&metadata_fields=local_category&metadata_fields=topics&metadata_fields=has_leadimage&metadata_fields=modified&metadata_fields=effective&metadata_fields=UID&sort_limit=6&translated_in_en=1&sort_on=effective&sort_order=descending"
            m.get(url, text=None)
            self.assertEqual(len(news_view.items), 0)
            no_modification = self.portalpage.ModificationDate()
            hash_4 = annotations.get(SECTION_ITEMS_HASH_KEY)
            self.assertEqual(hash_3, hash_4)
            self.assertEqual(last_modification, no_modification)

    @requests_mock.Mocker()
    def test_orientation(self, m):
        intids = getUtility(IIntIds)
        self.news.related_news = "64f4cbee9a394a018a951f6d94452914"
        self.news.linking_rest_view = RelationValue(intids.getId(self.rest_news_view))
        # Juste a patch to avoid "checking entity (get_json)" in case of missing NewsFolder in auth sources
        with patch(
            "imio.smartweb.core.contents.sections.news.view.NewsView._get_news_folders_uids_and_title_from_entity",
            return_value=(
                ["64f4cbee9a394a018a951f6d94452914"],
                {"64f4cbee9a394a018a951f6d94452914": "News Folder title"},
            ),
        ):
            news_view = queryMultiAdapter(
                (self.news, self.request), name="carousel_view"
            )
            url = "http://localhost:8080/Plone/@search_newsitems?selected_news_folders=64f4cbee9a394a018a951f6d94452914&portal_type=imio.news.NewsItem&metadata_fields=container_uid&metadata_fields=category_title&metadata_fields=local_category&metadata_fields=topics&metadata_fields=has_leadimage&metadata_fields=modified&metadata_fields=effective&metadata_fields=UID&sort_limit=6&translated_in_en=1&sort_on=effective&sort_order=descending"
            m.get(url, text=json.dumps(self.json_news))

            self.assertIn("paysage_vignette", news_view.items[0][0]["image"])
            self.news.orientation = "portrait"
            self.assertIn("portrait_vignette", news_view.items[0][0]["image"])

    @requests_mock.Mocker()
    def test_show_categories_or_topics(self, m):
        intids = getUtility(IIntIds)
        self.news.related_news = "64f4cbee9a394a018a951f6d94452914"
        self.news.linking_rest_view = RelationValue(intids.getId(self.rest_news_view))
        # Juste a patch to avoid "checking entity (get_json)" in case of missing NewsFolder in auth sources
        with patch(
            "imio.smartweb.core.contents.sections.news.view.NewsView._get_news_folders_uids_and_title_from_entity",
            return_value=(
                ["64f4cbee9a394a018a951f6d94452914"],
                {"64f4cbee9a394a018a951f6d94452914": "News Folder title"},
            ),
        ):
            news_view = queryMultiAdapter(
                (self.news, self.request), name="carousel_view"
            )
            url = "http://localhost:8080/Plone/@search_newsitems?selected_news_folders=64f4cbee9a394a018a951f6d94452914&portal_type=imio.news.NewsItem&metadata_fields=container_uid&metadata_fields=category_title&metadata_fields=local_category&metadata_fields=topics&metadata_fields=has_leadimage&metadata_fields=modified&metadata_fields=effective&metadata_fields=UID&sort_limit=6&translated_in_en=1&sort_on=effective&sort_order=descending"
            m.get(url, text=json.dumps(self.json_news))
            self.assertEqual(news_view.items[0][0]["category"], "Presse")
            self.news.show_categories_or_topics = "category"
            self.assertEqual(news_view.items[0][0]["category"], "Presse")
            self.news.show_categories_or_topics = "topic"
            self.assertEqual(news_view.items[0][0]["category"], "Education")
            self.news.show_categories_or_topics = ""
            self.assertEqual(news_view.items[0][0]["category"], "")

    def test_linking_rest_view_vocabulary_is_site_wide(self):
        # Regression: a SectionNews inside a minisite (INavigationRoot) must
        # accept a linking_rest_view pointing to a NewsView located outside
        # the minisite. With the navigation-root-scoped Catalog vocabulary
        # that was used before, validation raised ConstraintNotSatisfied.
        from imio.smartweb.core.behaviors.minisite import IImioSmartwebMinisite
        from zope.interface import alsoProvides

        minisite = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            id="minisite",
        )
        alsoProvides(minisite, IImioSmartwebMinisite)
        page = api.content.create(
            container=minisite,
            type="imio.smartweb.PortalPage",
            id="home",
        )
        section = api.content.create(
            container=page,
            type="imio.smartweb.SectionNews",
            title="Section in minisite",
        )

        factory = getUtility(
            IVocabularyFactory, "imio.smartweb.vocabulary.NewsViewsSite"
        )
        vocabulary = factory(section)
        self.assertIn(api.content.get_uuid(self.rest_news_view), vocabulary)
