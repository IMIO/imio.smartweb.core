# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from imio.smartweb.core.contents.sections.external_content import illiwap
from imio.smartweb.core.contents.sections.external_content.views import ArcgisPlugin
from imio.smartweb.core.contents.sections.external_content.views import ArcgisView
from imio.smartweb.core.contents.sections.external_content.views import BasePlugin
from imio.smartweb.core.contents.sections.external_content.views import (
    CognitoformPlugin,
)
from imio.smartweb.core.contents.sections.external_content.views import EaglebePlugin
from imio.smartweb.core.contents.sections.external_content.views import EllohaPlugin
from imio.smartweb.core.contents.sections.external_content.views import GiveADayPlugin
from imio.smartweb.core.contents.sections.external_content.views import (
    IdeluxWastePlugin,
)
from imio.smartweb.core.contents.sections.external_content.views import (
    IIdeluxWastePlugin,
)
from imio.smartweb.core.contents.sections.external_content.views import (
    InbwContainersAffluencePlugin,
)
from imio.smartweb.core.contents.sections.external_content.views import (
    IInbwContainersAffluencePlugin,
)
from imio.smartweb.core.contents.sections.external_content.views import (
    IOdwbWidgetPlugin,
)
from imio.smartweb.core.contents.sections.external_content.views import OdwbWidgetPlugin
from imio.smartweb.core.contents.sections.external_content.views import (
    UnknowServicePlugin,
)
from imio.smartweb.core.interfaces import IOdwbViewUtils
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.tests.utils import clear_ram_cache
from imio.smartweb.core.tests.utils import get_html
from imio.smartweb.core.tests.utils import get_json
from imio.smartweb.core.viewlets.external_content import ArcgisHeaderViewlet
from imio.smartweb.core.viewlets.external_content import OdwbWidgetHeaderViewlet
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from unittest.mock import MagicMock
from unittest.mock import patch
from urllib.parse import urlparse
from zope.component import queryMultiAdapter

import requests
import requests_mock
import requests_mock as requests_mock_module
import unittest

_VIEWS_MODULE = "imio.smartweb.core.contents.sections.external_content.views"
ILLIWAP_FEED_URL = "https://station.illiwap.com/rss/commune-de-test"
ILLIWAP_AGENDA_URL = "https://station.illiwap.com/fr/public/commune-de-test/agenda/list"
ILLIWAP_AGENDA_PAGE_URL = (
    "https://station.illiwap.com/fr/public/commune-de-test/evenements/"
)


