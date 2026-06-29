from imio.smartweb.common.ia.browser.views import BaseProcessCategorizeContentView
from imio.smartweb.core.contents import IPages
from imio.smartweb.core.contents import ISectionText
from imio.smartweb.core.utils import get_categories

import json


class ProcessCategorizeContentView(BaseProcessCategorizeContentView):

    def _get_all_text(self):
        all_text = ""
        if IPages.providedBy(self.context):
            for _id, obj in self.context.objectItems():
                if ISectionText.providedBy(obj):
                    all_text += " " + getattr(obj.text, "output", "")
        else:
            # We don't have context so we're in ++add++
            # Need to get page title on request
            raw = self.request.get("BODY")
            data = json.loads(raw)
            all_text = data.get("formdata").get("form-widgets-IBasic-title", "")
        return all_text.strip()

    def _process_specific(self, all_text, results):
        """Add the IA-suggested page category to the results."""
        results["form-widgets-page_category-taxonomy_page_category"] = (
            self._process_category(all_text)
        )
        return results

    def _process_category(self, all_text):
        # Only let the IA suggest a category when none has been set yet.
        # In ++add++ the context is the container (a Plone folder) which has no
        # taxonomy_page_category attribute, so the IA always runs in that case.
        if getattr(self.context, "taxonomy_page_category", None) is not None:
            return None

        categories = get_categories().makeVocabulary(self.current_lang).inv_data
        categories_voc = [
            {"title": title, "token": token} for token, title in categories.items()
        ]
        data = self._ask_categorization_to_ia(all_text, categories_voc)
        if not data:
            return ""
        return [
            {"title": r.get("title"), "token": r.get("token")}
            for r in data.get("result")
        ]
