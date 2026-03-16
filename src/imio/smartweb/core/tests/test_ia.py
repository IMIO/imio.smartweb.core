# -*- coding: utf-8 -*-

from imio.smartweb.core.browser.ia.ia import ProcessCategorizeContentView
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.textfield.value import RichTextValue
from unittest.mock import MagicMock
from unittest.mock import patch

import json


_IA_MODULE = "imio.smartweb.core.browser.ia.ia"


class TestProcessCategorizeContentView(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="A Page",
        )

    def _make_view(self, context=None):
        if context is None:
            context = self.page
        return ProcessCategorizeContentView(context, self.request)

    def _mock_taxonomy(self, inv_data=None):
        """Return a mock ITaxonomy with given inv_data dict."""
        if inv_data is None:
            inv_data = {"publication": "Publication", "actualites": "Actualités"}
        mock_taxo = MagicMock()
        mock_taxo.makeVocabulary.return_value.inv_data = inv_data
        return mock_taxo

    # --- _get_all_text: IPages branch ---

    def test_get_all_text_empty_for_page_with_no_sections(self):
        view = self._make_view()
        self.assertEqual(view._get_all_text(), "")

    def test_get_all_text_collects_section_text_output(self):
        section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionText",
            title="Section",
        )
        section.text = RichTextValue("<p>Kamoulox</p>", "text/html", "text/html")
        view = self._make_view()
        result = view._get_all_text()
        self.assertIn("Kamoulox", result)

    def test_get_all_text_ignores_non_text_sections(self):
        api.content.create(
            container=self.page,
            type="imio.smartweb.SectionFiles",
            title="Files",
        )
        view = self._make_view()
        self.assertEqual(view._get_all_text(), "")

    def test_get_all_text_concatenates_multiple_text_sections(self):
        for i in range(2):
            section = api.content.create(
                container=self.page,
                type="imio.smartweb.SectionText",
                title=f"Section {i}",
            )
            section.text = RichTextValue(f"<p>Part{i}</p>", "text/html", "text/html")
        view = self._make_view()
        result = view._get_all_text()
        self.assertIn("Part0", result)
        self.assertIn("Part1", result)

    # --- _get_all_text: non-IPages (BODY) branch ---

    def test_get_all_text_from_body_returns_form_title(self):
        body = json.dumps({"formdata": {"form-widgets-IBasic-title": "Test Title"}})
        view = self._make_view(context=self.portal)
        with patch.object(self.request, "get", return_value=body):
            result = view._get_all_text()
        self.assertEqual(result, "Test Title")

    def test_get_all_text_from_body_returns_empty_when_title_missing(self):
        body = json.dumps({"formdata": {}})
        view = self._make_view(context=self.portal)
        with patch.object(self.request, "get", return_value=body):
            result = view._get_all_text()
        self.assertEqual(result, "")

    # --- _process_category ---

    def test_process_category_returns_empty_string_when_ia_returns_nothing(self):
        view = self._make_view()
        with patch(f"{_IA_MODULE}.get_categories", return_value=self._mock_taxonomy()):
            with patch.object(view, "_ask_categorization_to_ia", return_value={}):
                result = view._process_category("some text", {})
        self.assertEqual(result, "")

    def test_process_category_returns_categories_from_ia(self):
        view = self._make_view()
        ia_data = {"result": [{"title": "Publication", "token": "publication"}]}
        with patch(f"{_IA_MODULE}.get_categories", return_value=self._mock_taxonomy()):
            with patch.object(view, "_ask_categorization_to_ia", return_value=ia_data):
                result = view._process_category("some text", {})
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["token"], "publication")
        self.assertEqual(result[0]["title"], "Publication")

    def test_process_category_returns_none_when_context_already_has_category(self):
        self.page.taxonomy_page_category = "publication"
        view = self._make_view()
        result = view._process_category("some text", {})
        self.assertIsNone(result)

    def test_process_category_builds_vocab_from_taxonomy_inv_data(self):
        """The vocabulary passed to the IA must reflect the taxonomy inv_data."""
        view = self._make_view()
        inv_data = {"token1": "Title1", "token2": "Title2"}
        captured_voc = []

        def capture_voc(text, voc):
            captured_voc.extend(voc)
            return {}

        with patch(
            f"{_IA_MODULE}.get_categories", return_value=self._mock_taxonomy(inv_data)
        ):
            with patch.object(
                view, "_ask_categorization_to_ia", side_effect=capture_voc
            ):
                view._process_category("text", {})

        tokens = {item["token"] for item in captured_voc}
        self.assertIn("token1", tokens)
        self.assertIn("token2", tokens)

    # --- _process_specific ---

    def test_process_specific_sets_taxonomy_page_category_key(self):
        view = self._make_view()
        with patch.object(view, "_process_category", return_value=[{"token": "x"}]):
            results = {}
            returned = view._process_specific("text", results)
        self.assertIn("form-widgets-page_category-taxonomy_page_category", returned)
        self.assertEqual(
            returned["form-widgets-page_category-taxonomy_page_category"],
            [{"token": "x"}],
        )

    def test_process_specific_returns_results(self):
        view = self._make_view()
        with patch.object(view, "_process_category", return_value=""):
            results = {"existing": "value"}
            returned = view._process_specific("text", results)
        self.assertIsNotNone(returned)
        self.assertIn("existing", returned)

    # --- __call__ ---

    def test_call_returns_valid_json(self):
        view = self._make_view()
        with patch(f"{_IA_MODULE}.get_categories", return_value=self._mock_taxonomy()):
            with patch.object(view, "_ask_categorization_to_ia", return_value={}):
                raw = view()
        result = json.loads(raw)
        self.assertTrue(result["ok"])
        self.assertEqual(result["message"], "Catégorisation calculée")
        self.assertIn("data", result)

    def test_call_data_includes_taxonomy_page_category_key(self):
        view = self._make_view()
        ia_data = {"result": [{"title": "Publication", "token": "publication"}]}
        with patch(f"{_IA_MODULE}.get_categories", return_value=self._mock_taxonomy()):
            with patch.object(view, "_ask_categorization_to_ia", return_value=ia_data):
                result = json.loads(view())
        self.assertIn(
            "form-widgets-page_category-taxonomy_page_category", result["data"]
        )
