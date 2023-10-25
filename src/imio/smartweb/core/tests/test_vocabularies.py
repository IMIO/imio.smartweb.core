# -*- coding: utf-8 -*-

from freezegun import freeze_time
from imio.smartweb.common.utils import get_vocabulary
from imio.smartweb.core import config
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.tests.utils import get_json
from plone import api
from unittest.mock import patch

import json
import requests
import requests_mock

GUICHET_URL = "https://demo.guichet-citoyen.be/api/formdefs/"


class TestVocabularies(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.json_procedures_raw_mock = get_json(
            "resources/json_procedures_raw_mock.json"
        )
        self.json_contacts_raw_mock = get_json("resources/json_contacts_raw_mock.json")
        self.json_empty_contacts_raw_mock = get_json(
            "resources/json_no_contact_raw_mock.json"
        )
        self.contact_search_url = "http://localhost:8080/Plone/@search?portal_type=imio.directory.Contact&selected_entities=396907b3b1b04a97896b12cc792c77f8&sort_on=breadcrumb&b_size=1000000&metadata_fields=UID&metadata_fields=breadcrumb"

    def test_icons(self):
        self.assertVocabularyLen("imio.smartweb.vocabulary.Icons", 49)
        vocabulary = get_vocabulary("imio.smartweb.vocabulary.Icons")
        term = vocabulary.getTerm("action.email")
        self.assertEqual(term.title, "Action - Email")

    @requests_mock.Mocker()
    def test_procedure_keys(self, m):
        m.get(GUICHET_URL, text=json.dumps(self.json_procedures_raw_mock))
        self.assertVocabularyLen("imio.smartweb.vocabulary.PublikProcedures", 3)
        vocabulary = get_vocabulary("imio.smartweb.vocabulary.PublikProcedures")
        self.assertEqual(
            vocabulary.getTerm(
                "https://demo-formulaires.guichet-citoyen.be/acte-de-deces/"
            ).title,
            "Acte de d\\u00e9c\\u00e8s",
        )
        self.assertEqual(
            vocabulary.getTerm(
                "https://demo-formulaires.guichet-citoyen.be/acte-de-divorce/"
            ).title,
            "Acte de divorce",
        )
        self.assertEqual(
            vocabulary.getTerm(
                "https://demo-formulaires.guichet-citoyen.be/acte-de-mariage/"
            ).title,
            "Acte de mariage",
        )
        api.portal.set_registry_record(
            "smartweb.url_formdefs_api",
            "https://demo.guichet-citoyen.be/api/formdefs/?query=kamoulox",
        )
        m.get(
            "https://demo.guichet-citoyen.be/api/formdefs/?query=kamoulox",
            text=json.dumps(self.json_procedures_raw_mock),
        )
        self.assertVocabularyLen("imio.smartweb.vocabulary.PublikProcedures", 3)

    @requests_mock.Mocker()
    def test_procedure_error_values(self, m):
        m.get(GUICHET_URL, exc=requests.exceptions.ConnectTimeout)
        self.assertVocabularyLen("imio.smartweb.vocabulary.PublikProcedures", 0)

        m.get(GUICHET_URL, status_code=404)
        self.assertVocabularyLen("imio.smartweb.vocabulary.PublikProcedures", 0)

        api.portal.set_registry_record("smartweb.url_formdefs_api", "")
        m.get(GUICHET_URL, text=json.dumps(self.json_procedures_raw_mock))
        self.assertVocabularyLen("imio.smartweb.vocabulary.PublikProcedures", 0)

    def test_bootstrap_css(self):
        self.assertVocabularyLen("imio.smartweb.vocabulary.BootstrapCSS", 6)

    def test_orientation(self):
        self.assertVocabularyLen("imio.smartweb.vocabulary.Orientation", 2)

    def test_subsite_display_mode(self):
        self.assertVocabularyLen("imio.smartweb.vocabulary.SubsiteDisplayMode", 3)

    def test_contact_blocks(self):
        self.assertVocabularyLen("imio.smartweb.vocabulary.ContactBlocks", 10)

    @requests_mock.Mocker()
    def test_empty_remote_directory_entities(self, m):
        m.get(
            self.contact_search_url, text=json.dumps(self.json_empty_contacts_raw_mock)
        )
        self.assertVocabularyLen("imio.smartweb.vocabulary.RemoteDirectoryEntities", 0)

    @requests_mock.Mocker()
    def test_remote_directory_entities(self, m):
        json_entities_raw_mock = get_json(
            "resources/json_directory_entities_raw_mock.json"
        )
        url = "{}/@search?portal_type=imio.directory.Entity&sort_on=sortable_title&b_size=1000000&metadata_fields=UID".format(
            config.DIRECTORY_URL
        )
        m.get(url, text=json.dumps(json_entities_raw_mock))
        self.assertVocabularyLen("imio.smartweb.vocabulary.RemoteDirectoryEntities", 2)
        vocabulary = get_vocabulary("imio.smartweb.vocabulary.RemoteDirectoryEntities")
        self.assertEqual(
            vocabulary.getTerm("7c69f9a738ec497c819725c55888ee3a").title,
            "Belleville",
        )

    @requests_mock.Mocker()
    def test_remote_agendas(self, m):
        json_entities_raw_mock = get_json(
            "resources/json_events_entities_raw_mock.json"
        )
        url = f"{config.EVENTS_URL}/@search?UID=7c69f9a738ec497c819725c55888ee31"
        m.get(url, text=json.dumps(json_entities_raw_mock))
        json_agendas_raw_mock = get_json("resources/json_events_agendas_raw_mock.json")
        url = f"{config.EVENTS_URL}/imio-events-entity/@search?portal_type=imio.events.Agenda&sort_on=sortable_title&b_size=1000000&metadata_fields=UID"
        m.get(url, text=json.dumps(json_agendas_raw_mock))
        self.assertVocabularyLen("imio.smartweb.vocabulary.RemoteAgendas", 2)
        vocabulary = get_vocabulary("imio.smartweb.vocabulary.RemoteAgendas")
        self.assertEqual(
            vocabulary.getTerm("64f4cbee9a394a018a951f6d94452914").title,
            "Agenda administration de Belleville",
        )

    @requests_mock.Mocker()
    def test_remote_news_empty_entity(self, m):
        # mock "control panel" to set entity
        url = "http://localhost:8080/Plone/@search?metadata_fields=UID&portal_type=imio.news.Entity"
        json_entities_raw_mock = get_json("resources/json_news_entities_raw_mock.json")
        m.get(url, text=json.dumps(json_entities_raw_mock))
        api.portal.set_registry_record(
            "smartweb.news_entity_uid", "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
        )

        # mock 2 : search one entity
        json_entity_raw_mock = get_json("resources/json_search_one_news_entity.json")
        url = f"{config.NEWS_URL}/@search?UID=zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
        m.get(url, text=json.dumps(json_entity_raw_mock))

        # mock 3
        json_no_newsfolder_raw_mock = get_json(
            "resources/json_no_newsfolder_raw_mock.json"
        )
        url = "http://localhost:8080/Plone/imio-news-empty-entity/@search?portal_type=imio.news.NewsFolder&sort_on=sortable_title&b_size=1000000&metadata_fields=UID"
        m.get(url, text=json.dumps(json_no_newsfolder_raw_mock))
        self.assertVocabularyLen("imio.smartweb.vocabulary.RemoteNewsFolders", 0)

    @requests_mock.Mocker()
    def test_remote_newsfolder(self, m):
        json_entities_raw_mock = get_json("resources/json_news_entities_raw_mock.json")
        url = f"{config.NEWS_URL}/@search?UID=7c69f9a738ec497c819725c55888ee32"
        m.get(url, text=json.dumps(json_entities_raw_mock))
        json_newsfolder_raw_mock = get_json(
            "resources/json_news_newsfolder_raw_mock.json"
        )
        url = f"{config.NEWS_URL}/imio-news-entity/@search?portal_type=imio.news.NewsFolder&sort_on=sortable_title&b_size=1000000&metadata_fields=UID"
        m.get(url, text=json.dumps(json_newsfolder_raw_mock))
        self.assertVocabularyLen("imio.smartweb.vocabulary.RemoteNewsFolders", 2)
        vocabulary = get_vocabulary("imio.smartweb.vocabulary.RemoteNewsFolders")
        self.assertEqual(
            vocabulary.getTerm("64f4cbee9a394a018a951f6d94452914").title,
            "News folder : Administration de Belleville",
        )

    @requests_mock.Mocker()
    def test_remote_contacts_error_values(self, m):
        m.get(self.contact_search_url, exc=requests.exceptions.ConnectTimeout)
        self.assertVocabularyLen("imio.smartweb.vocabulary.RemoteContacts", 0)
        m.get(self.contact_search_url, status_code=404)
        self.assertVocabularyLen("imio.smartweb.vocabulary.RemoteContacts", 0)

    @requests_mock.Mocker()
    def test_empty_remote_contacts(self, m):
        m.get(
            self.contact_search_url, text=json.dumps(self.json_empty_contacts_raw_mock)
        )
        self.assertVocabularyLen("imio.smartweb.vocabulary.RemoteContacts", 0)

    def test_alignment(self):
        self.assertVocabularyLen("imio.smartweb.vocabulary.Alignment", 4)

    def test_image_size(self):
        self.assertVocabularyLen("imio.smartweb.vocabulary.ImageSize", 2)

    def test_concat_category_topics_vocabulary(self):
        self.assertVocabularyLen("imio.smartweb.vocabulary.CategoryAndTopics", 126)

    def test_gallery_mode(self):
        self.assertVocabularyLen("imio.smartweb.vocabulary.GalleryMode", 2)

    def test_category_and_topics_vocabulary(self):
        self.assertVocabularyLen(
            "imio.smartweb.vocabulary.FilteredCategoryAndTopics", 0
        )

        record = {
            "emploi-mobility": "Emploie dans la mobilité",
            "presse-social": "Presse Sociale",
            "reglement-culture": "Reglement Culture",
        }

        api.portal.set_registry_record(
            name="smartweb.category_and_topics_vocabulary", value=record
        )
        self.assertVocabularyLen(
            "imio.smartweb.vocabulary.FilteredCategoryAndTopics", 3
        )

    @requests_mock.Mocker()
    def test_remote_contact_categories(self, m):
        json_contact_category_raw_mock = get_json(
            "resources/json_contact_category_raw_mock.json"
        )
        with patch(
            "imio.smartweb.core.vocabularies.get_wca_token", return_value="kamoulox"
        ):
            url = f"{config.DIRECTORY_URL}/@vocabularies/collective.taxonomy.contact_category"
            m.get(url, text=json.dumps(json_contact_category_raw_mock))
            self.assertVocabularyLen("imio.smartweb.vocabulary.DirectoryCategories", 25)
            vocabulary = get_vocabulary("imio.smartweb.vocabulary.DirectoryCategories")
            self.assertEqual(
                vocabulary.getTermByToken("cho96vl9ox").title,
                "Commerces et entreprises",
            )

    @requests_mock.Mocker()
    def test_remote_events_types(self, m):
        json_events_types_raw_mock = get_json(
            "resources/json_events_types_raw_mock.json"
        )
        with patch(
            "imio.smartweb.core.vocabularies.get_wca_token", return_value="kamoulox"
        ):
            url = f"{config.EVENTS_URL}/@vocabularies/imio.events.vocabulary.EventTypes"
            m.get(url, text=json.dumps(json_events_types_raw_mock))
            self.assertVocabularyLen("imio.smartweb.vocabulary.EventsTypes", 2)
            vocabulary = get_vocabulary("imio.smartweb.vocabulary.EventsTypes")
            self.assertEqual(
                vocabulary.getTermByToken("activity").title,
                "Activité (extrascolaire, sport, atelier et cours, etc.)",
            )

    @requests_mock.Mocker()
    @freeze_time("2021-11-15")
    def test_events_from_entity(self, m):
        json_entities_raw_mock = get_json(
            "resources/json_events_entities_raw_mock.json"
        )
        url = f"{config.EVENTS_URL}/@search?UID=7c69f9a738ec497c819725c55888ee31"
        m.get(url, text=json.dumps(json_entities_raw_mock))
        json_agendas_raw_mock = get_json("resources/json_events_agendas_raw_mock.json")
        url = f"{config.EVENTS_URL}/imio-events-entity/@search?portal_type=imio.events.Agenda&sort_on=sortable_title&b_size=1000000&metadata_fields=UID"
        m.get(url, text=json.dumps(json_agendas_raw_mock))
        url = f"{config.EVENTS_URL}/@search?selected_agendas=64f4cbee9a394a018a951f6d94452914&selected_agendas=96d3e3299dc74386943e12c4f4fd0b8a&portal_type=imio.events.Event&metadata_fields=category&metadata_fields=topics&metadata_fields=start&metadata_fields=end&metadata_fields=has_leadimage&metadata_fields=breadcrumb&metadata_fields=UID&event_dates.query=2021-11-15&event_dates.range=min&b_size=1000000"
        json_rest_events = get_json("resources/json_rest_events_with_breadcrumbs.json")
        m.get(url, text=json.dumps(json_rest_events))
        vocabulary = get_vocabulary("imio.smartweb.vocabulary.EventsFromEntity")
        self.assertEqual(
            vocabulary.getTermByToken("97902f2e26774a369035117d56381a2a").title,
            "Belleville » Accueil temps libre » Journée de l'ATL",
        )

    @requests_mock.Mocker()
    def test_news_from_entity(self, m):
        json_entities_raw_mock = get_json("resources/json_news_entities_raw_mock.json")
        url = f"{config.NEWS_URL}/@search?UID=7c69f9a738ec497c819725c55888ee32"
        m.get(url, text=json.dumps(json_entities_raw_mock))
        json_newsfolders_raw_mock = get_json(
            "resources/json_news_newsfolder_raw_mock.json"
        )
        url = f"{config.NEWS_URL}/imio-news-entity/@search?portal_type=imio.news.NewsFolder&sort_on=sortable_title&b_size=1000000&metadata_fields=UID"
        m.get(url, text=json.dumps(json_newsfolders_raw_mock))
        url = f"{config.NEWS_URL}/@search?selected_news_folders=64f4cbee9a394a018a951f6d94452914&selected_news_folders=96d3e3299dc74386943e12c4f4fd0b8a&portal_type=imio.news.NewsItem&metadata_fields=category&metadata_fields=topics&metadata_fields=has_leadimage&metadata_fields=breadcrumb&metadata_fields=UID&b_size=1000000"
        json_rest_news = get_json("resources/json_rest_news.json")
        m.get(url, text=json.dumps(json_rest_news))
        vocabulary = get_vocabulary("imio.smartweb.vocabulary.NewsItemsFromEntity")
        self.assertEqual(
            vocabulary.getTermByToken("bfe2b4391a0f4a8db6d8b7fed63d1c4a").title,
            "belleville >> commune >> Restauration de la Bibliothèque",
        )

    def test_sendinblue_button_position(self):
        self.assertVocabularyLen("imio.smartweb.vocabulary.SendInBlueButtonPosition", 2)
