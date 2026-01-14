from imio.smartweb.common.ia.browser.views import BaseProcessCategorizeContentView
from imio.smartweb.core.contents import IPages
from imio.smartweb.core.contents import ISectionText
from imio.smartweb.core.utils import get_categories


class ProcessCategorizeContentView(BaseProcessCategorizeContentView):

    def _get_all_text(self):
        all_text = ""
        if IPages.providedBy(self.context):
            for _id, obj in self.context.objectItems():
                if ISectionText.providedBy(obj):
                    all_text += " " + getattr(obj.text, "output", "")
        return all_text.strip()

    def _process_specific(self, all_text, results):
        """Must be impleted"""
        ia_categories = self._process_category(all_text, results)
        results["form-widgets-page_category-taxonomy_page_category"] = ia_categories
        return results

    def _process_category(self, all_text, results):
        # If agent doesn't register prevsouly a categorization so IA can bring categorization
        if self.context.taxonomy_page_category is None:
            categories_taxo = get_categories()
            categories_voca = categories_taxo.makeVocabulary(self.current_lang).inv_data
            categories_voc = [
                {"title": v, "token": k} for k, v in categories_voca.items()
            ]
            data = self._ask_categorization_to_ia(all_text, categories_voc)
            if not data:
                return ""
            ia_categories = [
                {"title": r.get("title"), "token": r.get("token")}
                for r in data.get("result")
            ]
            return ia_categories
