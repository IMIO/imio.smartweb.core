# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.external_content.views import (
    IIdeluxWastePlugin,
)
from imio.smartweb.core.contents.sections.external_content.views import (
    IInbwContainersAffluencePlugin,
)
from imio.smartweb.core.contents.sections.external_content.views import (
    IOdwbWidgetPlugin,
)
from imio.smartweb.core.interfaces import IOdwbViewUtils
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import queryMultiAdapter

import requests_mock as requests_mock_module


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