class TestSectionExternalContent(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

    def setUp(self):
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            id="page",
        )

    def test_parent_marker_interface(self):
        sec1 = api.content.create(
            container=self.page, type="imio.smartweb.SectionExternalContent", id="sec1"
        )
        self.assertTrue(IOdwbViewUtils.providedBy(self.page))

        sec2 = api.content.create(
            container=self.page, type="imio.smartweb.SectionExternalContent", id="sec2"
        )
        api.content.delete(obj=sec1)
        self.assertTrue(IOdwbViewUtils.providedBy(self.page))

        api.content.delete(obj=sec2)
        self.assertFalse(IOdwbViewUtils.providedBy(self.page))

        api.content.create(
            container=self.page,
            type="imio.smartweb.SectionText",
            id="not_external_content_section",
        )
        self.assertFalse(IOdwbViewUtils.providedBy(self.page))

    def test_unknow_service(self):
        sec = api.content.create(
            container=self.page, type="imio.smartweb.SectionExternalContent", id="sec"
        )
        sec.external_content_url = "https://kamoulox.be"
        section_view = queryMultiAdapter((sec, self.request), name="view")
        self.assertEqual(
            section_view.contents,
            '<p class="unknow_service">Unknow service</p>',
        )

    def test_eaglebe_plugin(self):
        sec = api.content.create(
            container=self.page, type="imio.smartweb.SectionExternalContent", id="sec"
        )

        sec.external_content_url = ""
        section_view = queryMultiAdapter((sec, self.request), name="view")
        self.assertEqual(
            section_view.contents,
            '<p class="unknow_service">Unknow service</p>',
        )

        sec.external_content_url = "https://app.eaglebe.com/auth/start"
        section_view = queryMultiAdapter((sec, self.request), name="view")
        self.assertEqual(
            section_view.contents,
            '<iframe class="eaglebe" src="https://app.eaglebe.com/auth/start" scrolling="no" width="100%">',
        )

    def test_elloha_plugin(self):
        sec = api.content.create(
            container=self.page, type="imio.smartweb.SectionExternalContent", id="sec"
        )

        # without extra params
        sec.external_content_url = (
            "https://reservation.elloha.com/Scripts/widget-loader.min.js?v=42"
        )
        section_view = queryMultiAdapter((sec, self.request), name="view")
        self.assertEqual(
            section_view.contents,
            '<div class="elloha elloha_error">With an elloha plugin, extra params must contain a dictionary with two keys : ConstellationWidgetContainer, Idoi</div>',
        )

        # with good extra params
        sec.external_content_params = """{
            "ConstellationWidgetContainer" : "11111111-1111-1111-1111-111111111111",
            "Idoi" : "22222222-2222-2222-2222-222222222222"
        }"""
        self.maxDiff = None
        section_view = queryMultiAdapter((sec, self.request), name="view")
        result = '<div class="elloha" style="position:relative;"><div id="ConstellationWidgetContainer11111111-1111-1111-1111-111111111111" style="width:100%" data-id-projet="11111111111111111111111111111111">...</div></div><script type="text/javascript" src="https://reservation.elloha.com/Scripts/widget-loader.min.js?v=42"></script><script type="text/javascript">var constellationWidgetUrl11111111111111111111111111111111, constellationTypeModule11111111111111111111111111111111;constellationWidgetUrl11111111111111111111111111111111 = "https://reservation.elloha.com/Widget/BookingEngine/11111111-1111-1111-1111-111111111111?idoi=22222222-2222-2222-2222-222222222222&culture=fr-FR";constellationTypeModule11111111111111111111111111111111=1; constellationWidgetLoad("ConstellationWidgetContainer11111111-1111-1111-1111-111111111111");constellationWidgetAddEvent(window, "resize", function () {constellationWidgetSetAppearance("ConstellationWidgetContainer11111111-1111-1111-1111-111111111111");});</script>'
        self.assertEqual(section_view.contents, result)

        # good extra params / dict keys are case insensitive
        sec.external_content_params = """{
            "CONSTELLATIONWIDGETCONTAINER" : "11111111-1111-1111-1111-111111111111",
            "IDOI" : "22222222-2222-2222-2222-222222222222"
        }"""
        section_view = queryMultiAdapter((sec, self.request), name="view")
        result = '<div class="elloha" style="position:relative;"><div id="ConstellationWidgetContainer11111111-1111-1111-1111-111111111111" style="width:100%" data-id-projet="11111111111111111111111111111111">...</div></div><script type="text/javascript" src="https://reservation.elloha.com/Scripts/widget-loader.min.js?v=42"></script><script type="text/javascript">var constellationWidgetUrl11111111111111111111111111111111, constellationTypeModule11111111111111111111111111111111;constellationWidgetUrl11111111111111111111111111111111 = "https://reservation.elloha.com/Widget/BookingEngine/11111111-1111-1111-1111-111111111111?idoi=22222222-2222-2222-2222-222222222222&culture=fr-FR";constellationTypeModule11111111111111111111111111111111=1; constellationWidgetLoad("ConstellationWidgetContainer11111111-1111-1111-1111-111111111111");constellationWidgetAddEvent(window, "resize", function () {constellationWidgetSetAppearance("ConstellationWidgetContainer11111111-1111-1111-1111-111111111111");});</script>'
        self.assertEqual(section_view.contents, result)

        # with bad params
        sec.external_content_params = "kamoulox"
        section_view = queryMultiAdapter((sec, self.request), name="view")
        result = '<div class="elloha elloha_error">With an elloha plugin, extra params must contain a dictionary with two keys : ConstellationWidgetContainer, Idoi</div>'
        self.assertEqual(section_view.contents, result)

        sec.external_content_params = """{
            "ConstellationWidgetContainer" : "11111111-1111-1111-1111-111111111111"
        }"""
        section_view = queryMultiAdapter((sec, self.request), name="view")
        result = '<div class="elloha elloha_error">With an elloha plugin, extra params must contain a dictionary with two keys : ConstellationWidgetContainer, Idoi</div>'
        self.assertEqual(section_view.contents, result)

        sec.external_content_params = """{
            "CONSTELLATIONWIDGETCONTAINER" : "11111111-1111-1111-1111-111111111111",
            "IDOI" : "22222222-2222-2222-2222-222222222222"
        """
        section_view = queryMultiAdapter((sec, self.request), name="view")
        result = '<div class="elloha elloha_error">With an elloha plugin, extra params must contain a dictionary with two keys : ConstellationWidgetContainer, Idoi</div>'
        self.assertEqual(section_view.contents, result)

    def test_cognitoform_plugin(self):
        sec = api.content.create(
            container=self.page, type="imio.smartweb.SectionExternalContent", id="sec"
        )
        url = "https://www.cognitoforms.com/YourOrg/YourForm"
        sec.external_content_url = url

        # Without extra params → returns simple iframe
        section_view = queryMultiAdapter((sec, self.request), name="view")
        self.assertIn(f'<iframe src="{url}"', section_view.contents)
        self.assertIn("overflow: auto;", section_view.contents)

        # Bad format (no braces)
        sec.external_content_params = "scrolling=yes"
        section_view = queryMultiAdapter((sec, self.request), name="view")
        self.assertIn("cognitoform_error", section_view.contents)

        # Bad JSON
        sec.external_content_params = '{"scrolling": "yes"'
        section_view = queryMultiAdapter((sec, self.request), name="view")
        self.assertIn("cognitoform_error", section_view.contents)

        # Missing overflow key
        sec.external_content_params = '{"scrolling": "yes"}'
        section_view = queryMultiAdapter((sec, self.request), name="view")
        self.assertIn("cognitoform_error", section_view.contents)

        # Valid params
        sec.external_content_params = '{"scrolling": "yes", "overflow": "hidden"}'
        section_view = queryMultiAdapter((sec, self.request), name="view")
        self.assertIn("overflow: hidden;", section_view.contents)
        self.assertIn('scrolling="yes"', section_view.contents)

    def test_arcgis_plugin(self):
        sec = api.content.create(
            container=self.page, type="imio.smartweb.SectionExternalContent", id="sec"
        )
        sec.external_content_url = "https://www.arcgis.com/apps/mapviewer/index.html"

        # Without extra params → error
        section_view = queryMultiAdapter((sec, self.request), name="view")
        self.assertIn("arcgis_error", section_view.contents)

        # Bad format
        sec.external_content_params = "no braces here"
        section_view = queryMultiAdapter((sec, self.request), name="view")
        self.assertIn("arcgis_error", section_view.contents)

        # Bad JSON
        sec.external_content_params = '{"portal_item_id": "abc'
        section_view = queryMultiAdapter((sec, self.request), name="view")
        self.assertIn("arcgis_error", section_view.contents)

        # Missing portal_item_id
        sec.external_content_params = '{"other_key": "value"}'
        section_view = queryMultiAdapter((sec, self.request), name="view")
        self.assertIn("arcgis_error", section_view.contents)

        # Valid portal_item_id
        sec.external_content_params = (
            '{"portal_item_id": "27a432b0835149e6acd3ac39d0e4349c"}'
        )
        section_view = queryMultiAdapter((sec, self.request), name="view")
        self.assertIn(
            "view_arcgis?portal_item_id=27a432b0835149e6acd3ac39d0e4349c",
            section_view.contents,
        )

    def test_giveaday_plugin(self):
        sec = api.content.create(
            container=self.page, type="imio.smartweb.SectionExternalContent", id="sec"
        )
        sec.external_content_url = "https://www.giveaday.be/campaign/123"
        section_view = queryMultiAdapter((sec, self.request), name="view")
        self.assertIn("giveaday-widget", section_view.contents)
        self.assertIn("giveaday_v1.js", section_view.contents)

    def test_idelux_waste_plugin(self):
        sec = api.content.create(
            container=self.page, type="imio.smartweb.SectionExternalContent", id="sec"
        )
        odwb_url = "https://www.odwb.be/api/explore/v2.1/catalog/datasets/guide-de-tri1/records"
        sec.external_content_url = odwb_url
        mock_data = {"results": [{"material": "plastic", "bin": "yellow"}]}

        with requests_mock_module.Mocker() as m:
            m.get(f"{odwb_url}?limit=-1", json=mock_data)
            section_view = queryMultiAdapter((sec, self.request), name="view")
            result = section_view.contents
            self.assertEqual(result, mock_data)
            self.assertTrue(IIdeluxWastePlugin.providedBy(section_view.get_plugin()))
            self.assertEqual(section_view.which_plugin(), "ideluxwasteplugin")

    def test_inbw_containers_affluence_plugin(self):
        sec = api.content.create(
            container=self.page, type="imio.smartweb.SectionExternalContent", id="sec"
        )
        odwb_url = "https://www.odwb.be/api/explore/v2.1/catalog/datasets/affluence/records?dataset=affluence"
        sec.external_content_url = odwb_url
        mock_data = {"results": [{"location": "site-a", "level": "high"}]}

        with requests_mock_module.Mocker() as m:
            m.get(f"{odwb_url}&limit=-1", json=mock_data)
            section_view = queryMultiAdapter((sec, self.request), name="view")
            import json

            result = section_view.contents
            self.assertEqual(result, json.dumps(mock_data))
            self.assertTrue(
                IInbwContainersAffluencePlugin.providedBy(section_view.get_plugin())
            )
            self.assertEqual(
                section_view.which_plugin(), "inbwcontainersaffluenceplugin"
            )

    def test_odwb_widget_plugin(self):
        sec = api.content.create(
            container=self.page, type="imio.smartweb.SectionExternalContent", id="sec"
        )
        sec.external_content_url = (
            "https://static.opendatasoft.com/ods-widgets/my-widget"
        )
        sec.external_content_params = "<ods-dataset-context>...</ods-dataset-context>"
        section_view = queryMultiAdapter((sec, self.request), name="view")
        self.assertEqual(
            section_view.contents, "<ods-dataset-context>...</ods-dataset-context>"
        )
        self.assertTrue(IOdwbWidgetPlugin.providedBy(section_view.get_plugin()))
        self.assertTrue(section_view.display_odwb_widget_viewlet())
        self.assertEqual(section_view.which_plugin(), "odwbwidgetplugin")

    def test_illiwap_plugin(self):
        sec = api.content.create(
            container=self.page, type="imio.smartweb.SectionExternalContent", id="sec"
        )
        sec.external_content_url = ILLIWAP_FEED_URL
        section_view = queryMultiAdapter((sec, self.request), name="view")
        # an illiwap feed is not embedded : the default view only points the
        # editor to the table / carousel display
        self.assertIn("illiwap_hint", section_view.contents)
        self.assertIn("Illiwap news feed detected", section_view.contents)
        self.assertIsNone(section_view.which_plugin())

    def test_external_content_view_methods(self):
        sec = api.content.create(
            container=self.page, type="imio.smartweb.SectionExternalContent", id="sec"
        )
        # Non-special URL → which_plugin returns None, display_odwb_widget_viewlet False
        sec.external_content_url = "https://kamoulox.be"
        section_view = queryMultiAdapter((sec, self.request), name="view")
        self.assertIsNone(section_view.which_plugin())
        self.assertFalse(section_view.display_odwb_widget_viewlet())

        # has_leadimage → False (SectionExternalContent has no lead image by default)
        self.assertFalse(section_view.has_leadimage())

        # image → returns absolute_url + download path
        image_url = section_view.image()
        self.assertIn(sec.absolute_url(), image_url)
        self.assertIn("@@download/image", image_url)


