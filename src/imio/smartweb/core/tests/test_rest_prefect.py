# -*- coding: utf-8 -*-

from DateTime import DateTime
from imio.smartweb.core.rest.prefect import clean_html
from imio.smartweb.core.rest.prefect import link_url
from imio.smartweb.core.rest.prefect import serialize_collection
from imio.smartweb.core.rest.prefect import serialize_contact
from imio.smartweb.core.rest.prefect import serialize_external_content
from imio.smartweb.core.rest.prefect import serialize_files
from imio.smartweb.core.rest.prefect import serialize_gallery
from imio.smartweb.core.rest.prefect import serialize_html
from imio.smartweb.core.rest.prefect import serialize_linked_rest_view
from imio.smartweb.core.rest.prefect import serialize_links
from imio.smartweb.core.rest.prefect import serialize_map
from imio.smartweb.core.rest.prefect import serialize_metadata
from imio.smartweb.core.rest.prefect import serialize_page
from imio.smartweb.core.rest.prefect import serialize_postit
from imio.smartweb.core.rest.prefect import serialize_section
from imio.smartweb.core.rest.prefect import serialize_selections
from imio.smartweb.core.rest.prefect import serialize_text
from imio.smartweb.core.rest.prefect import serialize_timestamped_publications
from imio.smartweb.core.rest.prefect import serialize_video
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_ACCEPTANCE_TESTING
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.tests.utils import get_json
from imio.smartweb.core.tests.utils import make_named_image
from plone import api
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.app.textfield.value import RichTextValue
from plone.formwidget.geolocation.geolocation import Geolocation
from plone.namedfile.file import NamedBlobFile
from plone.namedfile.file import NamedBlobImage
from plone.restapi.testing import RelativeSession
from z3c.relationfield import RelationValue
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

import json
import requests_mock
import transaction

IADELIBERATIONS_URL = "https://conseil.staging.imio.be"
INSTITUTION_URL = f"{IADELIBERATIONS_URL}/waremme"


def relation(obj):
    return RelationValue(getUtility(IIntIds).getId(obj))


def resolveuid(obj):
    return f"${{portal_url}}/resolveuid/{obj.UID()}"


