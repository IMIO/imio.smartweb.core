# -*- coding: utf-8 -*-
# imio/smartweb/core/browser/categorization_button_edit.py

from imio.smartweb.core.browser.forms import SmartwebCustomEditForm
from plone.z3cform import layout

from zope import schema
from z3c.form.interfaces import DISPLAY_MODE, HIDDEN_MODE
from z3c.form.widget import FieldWidget
from z3c.form import widget as z3c_widget
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile


FIELD_NAME = "categorization_ia_link"  # identifiant interne pour le faux champ


class HtmlSnippetWidget(z3c_widget.Widget):
    """Widget HTML (bouton + JS) avec template ZPT."""

    template = ViewPageTemplateFile("html_snippet_widget.pt")

    def update(self):
        # En edit, context == objet
        base = self.context.absolute_url()
        self.endpoint = f"{base}/@@ProcessCategorizeContent"
        # id unique pour le bouton + zone de statut
        self.wid = getattr(self, "name", FIELD_NAME)

    def render(self):
        return self.template()


class PageEditForm(SmartwebCustomEditForm):
    """Vue edit custom, avec bouton 'Catégoriser' injecté en haut de 'categorization'."""

    def update(self):
        super(PageEditForm, self).update()

        # 1) Ta logique existante : cacher hide_title dans le group 'layout'
        for group in getattr(self, "groups", []):
            if (
                getattr(group, "__name__", "") == "layout"
                and "hide_title" in group.widgets
            ):
                group.widgets["hide_title"].mode = HIDDEN_MODE
                group.widgets["hide_title"].value = ["selected"]

        # 2) Injecter le bouton en haut du fieldset 'categorization'
        #    (on travaille sur les widgets *instanciés*)
        if not getattr(self, "groups", None):
            return

        # Trouver le groupe 'categorization'
        cat = next(
            (g for g in self.groups if getattr(g, "__name__", "") == "categorization"),
            None,
        )
        if not cat or not getattr(cat, "widgets", None):
            return

        # Eviter doublons : si déjà présent, on stoppe
        existing_keys = list(getattr(cat.widgets, "keys", lambda: [])())
        for k in existing_keys:
            if (
                k.endswith(FIELD_NAME)
                or k == FIELD_NAME
                or k.endswith(f"form.widgets.{FIELD_NAME}")
            ):
                return

        # Créer un 'champ' factice sans label/description + FieldWidget(HtmlSnippetWidget)
        zfield = schema.Text(__name__=FIELD_NAME, title="", description="")
        w = FieldWidget(zfield, HtmlSnippetWidget(self.request))
        w.mode = DISPLAY_MODE
        w.context = self.context
        w.form = self
        w.ignoreContext = True
        w.label = ""
        w.update()  # prépare endpoint/wid

        # Insérer tout en HAUT du manager (clé varie selon versions)
        key = f"form.widgets.{FIELD_NAME}"

        # 2.1) si le manager expose la structure interne (_data_keys/_widgets)
        if hasattr(cat.widgets, "_data_keys") and hasattr(cat.widgets, "_widgets"):
            # supprimer occurrences résiduelles
            try:
                while key in cat.widgets._data_keys:
                    idx = cat.widgets._data_keys.index(key)
                    cat.widgets._data_keys.pop(idx)
                    cat.widgets._widgets.pop(idx)
            except Exception:
                pass
            # pré-insertion en tête
            cat.widgets._data_keys.insert(0, key)
            cat.widgets._widgets.insert(0, w)
            return

        # 2.2) fallback : reconstruire le mapping avec notre widget en premier
        try:
            existing = [(k, cat.widgets[k]) for k in list(cat.widgets.keys())]
            try:
                cat.widgets.clear()
            except Exception:
                pass
            # notre widget d'abord
            cat.widgets[key] = w
            # puis les autres
            for k, ww in existing:
                if k != key:
                    cat.widgets[k] = ww
        except Exception:
            # dernier recours : si rien d'autre n'a marché
            try:
                cat.widgets[key] = w
            except Exception:
                pass


PageEditView = layout.wrap_form(PageEditForm)
