from imio.smartweb.common.browser.forms import CustomAddForm
from imio.smartweb.common.config import APPLICATION_ID
from imio.smartweb.common.config import PROJECT_ID
from plone.dexterity.browser.add import DefaultAddView

from z3c.form.interfaces import HIDDEN_MODE, DISPLAY_MODE
from z3c.form.widget import FieldWidget
from z3c.form import widget as z3c_widget
from zope import schema
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile


FIELD_NAME = "categorization_ia_link"


class HtmlSnippetWidget(z3c_widget.Widget):
    template = ViewPageTemplateFile("html_snippet_widget.pt")
    x_imio_application = APPLICATION_ID
    x_imio_municipality = PROJECT_ID

    def update(self):
        # ++add++ : context = container ; edit : context = object
        base = self.context.absolute_url()
        self.endpoint = f"{base}/@@ProcessCategorizeContent"
        self.wid = getattr(self, "name", "categorization_ia_link")

    def render(self):
        return self.template()


class PageAddForm(CustomAddForm):
    portal_type = "imio.smartweb.Page"

    def update(self):
        super(PageAddForm, self).update()

        for group in self.groups:
            if getattr(group, "__name__", "") == "layout":
                if "hide_title" in group.widgets:
                    group.widgets["hide_title"].mode = HIDDEN_MODE
                    group.widgets["hide_title"].value = ["selected"]

        # 2) Inject HTML button in "categorization" group
        if not getattr(self, "groups", None):
            self.updateGroups()

        cat = next(
            (g for g in self.groups if getattr(g, "__name__", "") == "categorization"),
            None,
        )
        if not cat or not getattr(cat, "widgets", None):
            return

        # Avoid doublons (refresh)
        for k in getattr(cat.widgets, "keys", lambda: [])():
            if k.endswith(FIELD_NAME) or k == FIELD_NAME:
                return

        # Create dummy field + FieldWidget(HtmlSnippetWidget)
        zfield = schema.Text(__name__=FIELD_NAME, title="", description="")
        w = FieldWidget(zfield, HtmlSnippetWidget(self.request))
        w.mode = DISPLAY_MODE
        w.context = self.context  # conteneur du futur objet
        w.form = self
        w.ignoreContext = True
        w.label = ""
        w.update()

        try:
            cat.widgets[f"form.widgets.{FIELD_NAME}"] = w
        except Exception:
            try:
                cat.widgets[FIELD_NAME] = w
            except Exception:
                # Fallback bas niveau si nécessaire
                if hasattr(cat.widgets, "_data_keys") and hasattr(
                    cat.widgets, "_widgets"
                ):
                    cat.widgets._data_keys.append(FIELD_NAME)
                    cat.widgets._widgets.append(w)


class PagesAddView(DefaultAddView):
    form = PageAddForm