class TestPrefect(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="Collecte des déchets",
            description="Calendrier et **règles de tri**",
        )
        api.content.transition(self.page, "publish")
        self.page_url = self.page.absolute_url()

    def add_section(self, portal_type, container=None, **kwargs):
        return api.content.create(
            container=container or self.page,
            type=f"imio.smartweb.Section{portal_type}",
            title=kwargs.pop("title", portal_type),
            **kwargs,
        )

    def add_page(self, title, publish=True):
        page = api.content.create(
            container=self.portal, type="imio.smartweb.Page", title=title
        )
        if publish:
            api.content.transition(page, "publish")
        return page

    def add_portal_page(self):
        return api.content.create(
            container=self.portal, type="imio.smartweb.PortalPage", title="Portal"
        )

    def test_serialize_page(self):
        self.page.language = "fr"
        self.add_section("Text", title="First")
        self.add_section("Links", title="Second")
        self.page.moveObjectsByDelta(["second"], -1)
        data = serialize_page(self.page)
        self.assertEqual(
            sorted(data),
            [
                "description",
                "language",
                "metadata",
                "modified",
                "procedure_url",
                "schema_version",
                "sections",
                "title",
                "type",
                "uid",
                "url",
            ],
        )
        self.assertEqual(data["schema_version"], 1)
        self.assertEqual(data["uid"], self.page.UID())
        self.assertEqual(data["url"], self.page_url)
        self.assertEqual(data["type"], "page")
        self.assertEqual(data["language"], "fr")
        self.assertEqual(data["title"], "Collecte des déchets")
        self.assertEqual(data["description"], "Calendrier et **règles de tri**")
        # ISO 8601 in UTC, to the second
        self.assertAlmostEqual(
            DateTime(data["modified"]).timeTime(),
            self.page.modified().timeTime(),
            delta=1,
        )
        self.assertIsNone(data["procedure_url"])
        # sections come in the order of the page, not of creation
        self.assertEqual([s["id"] for s in data["sections"]], ["second", "first"])

        procedure = api.content.create(
            container=self.portal,
            type="imio.smartweb.Procedure",
            title="Procedure",
            procedure_url="https://guichet.example.be/demande",
        )
        data = serialize_page(procedure)
        self.assertEqual(data["type"], "procedure")
        self.assertEqual(data["procedure_url"], "https://guichet.example.be/demande")

        # sections that call external services when they are rendered are
        # serialized without any request: requests_mock refuses all of them
        portal_page = self.add_portal_page()
        self.add_section("Contact", portal_page, related_contacts=["abc"])
        self.add_section("Video", portal_page, video_url="https://youtu.be/abc")
        self.add_section(
            "ExternalContent",
            portal_page,
            external_content_url="https://www.eagle.be/widget",
        )
        self.add_section("Events", portal_page)
        self.add_section("News", portal_page)
        self.add_section("TimestampedPublications", portal_page)
        with requests_mock.Mocker():
            data = serialize_page(portal_page)
        self.assertEqual(data["type"], "portal_page")
        self.assertEqual(
            [(s["type"], s["status"]) for s in data["sections"]],
            [
                ("contact", "ok"),
                ("video", "ok"),
                ("external_content", "ok"),
                ("events", "ok"),
                ("news", "ok"),
                ("timestamped_publications", "ok"),
            ],
        )

    def test_serialize_metadata(self):
        self.page.topics = ["citizenship"]
        self.page.iam = ["newcomer", "removed_term"]
        self.page.taxonomy_page_category = "publication"
        metadata = serialize_metadata(self.page, "fr")
        self.assertEqual(
            metadata,
            {
                "minisite": None,
                "subsite": None,
                "category": "Publication",
                "topics": ["Citoyenneté"],
                "iam": ["Nouvel arrivant"],
            },
        )

        minisite = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            title="Office du tourisme",
        )
        getMultiAdapter((minisite, self.request), name="minisite_settings").enable()
        subsite = api.content.create(
            container=minisite, type="imio.smartweb.Folder", title="Balades"
        )
        getMultiAdapter((subsite, self.request), name="subsite_settings").enable()
        page = api.content.create(
            container=subsite, type="imio.smartweb.Page", title="Balade des crêtes"
        )
        api.content.transition(page, "publish")
        metadata = serialize_metadata(page, "fr")
        self.assertEqual(
            metadata["minisite"],
            {"title": "Office du tourisme", "url": minisite.absolute_url()},
        )
        self.assertEqual(
            metadata["subsite"], {"title": "Balades", "url": subsite.absolute_url()}
        )

        # the folders are private: their names are not given to anonymous users
        logout()
        metadata = serialize_metadata(page, "fr")
        self.assertIsNone(metadata["minisite"])
        self.assertIsNone(metadata["subsite"])

    def test_serialize_section(self):
        section = self.add_section("Text", title="Horaires", hide_title=True)
        self.assertEqual(
            serialize_section(self.page, section),
            {
                "id": "horaires",
                "type": "text",
                "status": "ok",
                "title": "Horaires",
                "title_hidden": True,
                "html": None,
                "iframes": [],
                "image": None,
            },
        )

        # unknown section type: identified, without content
        getMultiAdapter(
            (self.portal, self.request), name="herobanner_settings"
        ).add_herobanner()
        herobanner = self.portal.listFolderContents(
            contentFilter={"portal_type": "imio.smartweb.HeroBanner"}
        )[0]
        slide = self.add_section("Slide", herobanner, title="Slide")
        self.assertEqual(
            serialize_section(self.page, slide),
            {
                "id": "slide",
                "type": "slide",
                "status": "unsupported",
                "title": "Slide",
                "title_hidden": False,
            },
        )

        # corrupted data: the section is marked, the response is not broken
        postit = self.add_section("Postit", title="Infos")
        postit.postits = ["not a dict"]
        self.assertEqual(
            serialize_section(self.page, postit),
            {
                "id": "infos",
                "type": "postit",
                "status": "error",
                "title": "Infos",
                "title_hidden": False,
            },
        )

    def test_serialize_text(self):
        target = self.add_page("Calendrier")
        private = self.add_page("Brouillon", publish=False)
        section = self.add_section("Text")
        section.text = RichTextValue(
            f'<p>Voir <a href="resolveuid/{target.UID()}">le calendrier</a>'
            f' et <a href="resolveuid/{private.UID()}">le brouillon</a>.</p>'
            '<iframe src="https://carto.example.be/map" title="Carte"></iframe>',
            "text/html",
            "text/html",
        )
        section.image = NamedBlobImage(**make_named_image())
        section.image_caption = "Camion"
        logout()
        data = serialize_text(self.page, section)
        # the private content is linked for editors, not for anonymous users
        self.assertEqual(
            data["html"],
            f'<p>Voir <a href="{target.absolute_url()}">le calendrier</a>'
            " et le brouillon.</p>",
        )
        self.assertEqual(
            data["iframes"], [{"url": "https://carto.example.be/map", "title": "Carte"}]
        )
        self.assertEqual(
            data["image"],
            {"url": f"{section.absolute_url()}/@@images/image", "caption": "Camion"},
        )

    def test_serialize_html(self):
        section = self.add_section("HTML", html="<p>Carte</p>", description="**Info**")
        self.assertEqual(
            serialize_html(self.page, section),
            {"description": "**Info**", "html": "<p>Carte</p>", "iframes": []},
        )

    def test_serialize_links(self):
        section = self.add_section("Links", description="Utile")
        published = self.add_page("Recyparcs")
        private = self.add_page("Brouillon", publish=False)
        deleted = self.add_page("Ancien")
        links = [
            ("Recyparcs", resolveuid(published)),
            ("Fost Plus", "https://www.fostplus.be"),
            ("Brouillon", resolveuid(private)),
            ("Ancien", resolveuid(deleted)),
            ("Script", "javascript:alert(1)"),
        ]
        for title, url in links:
            api.content.create(
                container=section,
                type="imio.smartweb.BlockLink",
                title=title,
                remoteUrl=url,
            )
        api.content.delete(deleted)
        logout()
        data = serialize_links(self.page, section)
        self.assertEqual(data["description"], "Utile")
        self.assertEqual(
            [(link["title"], link["url"], link["internal"]) for link in data["links"]],
            [
                ("Recyparcs", published.absolute_url(), True),
                ("Fost Plus", "https://www.fostplus.be", False),
                ("Brouillon", None, True),
                ("Ancien", None, True),
                ("Script", None, False),
            ],
        )

    def test_serialize_gallery(self):
        section = self.add_section("Gallery")
        for title, description in [("Bulle à verre", "Place"), ("plone.png", "")]:
            api.content.create(
                container=section,
                type="Image",
                title=title,
                description=description,
                image=NamedBlobImage(**make_named_image()),
            )
        images = serialize_gallery(self.page, section)["images"]
        self.assertEqual(
            images,
            [
                {
                    "url": f"{section['bulle-a-verre'].absolute_url()}/@@images/image",
                    "title": "Bulle à verre",
                    "description": "Place",
                },
                {
                    "url": f"{section['plone.png'].absolute_url()}/@@images/image",
                    "title": None,
                    "description": None,
                },
            ],
        )

    @requests_mock.Mocker()
    def test_serialize_files(self, m):
        section = self.add_section("Files")
        file_obj = api.content.create(
            container=section,
            type="File",
            title="Règlement",
            file=NamedBlobFile(
                data=b"Article 1", filename="reglement.txt", contentType="text/plain"
            ),
        )
        api.portal.set_registry_record(
            "smartweb.iadeliberations_url", IADELIBERATIONS_URL
        )
        m.get(
            f"{IADELIBERATIONS_URL}/@search?portal_type=Institution",
            text=json.dumps(
                get_json("resources/json_iadeliberations_institutions.json")
            ),
        )
        api.portal.set_registry_record(
            "smartweb.iadeliberations_institution", INSTITUTION_URL
        )
        publication = get_json("resources/json_iadeliberations_publication.json")
        m.get(
            f"{INSTITUTION_URL}/publications/grand-froid?fullobjects=y",
            text=json.dumps(publication),
        )
        api.content.create(
            container=section,
            type="imio.smartweb.Publication",
            id="grand-froid",
            linked_publication="grand-froid",
        )
        self.assertEqual(
            serialize_files(self.page, section)["files"],
            [
                {
                    "title": "Règlement",
                    "description": None,
                    "url": f"{file_obj.absolute_url()}/@@download/file",
                    "mime_type": "text/plain",
                    "size": 9,
                },
                {
                    "title": publication["title"],
                    "description": publication["description"],
                    "url": publication["@id"],
                    "mime_type": publication["file"]["content-type"],
                    "size": publication["file"]["size"],
                },
            ],
        )

    def test_serialize_video(self):
        section = self.add_section("Video", video_url="https://youtu.be/abc")
        self.assertEqual(
            serialize_video(self.page, section),
            {"description": None, "video_url": "https://youtu.be/abc"},
        )

    def test_serialize_map(self):
        section = self.add_section("Map")
        self.assertEqual(
            serialize_map(self.page, section), {"latitude": None, "longitude": None}
        )
        section.geolocation = Geolocation(latitude=50.46, longitude=4.87)
        self.assertEqual(
            serialize_map(self.page, section), {"latitude": 50.46, "longitude": 4.87}
        )

    def test_serialize_postit(self):
        section = self.add_section(
            "Postit",
            postits=[{"title": "Horaires", "subtitle": "", "description": "9h-12h"}],
        )
        self.assertEqual(
            serialize_postit(self.page, section),
            {
                "description": None,
                "postits": [
                    {"title": "Horaires", "subtitle": None, "description": "9h-12h"}
                ],
            },
        )

    def test_serialize_selections(self):
        published = self.add_page("Compostage")
        private = self.add_page("Brouillon", publish=False)
        section = self.add_section("Selections")
        section.selected_items = [relation(private), relation(published)]
        self.assertEqual(len(serialize_selections(self.page, section)["items"]), 2)
        # rendering shows private targets (rel.to_object): @prefect does not
        logout()
        self.assertEqual(
            serialize_selections(self.page, section),
            {
                "items": [
                    {
                        "title": "Compostage",
                        "description": None,
                        "url": published.absolute_url(),
                    }
                ]
            },
        )

    def test_serialize_external_content(self):
        section = self.add_section(
            "ExternalContent",
            external_content_url="https://www.eagle.be/widget",
            external_content_params="{'technical': 'config'}",
        )
        self.assertEqual(
            serialize_external_content(self.page, section),
            {"description": None, "url": "https://www.eagle.be/widget"},
        )

    def test_serialize_contact(self):
        section = self.add_section("Contact", related_contacts=["uid1", "uid2"])
        self.assertEqual(
            serialize_contact(self.page, section), {"contact_uids": ["uid1", "uid2"]}
        )

    def test_serialize_collection(self):
        collection = api.content.create(
            container=self.portal, type="Collection", title="Actualités"
        )
        section = self.add_section(
            "Collection", self.add_portal_page(), link_text="Tout voir"
        )
        section.collection = relation(collection)
        self.assertEqual(
            serialize_collection(self.page, section),
            {"link_text": "Tout voir", "url": collection.absolute_url()},
        )
        logout()
        self.assertEqual(
            serialize_collection(self.page, section),
            {"link_text": "Tout voir", "url": None},
        )

    def test_serialize_linked_rest_view(self):
        events_view = api.content.create(
            container=self.portal, type="imio.smartweb.EventsView", title="Agenda"
        )
        section = self.add_section(
            "Events", self.add_portal_page(), link_text="Tout l'agenda"
        )
        self.assertEqual(
            serialize_linked_rest_view(self.page, section),
            {"link_text": "Tout l'agenda", "url": None},
        )
        section.linking_rest_view = relation(events_view)
        self.assertEqual(
            serialize_linked_rest_view(self.page, section),
            {"link_text": "Tout l'agenda", "url": events_view.absolute_url()},
        )

    @requests_mock.Mocker()
    def test_serialize_timestamped_publications(self, m):
        section = self.add_section(
            "TimestampedPublications", related_timestamped_publications=["p1", "p2"]
        )
        self.assertEqual(
            serialize_timestamped_publications(self.page, section),
            {"publication_uids": ["p1", "p2"], "publications_source_url": None},
        )
        api.portal.set_registry_record(
            "smartweb.iadeliberations_url", IADELIBERATIONS_URL
        )
        m.get(
            f"{IADELIBERATIONS_URL}/@search?portal_type=Institution",
            text=json.dumps(
                get_json("resources/json_iadeliberations_institutions.json")
            ),
        )
        api.portal.set_registry_record(
            "smartweb.iadeliberations_institution", INSTITUTION_URL
        )
        self.assertEqual(
            serialize_timestamped_publications(self.page, section),
            {
                "publication_uids": ["p1", "p2"],
                "publications_source_url": INSTITUTION_URL,
            },
        )

    def test_link_url(self):
        target = self.add_page("Cible")
        self.assertEqual(link_url(self.page, resolveuid(target)), target.absolute_url())
        self.assertEqual(
            link_url(self.page, "${portal_url}/cible"),
            f"{self.portal.absolute_url()}/cible",
        )
        self.assertEqual(
            link_url(self.page, "mailto:info@commune.be"), "mailto:info@commune.be"
        )
        self.assertEqual(link_url(self.page, "tel:+3281000000"), "tel:+3281000000")
        self.assertIsNone(link_url(self.page, "javascript:alert(1)"))
        self.assertIsNone(link_url(self.page, "${portal_url}/resolveuid/unknown"))
        self.assertIsNone(link_url(self.page, ""))

    def test_clean_html(self):
        base_url = f"{self.page_url}/"
        html, iframes = clean_html(
            '<p onclick="steal()" style="color:red" class="lead">Intro '
            '<a href="javascript:alert(1)">piège</a> '
            '<a href="mailto:info@commune.be">mail</a> '
            '<a href="tel:+3281000000">tel</a> '
            '<a href="docs/plan.pdf">plan</a> '
            '<a href="resolveuid/deleted">ancien</a></p>'
            "<script>alert(1)</script><!-- note --><style>p {}</style>"
            '<iframe src="https://carto.example.be/map" title="Carte"></iframe>'
            '<iframe src="javascript:steal()"></iframe>'
            '<iframe src="resolveuid/deleted" title="Interne"></iframe>'
            '<img src="data:image/png;base64,AAAA" alt="inline">'
            '<img src="https://img.example.be/a.png" alt="Photo">',
            base_url,
        )
        self.assertEqual(
            html,
            "<p>Intro piège "
            '<a href="mailto:info@commune.be">mail</a> '
            '<a href="tel:+3281000000">tel</a> '
            f'<a href="{self.page_url}/docs/plan.pdf">plan</a> '
            "ancien</p>"
            '<img src="https://img.example.be/a.png" alt="Photo">',
        )
        self.assertEqual(
            iframes, [{"url": "https://carto.example.be/map", "title": "Carte"}]
        )
        self.assertEqual(clean_html("", base_url), (None, []))
        self.assertEqual(clean_html("<script>x()</script>", base_url), (None, []))


