# -*- coding: utf-8 -*-

from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.widgets.frozen_label import FrozenLabelTextFieldWidget
from z3c.form.interfaces import NO_VALUE
from z3c.form.testing import TestRequest
from zope import schema


class TestFrozenLabelTextWidget(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def _make_widget(self, value):
        field = schema.TextLine(__name__="number", title="Number")
        widget = FrozenLabelTextFieldWidget(field, TestRequest())
        widget.name = "form.widgets.phones_display.0.widgets.number"
        widget.value = value
        return widget

    def test_render_shows_the_value_as_a_label(self):
        html = self._make_widget("+3287123456").render()
        self.assertIn('<span class="dgf-frozen-label">+3287123456</span>', html)

    def test_render_still_submits_the_value(self):
        # The whole point: a display-mode widget would emit nothing and
        # DictRow._validate would reject every row on save.
        html = self._make_widget("+3287123456").render()
        self.assertIn('type="hidden"', html)
        self.assertIn('name="form.widgets.phones_display.0.widgets.number"', html)
        self.assertIn('value="+3287123456"', html)

    def test_render_escapes_html(self):
        html = self._make_widget("<script>alert(1)</script>").render()
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)

    def test_render_handles_missing_value(self):
        for empty in (None, NO_VALUE, ""):
            html = self._make_widget(empty).render()
            self.assertIn('<span class="dgf-frozen-label"></span>', html)
            self.assertIn('value=""', html)

    def test_render_handles_a_list_value(self):
        # A DataGrid feeds the sub-widget the RAW field value. Guard against a
        # list slipping in, otherwise value[0] on a string would render a
        # single stray character.
        html = self._make_widget(["work"]).render()
        self.assertIn('<span class="dgf-frozen-label">work</span>', html)