class TestSectionExternalContent_params(ImioSmartwebTestCase):
    """external_content_params drives the illiwap display settings"""

    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.page = api.content.create(
            container=self.portal, type="imio.smartweb.Page", id="page"
        )
        self.section = api.content.create(
            container=self.page, type="imio.smartweb.SectionExternalContent", id="sec"
        )

    def test_manage_display(self):
        # only an illiwap feed has a display to choose from
        self.section.external_content_url = "https://app.eaglebe.com/auth/start"
        self.assertFalse(self.section.manage_display)
        self.section.external_content_url = ILLIWAP_FEED_URL
        self.assertTrue(self.section.manage_display)

    def test_defaults(self):
        self.assertEqual(self.section.params, {})
        self.assertEqual(self.section.nb_results_by_batch, 3)
        self.assertEqual(self.section.max_nb_batches, 3)
        self.assertFalse(self.section.show_items_description)

    def test_params_read_from_json(self):
        self.section.external_content_params = (
            '{"nb_results_by_batch": 4, "max_nb_batches": 2, '
            '"show_items_description": true}'
        )
        self.assertEqual(self.section.nb_results_by_batch, 4)
        self.assertEqual(self.section.max_nb_batches, 2)
        self.assertTrue(self.section.show_items_description)

    def test_params_of_another_plugin_are_ignored(self):
        self.section.external_content_params = (
            '{"portal_item_id": "27a432b0835149e6acd3ac39d0e4349c"}'
        )
        self.assertEqual(self.section.nb_results_by_batch, 3)
        self.assertEqual(self.section.max_nb_batches, 3)

    def test_params_are_clamped(self):
        # the templates lay out at most 4 columns (12 // nb_results_by_batch)
        self.section.external_content_params = '{"nb_results_by_batch": 99}'
        self.assertEqual(self.section.nb_results_by_batch, 4)
        self.section.external_content_params = '{"nb_results_by_batch": 0}'
        self.assertEqual(self.section.nb_results_by_batch, 1)
        self.section.external_content_params = '{"max_nb_batches": 99}'
        self.assertEqual(self.section.max_nb_batches, 12)

    def test_broken_params_fall_back_to_defaults(self):
        self.section.external_content_params = "kamoulox"
        self.assertEqual(self.section.params, {})
        self.assertEqual(self.section.nb_results_by_batch, 3)

        # valid json, but not a dictionary
        self.section.external_content_params = '["a", "list"]'
        self.assertEqual(self.section.params, {})

        # valid dictionary, but not a number
        self.section.external_content_params = '{"nb_results_by_batch": "trois"}'
        self.assertEqual(self.section.nb_results_by_batch, 3)