class TestPrefectGet(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_ACCEPTANCE_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.published = api.content.create(
            container=self.portal, type="imio.smartweb.Page", title="Publiée"
        )
        api.content.transition(self.published, "publish")
        self.private = api.content.create(
            container=self.portal, type="imio.smartweb.Page", title="Privée"
        )
        getMultiAdapter(
            (self.portal, self.request), name="footer_settings"
        ).add_footer()
        self.footer = self.portal.listFolderContents(
            contentFilter={"portal_type": "imio.smartweb.Footer"}
        )[0]
        transaction.commit()
        self.anonymous = RelativeSession(self.portal.absolute_url())
        self.anonymous.headers.update({"Accept": "application/json"})
        self.manager = RelativeSession(self.portal.absolute_url())
        self.manager.headers.update({"Accept": "application/json"})
        self.manager.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

    def tearDown(self):
        self.anonymous.close()
        self.manager.close()

    def test_reply(self):
        response = self.anonymous.get("publiee/@prefect")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Publiée")
        # a private page is not exposed to anonymous users
        self.assertEqual(self.anonymous.get("privee/@prefect").status_code, 401)
        response = self.manager.get("privee/@prefect")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Privée")
        # a footer is a part of other pages, not an eligible page
        response = self.manager.get(f"{self.footer.getId()}/@prefect")
        self.assertEqual(response.status_code, 404)
