# -*- coding: utf-8 -*-

from imio.gdpr.browser.views import GDPRView as BaseGDPRView
from imio.smartweb.core.browser.gdpr import GDPRView
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from unittest.mock import MagicMock
from unittest.mock import patch


_GDPR_BASE_MODULE = "imio.gdpr.browser.views"


class TestGDPRView(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def _make_view(self, context=None):
        return GDPRView(context or self.portal, self.request)

    # --- hide_herobanner ---

    def test_hide_herobanner_is_true(self):
        view = self._make_view()
        self.assertTrue(view.hide_herobanner)

    # --- __call__ ---

    def test_call_delegates_to_parent(self):
        view = self._make_view()
        with patch.object(
            BaseGDPRView, "__call__", return_value="parent_result"
        ) as mock_call:
            result = view()
        mock_call.assert_called_once()
        self.assertEqual(result, "parent_result")

    def test_call_renders_index_when_no_gdpr_content_in_nav_root(self):
        """When the nav root has no GDPR content, the base class renders the template."""
        view = self._make_view()
        view.index = MagicMock(return_value="<html>GDPR text</html>")
        result = view()
        view.index.assert_called_once()
        self.assertEqual(result, "<html>GDPR text</html>")

    def test_call_redirects_when_gdpr_content_exists_in_nav_root(self):
        """When the nav root has a matching GDPR content object, the base class redirects."""
        view = self._make_view()
        expected_url = "http://localhost/gdpr-explanation"
        mock_content = MagicMock()
        mock_content.Language.return_value = self.portal.Language()
        mock_content.absolute_url.return_value = expected_url

        class MockNavRoot:
            def __getattr__(self, name):
                return mock_content

        with patch(
            f"{_GDPR_BASE_MODULE}.api.portal.get_navigation_root",
            return_value=MockNavRoot(),
        ):
            with patch.object(self.request.response, "redirect") as mock_redirect:
                view()

        mock_redirect.assert_called_once_with(expected_url)