class TestIlliwapView(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

    def setUp(self):
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        # _fetch_news is ram cached on a time bucket, not per request
        clear_ram_cache(
            illiwap._fetch_news,
            illiwap._fetch_events,
            illiwap._fetch_event_slugs,
        )
        self.feed = get_html("resources/illiwap_rss_mock.xml").encode("utf-8")
        self.page = api.content.create(
            container=self.portal, type="imio.smartweb.Page", id="page"
        )
        self.section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionExternalContent",
            title="Actualités Illiwap",
        )
        self.section.external_content_url = ILLIWAP_FEED_URL

    @requests_mock.Mocker()
    def test_items_are_batched(self, m):
        m.get(ILLIWAP_FEED_URL, content=self.feed)
        view = queryMultiAdapter((self.section, self.request), name="table_view")
        # 3 items by batch by default, the feed holds 4
        self.assertEqual([len(batch) for batch in view.items], [3, 1])
        self.assertEqual(
            view.items[0][0]["title"], "Un coup de pouce pour réussir son permis"
        )

    @requests_mock.Mocker()
    def test_items_honour_params(self, m):
        m.get(ILLIWAP_FEED_URL, content=self.feed)
        self.section.external_content_params = (
            '{"nb_results_by_batch": 2, "max_nb_batches": 1}'
        )
        view = queryMultiAdapter((self.section, self.request), name="table_view")
        self.assertEqual([len(batch) for batch in view.items], [2])

    @requests_mock.Mocker()
    def test_items_when_feed_is_unavailable(self, m):
        m.get(ILLIWAP_FEED_URL, status_code=500)
        view = queryMultiAdapter((self.section, self.request), name="table_view")
        self.assertEqual(view.items, [])
        self.assertIn("Illiwap content is currently unavailable", view.issue)

    def test_items_when_url_is_not_illiwap(self):
        self.section.external_content_url = "https://app.eaglebe.com/auth/start"
        view = queryMultiAdapter((self.section, self.request), name="table_view")
        self.assertEqual(view.items, [])
        self.assertIn("Illiwap news feed", view.issue)

    @requests_mock.Mocker()
    def test_table_view_renders_the_news(self, m):
        m.get(ILLIWAP_FEED_URL, content=self.feed)
        self.section.external_content_params = '{"show_items_description": true}'
        self.section.setLayout("table_view")
        html = queryMultiAdapter((self.page, self.request), name="full_view")()
        soup = BeautifulSoup(html)

        titles = [tag.text.strip() for tag in soup.select("div.table_title span")]
        self.assertIn("Un coup de pouce pour réussir son permis", titles)
        self.assertEqual(len(titles), 4)

        # news are read on illiwap
        link = soup.select("div.table_display a.table_image")[0]
        self.assertEqual(
            link.get("href"),
            "https://station.illiwap.com/fr/public/commune-de-test/actu/un-coup-de-pouce",
        )
        # the template only renders target="_blank" for a visitor, but the
        # items do ask for it
        view = queryMultiAdapter((self.section, self.request), name="table_view")
        self.assertTrue(view.open_in_new_tab(view.items[0][0]))

        # the thumbnail dug out of the description html is used
        image = soup.select("div.table_display div.is-image")[0]
        self.assertIn("photo.jpg", image.get("style"))

        # the excerpt is shown once show_items_description is set
        self.assertIn(
            "Tu as entre 17 et 25 ans",
            soup.select("div.table_description")[0].text,
        )

    @requests_mock.Mocker()
    def test_carousel_view_renders_the_news(self, m):
        m.get(ILLIWAP_FEED_URL, content=self.feed)
        self.section.setLayout("carousel_view")
        html = queryMultiAdapter((self.page, self.request), name="full_view")()
        soup = BeautifulSoup(html)

        titles = [tag.text.strip() for tag in soup.select("div.swiper_title h3")]
        self.assertIn("Un coup de pouce pour réussir son permis", titles)
        self.assertEqual(len(titles), 4)

    @requests_mock.Mocker()
    def test_visitor_links_open_in_a_new_tab(self, m):
        """The templates only render target="_blank" for a visitor, never for
        an editor : render through the view a visitor gets.
        """
        m.get(ILLIWAP_FEED_URL, content=self.feed)
        self.section.setLayout("table_view")
        html = queryMultiAdapter(
            (self.section, self.request), name="full_view_item_without_edit"
        )()
        soup = BeautifulSoup(html)
        links = soup.select("div.table_display a.table_image")
        self.assertEqual(len(links), 4)
        for link in links:
            self.assertEqual(link.get("target"), "_blank")
            self.assertTrue(link.get("href").startswith("https://station.illiwap.com/"))

    @requests_mock.Mocker()
    def test_editor_is_warned_when_feed_is_unavailable(self, m):
        """No news is rendered, and the editor gets a translatable warning"""
        m.get(ILLIWAP_FEED_URL, status_code=500)
        self.section.setLayout("carousel_view")
        html = queryMultiAdapter((self.page, self.request), name="full_view")()
        soup = BeautifulSoup(html)
        self.assertEqual(soup.select("div.swiper_title"), [])
        self.assertIn(
            "Illiwap content is currently unavailable",
            soup.select("p.issue")[0].text,
        )


