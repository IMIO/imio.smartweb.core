# -*- coding: utf-8 -*-

from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import queryMultiAdapter


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

    def test_unknow_service(self):
        sec = api.content.create(
            container=self.page, type="imio.smartweb.SectionExternalContent", id="sec"
        )
        sec.external_content_url = "https://kamoulox.be"
        section_view = queryMultiAdapter((sec, self.request), name="view")
        self.assertEqual(
            section_view.get_embed_external_content(),
            '<p class="unknow_service">Unknow service</p>',
        )

    # def test_eaglebe_plugin(self):
    #     sec = api.content.create(
    #         container=self.page, type="imio.smartweb.SectionExternalContent", id="sec"
    #     )

    #     sec.external_content_url = ""
    #     section_view = queryMultiAdapter((sec, self.request), name="view")
    #     self.assertEqual(
    #         section_view.get_embed_external_content(),
    #         '<p class="unknow_service">Unknow service</p>',
    #     )

    #     sec.external_content_url = "https://app.eaglebe.com/auth/start"
    #     section_view = queryMultiAdapter((sec, self.request), name="view")
    #     self.assertEqual(
    #         section_view.get_embed_external_content(),
    #         '<iframe class="eaglebe" src="https://app.eaglebe.com/auth/start" scrolling="no" width="100%">',
    #     )

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
            section_view.get_embed_external_content(),
            '<div class="elloha elloha_error">With an elloha plugin, extra params must contain a dictionary with two keys : ConstellationWidgetContainer, Idoi</div>',
        )

        # with good extra params
        sec.external_content_params = """{
            "ConstellationWidgetContainer" : "11111111-1111-1111-1111-111111111111",
            "Idoi" : "22222222-2222-2222-2222-222222222222"
        }"""
        section_view = queryMultiAdapter((sec, self.request), name="view")
        result = '<div class="elloha"><div id="ConstellationWidgetContainer11111111-1111-1111-1111-111111111111" style="width:100%" data-id-projet="11111111111111111111111111111111">...</div></div><script type="text/javascript" src="https://reservation.elloha.com/Scripts/widget-loader.min.js?v=42/Scripts/widget-loader.min.js?v=42"></script><script type="text/javascript">var constellationWidgetUrl11111111111111111111111111111111, constellationTypeModule11111111111111111111111111111111;constellationWidgetUrl11111111111111111111111111111111 = "https://reservation.elloha.com/Widget/BookingEngine/11111111-1111-1111-1111-111111111111?idoi=22222222-2222-2222-2222-222222222222&culture=fr-FR";constellationTypeModule11111111111111111111111111111111=1; constellationWidgetLoad("ConstellationWidgetContainer11111111-1111-1111-1111-111111111111");constellationWidgetAddEvent(window, "resize", function () {constellationWidgetSetAppearance("ConstellationWidgetContainer11111111-1111-1111-1111-111111111111");});</script>'
        self.assertEqual(section_view.get_embed_external_content(), result)

        # good extra params / dict keys are case insensitive
        sec.external_content_params = """{
            "CONSTELLATIONWIDGETCONTAINER" : "11111111-1111-1111-1111-111111111111",
            "IDOI" : "22222222-2222-2222-2222-222222222222"
        }"""
        section_view = queryMultiAdapter((sec, self.request), name="view")
        result = '<div class="elloha"><div id="ConstellationWidgetContainer11111111-1111-1111-1111-111111111111" style="width:100%" data-id-projet="11111111111111111111111111111111">...</div></div><script type="text/javascript" src="https://reservation.elloha.com/Scripts/widget-loader.min.js?v=42/Scripts/widget-loader.min.js?v=42"></script><script type="text/javascript">var constellationWidgetUrl11111111111111111111111111111111, constellationTypeModule11111111111111111111111111111111;constellationWidgetUrl11111111111111111111111111111111 = "https://reservation.elloha.com/Widget/BookingEngine/11111111-1111-1111-1111-111111111111?idoi=22222222-2222-2222-2222-222222222222&culture=fr-FR";constellationTypeModule11111111111111111111111111111111=1; constellationWidgetLoad("ConstellationWidgetContainer11111111-1111-1111-1111-111111111111");constellationWidgetAddEvent(window, "resize", function () {constellationWidgetSetAppearance("ConstellationWidgetContainer11111111-1111-1111-1111-111111111111");});</script>'
        self.assertEqual(section_view.get_embed_external_content(), result)

        # with bad params
        sec.external_content_params = "kamoulox"
        section_view = queryMultiAdapter((sec, self.request), name="view")
        result = '<div class="elloha elloha_error">With an elloha plugin, extra params must contain a dictionary with two keys : ConstellationWidgetContainer, Idoi</div>'
        self.assertEqual(section_view.get_embed_external_content(), result)

        sec.external_content_params = """{
            "ConstellationWidgetContainer" : "11111111-1111-1111-1111-111111111111"
        }"""
        section_view = queryMultiAdapter((sec, self.request), name="view")
        result = '<div class="elloha elloha_error">With an elloha plugin, extra params must contain a dictionary with two keys : ConstellationWidgetContainer, Idoi</div>'
        self.assertEqual(section_view.get_embed_external_content(), result)

        sec.external_content_params = """{
            "CONSTELLATIONWIDGETCONTAINER" : "11111111-1111-1111-1111-111111111111",
            "IDOI" : "22222222-2222-2222-2222-222222222222"
        """
        section_view = queryMultiAdapter((sec, self.request), name="view")
        result = '<div class="elloha elloha_error">With an elloha plugin, extra params must contain a dictionary with two keys : ConstellationWidgetContainer, Idoi</div>'
        self.assertEqual(section_view.get_embed_external_content(), result)
