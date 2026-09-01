# -*- coding: utf-8 -*-

from collective.instancebehavior import enable_behaviors
from collective.taxonomy.exportimport import TaxonomyImportExportAdapter
from collective.taxonomy.factory import registerTaxonomy
from collective.taxonomy.interfaces import ITaxonomy
from imio.smartweb.core.browser.migration.taxonomy_mapping import AVISENQUETES_FIELD
from imio.smartweb.core.browser.migration.taxonomy_mapping import (
    PAGE_CATEGORY_TO_AVISENQUETES,
)
from imio.smartweb.core.browser.migration.taxonomy_mapping import (
    PAGE_CATEGORY_TO_REGLEMENTS,
)
from imio.smartweb.core.browser.migration.taxonomy_mapping import REGLEMENTS_FIELD
from imio.smartweb.core.browser.migration.taxonomy_mapping import (
    UNMAPPED_PAGE_CATEGORY_TERMS,
)
from imio.smartweb.core.interfaces import IImioSmartwebCoreLayer
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from zope.interface import alsoProvides

import os


class TestMigratePageCategory(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        alsoProvides(self.request, IImioSmartwebCoreLayer)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.folder = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            id="folder",
        )

    def install_taxonomy(self, short_name, title, single_select=True, on_fti=True):
        """Create a taxonomy and enable it on Page, as done through the web.

        ``on_fti=False`` reproduces the other through the web route: the
        taxonomy is created in the control panel but the behavior is turned on
        object by object with the "Taxonomies choices" form
        (collective.instancebehavior), never on the content type.
        """
        path = os.path.join(
            os.path.dirname(__file__), "resources", f"taxonomy_{short_name}.xml"
        )
        with open(path, "rb") as vdex:
            body = vdex.read()
        taxonomy = registerTaxonomy(
            self.portal, name=short_name, title=title, default_language="fr"
        )
        TaxonomyImportExportAdapter(self.portal).importDocument(taxonomy, body)
        taxonomy.registerBehavior(
            field_title=title,
            field_description="",
            default_language="fr",
            taxonomy_fieldset="categorization",
            is_single_select=single_select,
            is_required=False,
        )
        if on_fti:
            fti = self.portal.portal_types["imio.smartweb.Page"]
            fti.behaviors = tuple(fti.behaviors) + (taxonomy.getGeneratedName(),)
        return taxonomy

    def install_both_taxonomies(self, single_select=True, on_fti=True):
        self.install_taxonomy(
            "avisenquetes", "Types d'avis et enquêtes", single_select, on_fti
        )
        self.install_taxonomy(
            "reglements", "Types de règlements", single_select, on_fti
        )

    def create_page(self, page_id, page_category):
        page = api.content.create(
            container=self.folder,
            type="imio.smartweb.Page",
            id=page_id,
        )
        page.taxonomy_page_category = page_category
        page.reindexObject()
        return page

    def migrate(self, apply=True):
        self.request.form["apply"] = "1" if apply else "0"
        view = self.portal.restrictedTraverse("@@migrate_page_category")
        view()
        return view

    def taxonomy_values(self, taxonomy_name):
        sm = self.portal.getSiteManager()
        taxonomy = sm.queryUtility(ITaxonomy, name=taxonomy_name)
        return list(taxonomy.data["fr"].values())

    def test_mapping_targets_exist_in_new_taxonomies(self):
        """Every mapped identifier must be a real term of its new taxonomy."""
        self.install_both_taxonomies()
        avis = self.taxonomy_values("collective.taxonomy.avisenquetes")
        reglements = self.taxonomy_values("collective.taxonomy.reglements")
        for new_term in PAGE_CATEGORY_TO_AVISENQUETES.values():
            self.assertIn(new_term, avis)
        for new_term in PAGE_CATEGORY_TO_REGLEMENTS.values():
            self.assertIn(new_term, reglements)

    def test_mapping_has_no_duplicate(self):
        """An old term maps to one taxonomy only, a new term is used once."""
        self.assertFalse(
            set(PAGE_CATEGORY_TO_AVISENQUETES) & set(PAGE_CATEGORY_TO_REGLEMENTS)
        )
        self.assertFalse(
            set(PAGE_CATEGORY_TO_AVISENQUETES) & UNMAPPED_PAGE_CATEGORY_TERMS
        )
        self.assertFalse(
            set(PAGE_CATEGORY_TO_REGLEMENTS) & UNMAPPED_PAGE_CATEGORY_TERMS
        )
        self.assertEqual(
            len(set(PAGE_CATEGORY_TO_AVISENQUETES.values())),
            len(PAGE_CATEGORY_TO_AVISENQUETES),
        )
        self.assertEqual(
            len(set(PAGE_CATEGORY_TO_REGLEMENTS.values())),
            len(PAGE_CATEGORY_TO_REGLEMENTS),
        )

    def test_view_refuses_to_run_without_the_taxonomies(self):
        page = self.create_page("permis-urbanisme", "93ny1xr4rq")

        view = self.migrate()

        self.assertEqual(len(view.errors), 2)
        self.assertEqual(page.taxonomy_page_category, "93ny1xr4rq")

    def test_page_is_reported_when_taxonomy_is_not_enabled(self):
        """A term is never written where the behavior is enabled nowhere."""
        self.install_both_taxonomies(on_fti=False)
        page = self.create_page("permis-urbanisme", "93ny1xr4rq")

        view = self.migrate()

        self.assertEqual(view.errors, [])
        self.assertEqual(view.migrated, [])
        self.assertEqual(len(view.not_enabled), 1)
        self.assertEqual(view.not_enabled[0]["field"], AVISENQUETES_FIELD)
        self.assertEqual(page.taxonomy_page_category, "93ny1xr4rq")

    def test_migrate_when_taxonomy_is_enabled_as_an_instance_behavior(self):
        """The behavior may be turned on per object instead of on the FTI."""
        self.install_both_taxonomies(on_fti=False)
        # "Commerce", a sub term of the reglement root term
        page = self.create_page("reglement-commerce", "fpswde31ge")
        sm = self.portal.getSiteManager()
        taxonomy = sm.queryUtility(ITaxonomy, name="collective.taxonomy.reglements")
        enable_behaviors(page, [taxonomy.getGeneratedName()], [])

        view = self.migrate()

        self.assertEqual(view.errors, [])
        self.assertEqual(page.taxonomy_reglements, "8ly7x1obbc")
        self.assertEqual(page.taxonomy_page_category, "reglement")

    def test_dry_run_reports_without_changing_anything(self):
        self.install_both_taxonomies()
        page = self.create_page("permis-urbanisme", "93ny1xr4rq")

        view = self.migrate(apply=False)

        self.assertEqual(len(view.migrated), 1)
        self.assertEqual(view.migrated[0]["new_term"], "b8x771g41d")
        self.assertEqual(page.taxonomy_page_category, "93ny1xr4rq")
        self.assertIsNone(getattr(page, AVISENQUETES_FIELD, None))

    def test_migrate_avisenquetes_term(self):
        self.install_both_taxonomies()
        # "Permis d'urbanisme", a sub term of the avis_et_enquete root term
        page = self.create_page("permis-urbanisme", "93ny1xr4rq")

        self.migrate()

        self.assertEqual(page.taxonomy_avisenquetes, "b8x771g41d")
        self.assertEqual(page.taxonomy_page_category, "avis_et_enquete")
        self.assertIsNone(getattr(page, REGLEMENTS_FIELD, None))

    def test_migrate_reglements_term(self):
        self.install_both_taxonomies()
        # "Taxes additionnelles", a sub term of the reglement root term
        page = self.create_page("taxes-additionnelles", "cnij6b4rjr")

        self.migrate()

        self.assertEqual(page.taxonomy_reglements, "mp4d3c9msm")
        self.assertEqual(page.taxonomy_page_category, "reglement")
        self.assertIsNone(getattr(page, AVISENQUETES_FIELD, None))

    def test_migrate_leaves_unmapped_term_untouched(self):
        self.install_both_taxonomies()
        # "Autres enquêtes" has no equivalent, it stays in page_category
        page = self.create_page("autres-enquetes", "imc5kgi47j")

        view = self.migrate()

        self.assertEqual(view.migrated, [])
        self.assertEqual(page.taxonomy_page_category, "imc5kgi47j")
        self.assertIsNone(getattr(page, AVISENQUETES_FIELD, None))

    def test_migrate_leaves_root_term_untouched(self):
        self.install_both_taxonomies()
        page = self.create_page("publication", "publication")
        empty_page = self.create_page("no-category", None)

        view = self.migrate()

        self.assertEqual(view.migrated, [])
        self.assertEqual(page.taxonomy_page_category, "publication")
        self.assertIsNone(empty_page.taxonomy_page_category)

    def test_migrate_keeps_a_term_already_set_by_an_editor(self):
        self.install_both_taxonomies()
        page = self.create_page("permis-integres", "s21slbx3dg")
        page.taxonomy_avisenquetes = "w2yt44q4ly"  # Réunions d'informations publiques

        view = self.migrate()

        self.assertEqual(len(view.kept), 1)
        self.assertEqual(view.migrated, [])
        self.assertEqual(page.taxonomy_avisenquetes, "w2yt44q4ly")
        self.assertEqual(page.taxonomy_page_category, "avis_et_enquete")

    def test_migrate_stores_a_list_when_taxonomy_is_multi_select(self):
        """The migrated value follows the arity of the registered behavior."""
        self.install_both_taxonomies(single_select=False)
        page = self.create_page("permis-environnement", "wkh7nco011")

        self.migrate()

        self.assertEqual(page.taxonomy_avisenquetes, ["xdf5xbnf5x"])

    def test_migrate_reindexes_migrated_page(self):
        self.install_both_taxonomies()
        page = self.create_page("permis-unique", "slbfv3ir5g")

        self.migrate()

        brains = api.content.find(taxonomy_avisenquetes="0wl3gd1vmf")
        self.assertEqual(
            [brain.getPath() for brain in brains],
            ["/".join(page.getPhysicalPath())],
        )
        self.assertEqual(
            len(api.content.find(taxonomy_page_category="avis_et_enquete")), 1
        )

    def test_migrate_skips_stale_catalog_entries(self):
        """A brain whose object is gone is reported, not raised."""
        self.install_both_taxonomies()
        page = self.create_page("permis-urbanisme", "93ny1xr4rq")
        catalog = api.portal.get_tool("portal_catalog")
        ghost_path = "/".join(self.folder.getPhysicalPath()) + "/decouvrir"
        catalog.catalog_object(page, uid=ghost_path)

        view = self.migrate()

        self.assertEqual(view.stale, [ghost_path])
        self.assertEqual(len(view.migrated), 1)
        self.assertEqual(page.taxonomy_avisenquetes, "b8x771g41d")

    def test_migrate_is_idempotent(self):
        self.install_both_taxonomies()
        page = self.create_page("permis-groupes", "k1m9x7hflb")

        self.migrate()
        view = self.migrate()

        self.assertEqual(view.migrated, [])
        self.assertEqual(page.taxonomy_avisenquetes, "uylqc6415e")
        self.assertEqual(page.taxonomy_page_category, "avis_et_enquete")

    def tearDown(self):
        """Unregister the taxonomies created by the test.

        registerBehavior stores the generated schema on the module-level
        collective.taxonomy.generated namespace, which the transaction abort
        does not roll back.
        """
        sm = self.portal.getSiteManager()
        for short_name in ("avisenquetes", "reglements"):
            name = f"collective.taxonomy.{short_name}"
            taxonomy = sm.queryUtility(ITaxonomy, name=name)
            if taxonomy is None:
                continue
            if sm.queryUtility(IBehavior, name=taxonomy.getGeneratedName()):
                taxonomy.unregisterBehavior()