class TestIlliwapAgendaView(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

    def setUp(self):
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        clear_ram_cache(
            illiwap._fetch_news,
            illiwap._fetch_events,
            illiwap._fetch_event_slugs,
        )
        self.agenda = get_json("resources/json_illiwap_agenda_mock.json")
        self.listing = get_html("resources/illiwap_agenda_listing_mock.html")
        self.page = api.content.create(
            container=self.portal, type="imio.smartweb.Page", id="page"
        )
        self.section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionExternalContent",
            title="Agenda Illiwap",
        )
        self.section.external_content_url = ILLIWAP_AGENDA_PAGE_URL

    def test_manage_display(self):
        self.assertTrue(self.section.manage_display)

    @requests_mock.Mocker()
    def test_items_are_batched(self, m):
        m.get(ILLIWAP_AGENDA_URL, json=self.agenda)
        m.get(ILLIWAP_AGENDA_PAGE_URL, text=self.listing)
        view = queryMultiAdapter((self.section, self.request), name="table_view")
        # 3 by batch by default, the mock holds 3 usable events
        self.assertEqual([len(batch) for batch in view.items], [3])

    @requests_mock.Mocker()
    def test_table_view_renders_the_events(self, m):
        m.get(ILLIWAP_AGENDA_URL, json=self.agenda)
        m.get(ILLIWAP_AGENDA_PAGE_URL, text=self.listing)
        self.section.setLayout("table_view")
        html = queryMultiAdapter((self.page, self.request), name="full_view")()
        soup = BeautifulSoup(html)

        titles = [tag.text.strip() for tag in soup.select("div.table_title span")]
        self.assertEqual(
            titles, ["Enigm'Ha", "Guinguette de Fairon", "Marathon de l'Ourthe 2026"]
        )

        # the category comes from the agenda, not from a smartweb vocabulary
        categories = [
            tag.text.strip() for tag in soup.select("div.table_category span")
        ]
        self.assertEqual(categories, ["Animation", "Autres", "Sport"])

        # the thumbnail is the small media
        image = soup.select("div.table_display div.is-image")[0]
        self.assertIn("vignette_agenda_media_sm", image.get("style"))

        # each card links to its own page on illiwap, with the real slug
        # (illiwap suffixes duplicates, so it cannot be derived from the title)
        hrefs = [a.get("href") for a in soup.select("div.table_display a.table_image")]
        self.assertEqual(
            hrefs,
            [
                f"{ILLIWAP_AGENDA_PAGE_URL}enigm-ha-1",
                f"{ILLIWAP_AGENDA_PAGE_URL}guinguette-de-fairon-1",
                f"{ILLIWAP_AGENDA_PAGE_URL}marathon-de-l-ourthe-2026",
            ],
        )

    @requests_mock.Mocker()
    def test_event_date_macro_is_fed(self, m):
        """A multi day event renders a start and an end, a single day one does
        not : that is what the shared event_date macro does with our datetimes.
        """
        m.get(ILLIWAP_AGENDA_URL, json=self.agenda)
        m.get(ILLIWAP_AGENDA_PAGE_URL, text=self.listing)
        self.section.setLayout("table_view")
        html = queryMultiAdapter((self.page, self.request), name="full_view")()
        soup = BeautifulSoup(html)

        # Enigm'Ha runs from 05/07 to 23/08
        multi = soup.select("div.table_display")[0]
        self.assertEqual(multi.select("div.start_date span.day")[0].text, "05")
        self.assertEqual(multi.select("div.start_date span.month")[0].text, "07")
        self.assertEqual(multi.select("div.end_date span.day")[0].text, "23")
        self.assertEqual(multi.select("div.end_date span.month")[0].text, "08")

        # the Guinguette is a single day event
        single = soup.select("div.table_display")[1]
        self.assertEqual(single.select("div.start_date"), [])
        self.assertEqual(single.select("div.day_date span.day")[0].text, "12")
        self.assertEqual(single.select("div.day_date span.month")[0].text, "09")

    @requests_mock.Mocker()
    def test_see_all_link_is_opt_in(self, m):
        m.get(ILLIWAP_AGENDA_URL, json=self.agenda)
        m.get(ILLIWAP_AGENDA_PAGE_URL, text=self.listing)
        self.section.setLayout("table_view")

        # no link_text in the params, no link
        html = queryMultiAdapter((self.page, self.request), name="full_view")()
        self.assertEqual(BeautifulSoup(html).select("div.see_all"), [])

        self.section.external_content_params = '{"link_text": "Voir tout l\'agenda"}'
        html = queryMultiAdapter((self.page, self.request), name="full_view")()
        link = BeautifulSoup(html).select("div.see_all a")[0]
        self.assertEqual(link.text.strip(), "Voir tout l'agenda")
        self.assertEqual(link.get("href"), ILLIWAP_AGENDA_PAGE_URL)

    @requests_mock.Mocker()
    def test_carousel_view_renders_the_events(self, m):
        m.get(ILLIWAP_AGENDA_URL, json=self.agenda)
        m.get(ILLIWAP_AGENDA_PAGE_URL, text=self.listing)
        self.section.setLayout("carousel_view")
        html = queryMultiAdapter((self.page, self.request), name="full_view")()
        soup = BeautifulSoup(html)
        titles = [tag.text.strip() for tag in soup.select("div.swiper_title h3")]
        self.assertEqual(len(titles), 3)
        self.assertEqual(len(soup.select("a.swiper_link")), 3)

    @requests_mock.Mocker()
    def test_editor_is_warned_when_agenda_is_unavailable(self, m):
        m.get(ILLIWAP_AGENDA_URL, status_code=400)
        view = queryMultiAdapter((self.section, self.request), name="table_view")
        self.assertEqual(view.items, [])
        self.assertIn("Illiwap content is currently unavailable", view.issue)


