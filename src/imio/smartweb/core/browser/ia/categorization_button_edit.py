# -*- coding: utf-8 -*-
# imio/smartweb/core/browser/categorization_button_edit.py
from imio.smartweb.common.config import APPLICATION_ID
from imio.smartweb.common.config import PROJECT_ID
from imio.smartweb.core.browser.forms import SmartwebCustomEditForm
from imio.smartweb.core.contents import ISectionText

from plone.z3cform import layout

from zope import schema
from z3c.form.interfaces import DISPLAY_MODE, HIDDEN_MODE
from z3c.form.widget import FieldWidget
from z3c.form import widget as z3c_widget
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile


FIELD_NAME = "categorization_ia_link"  # Internal id for dummy field


class HtmlSnippetWidget(z3c_widget.Widget):
    """Widget HTML (bouton + JS) avec template ZPT."""

    template = ViewPageTemplateFile("html_snippet_widget.pt")
    x_imio_application = APPLICATION_ID
    x_imio_municipality = PROJECT_ID

    def update(self):
        # edit : context == objet
        base = self.context.absolute_url()
        self.endpoint = f"{base}/@@ProcessCategorizeContent"
        # Unique id for button + status zone
        self.wid = getattr(self, "name", FIELD_NAME)

        # Désactiver le bouton si aucune section texte avec contenu n'est présente
        self.klass = getattr(self, "klass", "")
        has_text_content = False

        # Vérifie si le contexte contient au moins une section texte avec du contenu
        try:
            for item in getattr(self.context, "objectItems", lambda: [])():
                obj = item[1]
                if ISectionText.providedBy(obj):
                    # Vérifier si la section texte a du contenu (non vide)
                    text_output = getattr(getattr(obj, "text", None), "output", "")
                    if text_output and text_output.strip():
                        has_text_content = True
                        break
        except Exception:
            pass

        if not has_text_content:
            self.klass = f"{self.klass} disabled".strip() if self.klass else "disabled"
            self.is_disabled = True
        else:
            self.is_disabled = False

    def render(self):
        return self.template()


class PageEditForm(SmartwebCustomEditForm):
    """Vue edit custom, avec bouton 'Catégoriser' injecté en haut de 'categorization'."""

    def update(self):
        super(PageEditForm, self).update()

        # 1) Hide hide_title in 'layout' group
        for group in getattr(self, "groups", []):
            if (
                getattr(group, "__name__", "") == "layout"
                and "hide_title" in group.widgets
            ):
                group.widgets["hide_title"].mode = HIDDEN_MODE
                group.widgets["hide_title"].value = ["selected"]

        # 2) Inject button on top of 'categorization' fieldset
        if not getattr(self, "groups", None):
            return

        # Find 'categorization' group
        cat = next(
            (g for g in self.groups if getattr(g, "__name__", "") == "categorization"),
            None,
        )
        if not cat or not getattr(cat, "widgets", None):
            return

        # Avoid doublons (refresh) if already here => stop
        existing_keys = list(getattr(cat.widgets, "keys", lambda: [])())
        for k in existing_keys:
            if (
                k.endswith(FIELD_NAME)
                or k == FIELD_NAME
                or k.endswith(f"form.widgets.{FIELD_NAME}")
            ):
                return

        # Create dummy field + FieldWidget(HtmlSnippetWidget)
        zfield = schema.Text(__name__=FIELD_NAME, title="", description="")
        w = FieldWidget(zfield, HtmlSnippetWidget(self.request))
        w.mode = DISPLAY_MODE
        w.context = self.context
        w.form = self
        w.ignoreContext = True
        w.label = ""
        w.update()  # prépare endpoint/wid

        key = f"form.widgets.{FIELD_NAME}"

        if hasattr(cat.widgets, "_data_keys") and hasattr(cat.widgets, "_widgets"):
            # Remove residual occurrences
            try:
                while key in cat.widgets._data_keys:
                    idx = cat.widgets._data_keys.index(key)
                    cat.widgets._data_keys.pop(idx)
                    cat.widgets._widgets.pop(idx)
            except Exception:
                pass
            cat.widgets._data_keys.insert(0, key)
            cat.widgets._widgets.insert(0, w)
            return

        # fallback : rebuild mapping with our with our widget
        try:
            existing = [(k, cat.widgets[k]) for k in list(cat.widgets.keys())]
            try:
                cat.widgets.clear()
            except Exception:
                pass
            # Firstly, our widget
            cat.widgets[key] = w
            # Next...
            for k, ww in existing:
                if k != key:
                    cat.widgets[k] = ww
        except Exception:
            # Last resort: If nothing else worked
            try:
                cat.widgets[key] = w
            except Exception:
                pass


PageEditView = layout.wrap_form(PageEditForm)