class TestArcgisHeaderViewlet(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def _make_viewlet(self, view=None):
        return ArcgisHeaderViewlet(self.portal, self.request, view or MagicMock(), None)

    def test_update_calls_parent_and_sets_setheader(self):
        """update() delegates to parent which binds self.setHeader from the response."""
        viewlet = self._make_viewlet()
        viewlet.update()
        self.assertTrue(hasattr(viewlet, "setHeader"))
        self.assertEqual(viewlet.setHeader, self.request.response.setHeader)

    def test_update_sets_portal_state(self):
        """update() runs ViewletBase.update() which sets portal_state."""
        viewlet = self._make_viewlet()
        viewlet.update()
        self.assertTrue(hasattr(viewlet, "portal_state"))


class TestOdwbWidgetHeaderViewlet(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def _make_viewlet(self, view=None):
        return OdwbWidgetHeaderViewlet(
            self.portal, self.request, view or MagicMock(), None
        )

    # --- should_render ---

    def test_should_render_false_when_view_has_no_attribute(self):
        view = MagicMock(spec=[])  # no attributes → hasattr returns False
        viewlet = self._make_viewlet(view=view)
        self.assertFalse(viewlet.should_render())

    def test_should_render_returns_true_when_view_attribute_is_true(self):
        view = MagicMock()
        view.should_display_odwb_widget_viewlet = True
        viewlet = self._make_viewlet(view=view)
        self.assertTrue(viewlet.should_render())

    def test_should_render_returns_false_when_view_attribute_is_false(self):
        view = MagicMock()
        view.should_display_odwb_widget_viewlet = False
        viewlet = self._make_viewlet(view=view)
        self.assertFalse(viewlet.should_render())

    # --- render ---

    def test_render_calls_index_and_returns_its_result(self):
        viewlet = self._make_viewlet()
        viewlet.index = MagicMock(return_value="<script>odwb</script>")
        result = viewlet.render()
        viewlet.index.assert_called_once()
        self.assertEqual(result, "<script>odwb</script>")

    def test_render_calls_index_even_when_should_render_is_false(self):
        """render() always calls index() — the should_render() guard is commented out."""
        view = MagicMock(spec=[])  # should_render() would return False
        viewlet = self._make_viewlet(view=view)
        self.assertFalse(viewlet.should_render())
        viewlet.index = MagicMock(return_value="output")
        result = viewlet.render()
        viewlet.index.assert_called_once()
        self.assertEqual(result, "output")


# ---------------------------------------------------------------------------
# Pure unit tests (no Plone layer needed)
# ---------------------------------------------------------------------------


class TestBasePlugin(unittest.TestCase):
    def test_contents_returns_empty_string(self):
        plugin = BasePlugin()
        self.assertEqual(plugin.contents, "")


class TestPluginMatching(unittest.TestCase):
    """Direct unit tests for each plugin's __call__ matching logic."""

    def _call(self, plugin, url, config=None):
        return plugin(urlparse(url), config or {})

    # --- EaglebePlugin ---

    def test_eaglebe_matches_eaglebe_url(self):
        p = EaglebePlugin()
        result = self._call(p, "https://app.eaglebe.com/auth/start", {"width": "100%"})
        self.assertIs(result, p)

    def test_eaglebe_returns_none_for_other_url(self):
        p = EaglebePlugin()
        self.assertIsNone(self._call(p, "https://kamoulox.be"))

    # --- EllohaPlugin ---

    def test_elloha_matches_elloha_url(self):
        p = EllohaPlugin()
        config = {"current_lang": "fr", "extra_params": None}
        result = self._call(
            p, "https://reservation.elloha.com/Scripts/widget-loader.min.js", config
        )
        self.assertIs(result, p)

    def test_elloha_returns_none_for_other_url(self):
        p = EllohaPlugin()
        self.assertIsNone(self._call(p, "https://kamoulox.be"))

    # --- CognitoformPlugin ---

    def test_cognitoform_matches_cognitoforms_url(self):
        p = CognitoformPlugin()
        config = {"current_lang": "fr", "extra_params": None, "width": "100%"}
        result = self._call(p, "https://www.cognitoforms.com/Org/Form", config)
        self.assertIs(result, p)

    def test_cognitoform_returns_none_for_other_url(self):
        p = CognitoformPlugin()
        self.assertIsNone(self._call(p, "https://kamoulox.be"))

    # --- ArcgisPlugin ---

    def test_arcgis_matches_arcgis_url(self):
        p = ArcgisPlugin()
        config = {
            "current_lang": "fr",
            "extra_params": None,
            "url": "http://localhost",
        }
        result = self._call(p, "https://www.arcgis.com/apps/mapviewer/", config)
        self.assertIs(result, p)

    def test_arcgis_returns_none_for_other_url(self):
        p = ArcgisPlugin()
        self.assertIsNone(self._call(p, "https://kamoulox.be"))

    # --- GiveADayPlugin ---

    def test_giveaday_matches_giveaday_url(self):
        p = GiveADayPlugin()
        result = self._call(p, "https://www.giveaday.be/campaign/123")
        self.assertIs(result, p)

    def test_giveaday_returns_none_for_other_url(self):
        p = GiveADayPlugin()
        self.assertIsNone(self._call(p, "https://kamoulox.be"))

    # --- IdeluxWastePlugin ---

    def test_idelux_waste_matches_odwb_guide_de_tri_url(self):
        p = IdeluxWastePlugin()
        url = "https://www.odwb.be/api/explore/v2.1/catalog/datasets/guide-de-tri1/records"
        result = self._call(p, url)
        self.assertIs(result, p)

    def test_idelux_waste_returns_none_for_non_matching_path(self):
        p = IdeluxWastePlugin()
        url = "https://www.odwb.be/api/explore/v2.1/catalog/datasets/other-dataset/records"
        self.assertIsNone(self._call(p, url))

    def test_idelux_waste_returns_none_for_non_odwb_host(self):
        p = IdeluxWastePlugin()
        self.assertIsNone(self._call(p, "https://kamoulox.be/guide-de-tri1"))

    # --- InbwContainersAffluencePlugin ---

    def test_inbw_affluence_matches_odwb_affluence_url(self):
        p = InbwContainersAffluencePlugin()
        url = "https://www.odwb.be/api/explore/v2.1/catalog/datasets/affluence/records"
        result = self._call(p, url)
        self.assertIs(result, p)

    def test_inbw_affluence_returns_none_for_non_matching_path(self):
        p = InbwContainersAffluencePlugin()
        url = "https://www.odwb.be/api/explore/v2.1/catalog/datasets/other/records"
        self.assertIsNone(self._call(p, url))

    # --- OdwbWidgetPlugin ---

    def test_odwb_widget_matches_opendatasoft_url(self):
        p = OdwbWidgetPlugin()
        config = {"extra_params": "<ods-dataset-context>...</ods-dataset-context>"}
        result = self._call(
            p, "https://static.opendatasoft.com/ods-widgets/my-widget", config
        )
        self.assertIs(result, p)

    def test_odwb_widget_sets_is_odwb_widget_plugins_true_on_match(self):
        p = OdwbWidgetPlugin()
        config = {"extra_params": "html"}
        self._call(p, "https://static.opendatasoft.com/ods-widgets/widget", config)
        self.assertTrue(p.is_odwb_widget_plugins)

    def test_odwb_widget_returns_none_for_other_url(self):
        p = OdwbWidgetPlugin()
        self.assertIsNone(self._call(p, "https://kamoulox.be"))

    # --- UnknowServicePlugin ---

    def test_unknow_service_always_returns_self(self):
        p = UnknowServicePlugin()
        result = self._call(p, "https://kamoulox.be", {"current_lang": "fr"})
        self.assertIs(result, p)


class TestTimeoutHandling(unittest.TestCase):
    """Timeout exception branches in IdeluxWastePlugin and InbwContainersAffluencePlugin."""

    def test_idelux_waste_contents_returns_none_on_timeout(self):
        plugin = IdeluxWastePlugin()
        url = "https://www.odwb.be/api/explore/v2.1/catalog/datasets/guide-de-tri1/records"
        plugin.parts = urlparse(url)
        plugin.url = url  # referenced in logger.warning inside except block
        plugin.config = {}
        with patch(f"{_VIEWS_MODULE}.requests.get") as mock_get:
            mock_get.side_effect = requests.exceptions.Timeout
            result = plugin.contents
        self.assertIsNone(result)

    def test_inbw_affluence_contents_returns_none_on_timeout(self):
        plugin = InbwContainersAffluencePlugin()
        url = "https://www.odwb.be/api/explore/v2.1/catalog/datasets/affluence/records"
        plugin.parts = urlparse(url)
        plugin.url = url  # referenced in logger.warning inside except block
        plugin.config = {}
        with patch(f"{_VIEWS_MODULE}.requests.get") as mock_get:
            mock_get.side_effect = requests.exceptions.Timeout
            result = plugin.contents
        self.assertIsNone(result)


class TestArcgisView(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]

    def test_get_portal_item_id_reads_from_request(self):
        self.request.portal_item_id = "27a432b0835149e6acd3ac39d0e4349c"
        view = ArcgisView(self.portal, self.request)
        self.assertEqual(view.get_portal_item_id, "27a432b0835149e6acd3ac39d0e4349c")


class TestExternalContentViewExtra(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            id="page",
        )

    def _make_section_view(self, url="https://kamoulox.be"):
        sec = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionExternalContent",
            id="sec",
        )
        sec.external_content_url = url
        return queryMultiAdapter((sec, self.request), name="view")

    def test_has_leadimage_returns_true_when_context_has_image(self):
        section_view = self._make_section_view()
        with patch(f"{_VIEWS_MODULE}.ILeadImage") as mock_lead:
            mock_lead.providedBy.return_value = True
            section_view.context.image = object()  # any truthy value
            result = section_view.has_leadimage()
        self.assertTrue(result)

    def test_render_viewlet_calls_index_and_returns_result(self):
        section_view = self._make_section_view()
        section_view.index = MagicMock(return_value="<div>section</div>")
        result = section_view.render_viewlet()
        section_view.index.assert_called_once()
        self.assertEqual(result, "<div>section</div>")
