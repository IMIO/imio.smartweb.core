# -*- coding: utf-8 -*-
from imio.smartweb.core.contents import ICampaignView
from imio.smartweb.core.contents.rest.campaign.endpoint import AllTopicsEndpoint
from imio.smartweb.core.contents.rest.campaign.endpoint import AllTopicsEndpointGet
from imio.smartweb.core.contents.rest.campaign.endpoint import AuthCampaignEndpointGet
from imio.smartweb.core.contents.rest.campaign.endpoint import CampaignEndpoint
from imio.smartweb.core.contents.rest.campaign.endpoint import CampaignEndpointGet
from imio.smartweb.core.contents.rest.campaign.endpoint import (
    PROJECT_WORKFLOW_STATUS_TO_KEEP,
)
from imio.smartweb.core.contents.rest.campaign.endpoint import TopicsEndpoint
from imio.smartweb.core.contents.rest.campaign.endpoint import TopicsEndpointGet
from imio.smartweb.core.contents.rest.campaign.endpoint import TsTopicsEndpoint
from imio.smartweb.core.contents.rest.campaign.endpoint import TsTopicsEndpointGet
from imio.smartweb.core.contents.rest.campaign.endpoint import ZonesEndpoint
from imio.smartweb.core.contents.rest.campaign.endpoint import ZonesEndpointGet
from imio.smartweb.core.contents.rest.campaign.endpoint import (
    get_ideabox_basic_auth_header,
)
from imio.smartweb.core.tests.utils import get_json
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from unittest.mock import MagicMock
from unittest.mock import patch
from zope.component import createObject
from zope.component import queryUtility
from zope.publisher.browser import TestRequest

import base64
import json
import requests_mock

_ENDPOINT = "imio.smartweb.core.contents.rest.campaign.endpoint"
_SUBSCRIBER = "imio.smartweb.core.subscribers"


class TestIdeabox(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.folder = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            title="A Folder",
        )
        self.json_campaigns_raw_mock = get_json("resources/json_ideabox_campaigns.json")
        self.json_campaign_raw_mock = get_json("resources/json_ideabox_campaign.json")

    def test_ct_publication_schema(self):
        fti = queryUtility(IDexterityFTI, name="imio.smartweb.CampaignView")
        schema = fti.lookupSchema()
        self.assertEqual(ICampaignView, schema)

    def test_ct_publication_fti(self):
        fti = queryUtility(IDexterityFTI, name="imio.smartweb.CampaignView")
        self.assertTrue(fti)

    def test_ct_publication_factory(self):
        fti = queryUtility(IDexterityFTI, name="imio.smartweb.CampaignView")
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(
            ICampaignView.providedBy(obj),
            "ICampaignView not provided by {0}!".format(
                obj,
            ),
        )

    @patch("imio.smartweb.core.subscribers.get_basic_auth_json")
    @patch("imio.smartweb.core.subscribers.get_value_from_registry")
    @patch("imio.smartweb.core.contents.rest.campaign.content.get_basic_auth_json")
    @patch("imio.smartweb.core.contents.rest.campaign.content.get_value_from_registry")
    def test_get_campaign(
        self,
        m_get_value_from_registry_namechooser,
        m_get_basic_auth_json_namechooser,
        m_get_value_from_registry,
        m_get_basic_auth_json,
    ):
        m_get_value_from_registry.return_value = (
            "https://staging3-formulaires.guichet-citoyen.be/api"
        )
        m_get_basic_auth_json.return_value = self.json_campaign_raw_mock

        m_get_value_from_registry_namechooser.return_value = (
            "https://staging3-formulaires.guichet-citoyen.be/api"
        )
        m_get_basic_auth_json_namechooser.return_value = self.json_campaign_raw_mock
        campaign_view = api.content.create(
            title="kamoulox",
            container=self.folder,
            type="imio.smartweb.CampaignView",
            linked_campaign="2",
        )
        self.assertEqual(campaign_view.title, "Sprint iMio Fall 2024")
        self.assertEqual(campaign_view.id, "sprint-imio-fall-2024")

    # CampaignNameChooser : Give th Title to our object thanks to e-guichet object Title.
    @patch("imio.smartweb.core.subscribers.get_basic_auth_json")
    @patch("imio.smartweb.core.subscribers.get_value_from_registry")
    @patch("imio.smartweb.core.contents.rest.campaign.content.get_basic_auth_json")
    @patch("imio.smartweb.core.contents.rest.campaign.content.get_value_from_registry")
    def test_campaign_name_chooser(
        self,
        m_get_value_from_registry_namechooser,
        m_get_basic_auth_json_namechooser,
        m_get_value_from_registry,
        m_get_basic_auth_json,
    ):
        from imio.smartweb.core.contents.rest.campaign.content import CampaignView
        from zope.component import queryAdapter
        from zope.container.interfaces import INameChooser

        m_get_value_from_registry.return_value = (
            "https://staging3-formulaires.guichet-citoyen.be/api"
        )
        m_get_basic_auth_json.return_value = self.json_campaign_raw_mock

        m_get_value_from_registry_namechooser.return_value = (
            "https://staging3-formulaires.guichet-citoyen.be/api"
        )
        m_get_basic_auth_json_namechooser.return_value = self.json_campaign_raw_mock
        campaign_view = CampaignView(id="test-campaign", title=None)
        campaign_view.linked_campaign = "2"
        name_chooser = queryAdapter(self.folder, INameChooser)
        generated_id = name_chooser.chooseName(None, campaign_view)
        self.assertEqual(campaign_view.title, "Sprint iMio Fall 2024")
        self.assertEqual(generated_id, "sprint-imio-fall-2024")

    @requests_mock.Mocker()
    @patch("imio.smartweb.core.subscribers.get_basic_auth_json")
    @patch("imio.smartweb.core.subscribers.get_value_from_registry")
    def test_get_projects(self, m_get_value_from_registry, m_get_basic_auth_json, m):
        m_get_value_from_registry.return_value = (
            "https://staging3-formulaires.guichet-citoyen.be/api"
        )
        m_get_basic_auth_json.return_value = self.json_campaign_raw_mock
        campaign_view = api.content.create(
            id="kamoulox",
            container=self.folder,
            type="imio.smartweb.CampaignView",
            linked_campaign="2",
        )
        # react additionnal fields request.
        # form={
        #         "taxonomy_contact_category_for_filtering": ("token"),
        #         "topics": "education",
        #     }

        request = TestRequest()
        endpoint = CampaignEndpoint(campaign_view, request)
        url = endpoint.query_url
        filter_statut = "|".join(PROJECT_WORKFLOW_STATUS_TO_KEEP)
        self.assertEqual(
            url,
            f"https://demo-formulaires.guichet-citoyen.be/api/cards/imio-ideabox-projet/list?filter-campagne=2&full=on&filter-statut={filter_statut}&filter-statut-operator=in&",
        )

        m.get(url, text=json.dumps({}))
        call = endpoint()
        self.assertEqual(call, {})

        # to be continued


# ---------------------------------------------------------------------------
# Helpers shared across new test classes
# ---------------------------------------------------------------------------


def _make_project(extra=None):
    """Return a minimal project dict that satisfies CampaignEndpoint logic."""
    project = {
        "uuid": "test-uuid",
        "id": "1",
        "display_name": "Test Project",
        "text": "Some text",
        "url": "http://example.com/p/1",
        "api_url": "http://example.com/api/p/1",
        "fields": {"images_raw": [{"image": {"url": "http://example.com/img.png"}}]},
        "workflow": {"status": "Publié"},
        "user": {"name": "Alice"},
        "roles": {"admin": []},
        "submission": {"channel": "web"},
        "evolution": [{"time": "2024-01-01", "status": "recorded"}],
        "should_be_removed": "yes",
    }
    if extra:
        project.update(extra)
    return project


class _CampaignViewMixin(ImioSmartwebTestCase):
    """Mixin that creates a CampaignView while silencing subscriber API calls."""

    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.folder = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            title="Campaign Folder",
        )
        patcher_vfr = patch(
            f"{_SUBSCRIBER}.get_value_from_registry",
            return_value="https://staging.guichet-citoyen.be/api",
        )
        patcher_baj = patch(
            f"{_SUBSCRIBER}.get_basic_auth_json",
            return_value={"fields": {"titre": "Test Campaign", "description": "Desc"}},
        )
        patcher_vfr.start()
        patcher_baj.start()
        self.campaign_view = api.content.create(
            id="test-campaign",
            container=self.folder,
            type="imio.smartweb.CampaignView",
            linked_campaign="42",
        )
        patcher_vfr.stop()
        patcher_baj.stop()

    def _make_endpoint(self, form=None):
        request = TestRequest(form=form or {})
        return CampaignEndpoint(self.campaign_view, request)


# ---------------------------------------------------------------------------
# get_ideabox_basic_auth_header
# ---------------------------------------------------------------------------


class TestGetIdeaboxBasicAuthHeader(_CampaignViewMixin):

    @patch(
        "plone.api.portal.get_registry_record",
        side_effect=lambda k: {
            "smartweb.iaideabox_api_username": "user42",
            "smartweb.iaideabox_api_password": "s3cr3t",
        }[k],
    )
    def test_returns_basic_auth_header(self, _mock):
        header = get_ideabox_basic_auth_header()
        expected_b64 = base64.b64encode(b"user42:s3cr3t").decode("utf-8")
        self.assertEqual(header, f"Basic {expected_b64}")

    @patch(
        "plone.api.portal.get_registry_record",
        side_effect=lambda k: {
            "smartweb.iaideabox_api_username": "a",
            "smartweb.iaideabox_api_password": "b",
        }[k],
    )
    def test_header_starts_with_basic(self, _mock):
        header = get_ideabox_basic_auth_header()
        self.assertTrue(header.startswith("Basic "))

    @patch(
        "plone.api.portal.get_registry_record",
        side_effect=lambda k: {
            "smartweb.iaideabox_api_username": "u",
            "smartweb.iaideabox_api_password": "p",
        }[k],
    )
    def test_header_b64_is_decodable(self, _mock):
        header = get_ideabox_basic_auth_header()
        b64_part = header[len("Basic ") :]
        decoded = base64.b64decode(b64_part).decode("utf-8")
        self.assertIn(":", decoded)


# ---------------------------------------------------------------------------
# CampaignEndpoint.__call__
# ---------------------------------------------------------------------------


class TestCampaignEndpointCall(_CampaignViewMixin):

    def test_call_returns_empty_dict_when_no_json(self):
        endpoint = self._make_endpoint()
        with patch.object(endpoint, "_get_json", return_value=None):
            result = endpoint()
        self.assertEqual(result, {})

    def test_call_returns_empty_dict_when_json_is_empty(self):
        endpoint = self._make_endpoint()
        with patch.object(endpoint, "_get_json", return_value={}):
            result = endpoint()
        self.assertEqual(result, {})

    def test_call_returns_items_and_total_for_list(self):
        endpoint = self._make_endpoint()
        mock_resp = MagicMock()
        mock_resp.content = b"img_bytes"
        with patch.object(
            endpoint, "_get_json", return_value={"data": [_make_project()], "count": 1}
        ):
            with patch.object(endpoint, "get_image", return_value=mock_resp):
                result = endpoint()
        self.assertIn("items", result)
        self.assertIn("items_total", result)
        self.assertEqual(result["items_total"], 1)
        self.assertEqual(len(result["items"]), 1)

    def test_call_filters_to_required_keys(self):
        require_keys = {
            "uuid",
            "id",
            "display_name",
            "text",
            "url",
            "api_url",
            "fields",
            "workflow",
        }
        endpoint = self._make_endpoint()
        mock_resp = MagicMock()
        mock_resp.content = b"img"
        with patch.object(
            endpoint, "_get_json", return_value={"data": [_make_project()], "count": 1}
        ):
            with patch.object(endpoint, "get_image", return_value=mock_resp):
                result = endpoint()
        returned_keys = set(result["items"][0].keys())
        self.assertTrue(returned_keys.issubset(require_keys))
        self.assertNotIn("should_be_removed", returned_keys)
        self.assertNotIn("user", returned_keys)

    def test_call_items_total_comes_from_count(self):
        endpoint = self._make_endpoint()
        mock_resp = MagicMock()
        mock_resp.content = b"img"
        with patch.object(
            endpoint,
            "_get_json",
            return_value={"data": [_make_project(), _make_project()], "count": 99},
        ):
            with patch.object(endpoint, "get_image", return_value=mock_resp):
                result = endpoint()
        self.assertEqual(result["items_total"], 99)

    def test_call_returns_single_project_dict_when_no_data_key(self):
        single = {
            "uuid": "x",
            "id": "3",
            "title": "A project",
            "evolution": ["something"],
            "roles": {"r": []},
            "submission": {"channel": "web"},
            "user": {"name": "Bob"},
        }
        endpoint = self._make_endpoint()
        with patch.object(endpoint, "_get_json", return_value=single):
            result = endpoint()
        self.assertEqual(result["uuid"], "x")
        self.assertEqual(result["title"], "A project")

    def test_call_removes_evolution_from_single_project(self):
        single = {"uuid": "x", "evolution": ["e"], "id": "1"}
        endpoint = self._make_endpoint()
        with patch.object(endpoint, "_get_json", return_value=single):
            result = endpoint()
        self.assertNotIn("evolution", result)

    def test_call_removes_roles_from_single_project(self):
        single = {"uuid": "x", "roles": {"admin": []}, "id": "1"}
        endpoint = self._make_endpoint()
        with patch.object(endpoint, "_get_json", return_value=single):
            result = endpoint()
        self.assertNotIn("roles", result)

    def test_call_removes_submission_from_single_project(self):
        single = {"uuid": "x", "submission": {"channel": "web"}, "id": "1"}
        endpoint = self._make_endpoint()
        with patch.object(endpoint, "_get_json", return_value=single):
            result = endpoint()
        self.assertNotIn("submission", result)

    def test_call_removes_user_from_single_project(self):
        single = {"uuid": "x", "user": {"name": "Bob"}, "id": "1"}
        endpoint = self._make_endpoint()
        with patch.object(endpoint, "_get_json", return_value=single):
            result = endpoint()
        self.assertNotIn("user", result)


# ---------------------------------------------------------------------------
# CampaignEndpoint.query_url
# ---------------------------------------------------------------------------


class TestCampaignEndpointQueryUrl(_CampaignViewMixin):

    @patch(f"{_ENDPOINT}.get_ts_api_url", return_value="https://wcs.example.be/api")
    def test_query_url_with_specific_id_returns_single_project_url(self, _mock):
        endpoint = self._make_endpoint(form={"id": "7"})
        url = endpoint.query_url
        self.assertIn("/cards/imio-ideabox-projet/7", url)
        self.assertIn("full=on", url)
        self.assertNotIn("filter-campagne", url)

    @patch(f"{_ENDPOINT}.get_ts_api_url", return_value="https://wcs.example.be/api")
    def test_query_url_list_contains_campaign_id(self, _mock):
        endpoint = self._make_endpoint()
        url = endpoint.query_url
        self.assertIn("filter-campagne=42", url)
        self.assertIn("filter-statut", url)
        self.assertIn("filter-statut-operator=in", url)

    @patch(f"{_ENDPOINT}.get_ts_api_url", return_value="https://wcs.example.be/api")
    def test_query_url_list_contains_all_workflow_statuses(self, _mock):
        endpoint = self._make_endpoint()
        url = endpoint.query_url
        for status in PROJECT_WORKFLOW_STATUS_TO_KEEP:
            self.assertIn(status, url)

    @patch(f"{_ENDPOINT}.get_ts_api_url", return_value="https://wcs.example.be/api")
    def test_query_url_list_appends_extra_form_params(self, _mock):
        endpoint = self._make_endpoint(form={"zone": "nord", "topic": "education"})
        url = endpoint.query_url
        self.assertIn("zone=nord", url)
        self.assertIn("topic=education", url)


# ---------------------------------------------------------------------------
# CampaignEndpoint.get_image
# ---------------------------------------------------------------------------


class TestGetImage(_CampaignViewMixin):

    def test_get_image_returns_none_for_empty_url(self):
        endpoint = self._make_endpoint()
        result = endpoint.get_image("")
        self.assertIsNone(result)

    def test_get_image_returns_none_for_none_url(self):
        endpoint = self._make_endpoint()
        result = endpoint.get_image(None)
        self.assertIsNone(result)

    @patch(f"{_ENDPOINT}.requests.get")
    @patch(
        "plone.api.portal.get_registry_record",
        side_effect=lambda k: {
            "smartweb.iaideabox_api_username": "u",
            "smartweb.iaideabox_api_password": "p",
        }[k],
    )
    def test_get_image_calls_requests_get(self, _mock_reg, mock_get):
        mock_get.return_value = MagicMock(content=b"imgdata")
        endpoint = self._make_endpoint()
        result = endpoint.get_image("http://example.com/img.png")
        mock_get.assert_called_once()
        self.assertEqual(result.content, b"imgdata")

    @patch(f"{_ENDPOINT}.requests.get")
    @patch(
        "plone.api.portal.get_registry_record",
        side_effect=lambda k: {
            "smartweb.iaideabox_api_username": "u",
            "smartweb.iaideabox_api_password": "p",
        }[k],
    )
    def test_get_image_sends_authorization_header(self, _mock_reg, mock_get):
        mock_get.return_value = MagicMock(content=b"img")
        endpoint = self._make_endpoint()
        endpoint.get_image("http://example.com/img.png")
        call_kwargs = mock_get.call_args[1]
        self.assertIn("Authorization", call_kwargs.get("headers", {}))
        self.assertTrue(call_kwargs["headers"]["Authorization"].startswith("Basic "))

    @patch(f"{_ENDPOINT}.requests.get")
    @patch(
        "plone.api.portal.get_registry_record",
        side_effect=lambda k: {
            "smartweb.iaideabox_api_username": "u",
            "smartweb.iaideabox_api_password": "p",
        }[k],
    )
    def test_get_image_sends_accept_header(self, _mock_reg, mock_get):
        mock_get.return_value = MagicMock(content=b"img")
        endpoint = self._make_endpoint()
        endpoint.get_image("http://example.com/img.png")
        call_kwargs = mock_get.call_args[1]
        self.assertEqual(call_kwargs.get("headers", {}).get("Accept"), "image/*")


# ---------------------------------------------------------------------------
# CampaignEndpoint.add_b64_image_to_data
# ---------------------------------------------------------------------------


class TestAddB64Image(_CampaignViewMixin):

    def test_add_b64_image_encodes_content(self):
        endpoint = self._make_endpoint()
        mock_resp = MagicMock()
        mock_resp.content = b"raw_image_bytes"
        expected_b64 = base64.b64encode(b"raw_image_bytes").decode("utf-8")
        data = [
            {
                "fields": {
                    "images_raw": [{"image": {"url": "http://example.com/img.png"}}]
                }
            }
        ]
        with patch.object(endpoint, "get_image", return_value=mock_resp):
            result = endpoint.add_b64_image_to_data(data)
        self.assertEqual(
            result[0]["fields"]["images_raw"][0]["image"]["content"], expected_b64
        )

    def test_add_b64_image_fetches_url_from_fields(self):
        endpoint = self._make_endpoint()
        mock_resp = MagicMock()
        mock_resp.content = b"bytes"
        image_url = "http://example.com/specific-image.png"
        data = [{"fields": {"images_raw": [{"image": {"url": image_url}}]}}]
        with patch.object(
            endpoint, "get_image", return_value=mock_resp
        ) as mock_get_image:
            endpoint.add_b64_image_to_data(data)
        mock_get_image.assert_called_once_with(image_url)

    def test_add_b64_image_processes_all_items(self):
        endpoint = self._make_endpoint()
        mock_resp = MagicMock()
        mock_resp.content = b"img"

        def make_item(url):
            return {"fields": {"images_raw": [{"image": {"url": url}}]}}

        data = [make_item("http://a.com/1.png"), make_item("http://b.com/2.png")]
        with patch.object(endpoint, "get_image", return_value=mock_resp):
            result = endpoint.add_b64_image_to_data(data)
        self.assertEqual(len(result), 2)
        for item in result:
            self.assertIn("content", item["fields"]["images_raw"][0]["image"])


# ---------------------------------------------------------------------------
# ZonesEndpoint
# ---------------------------------------------------------------------------


class TestZonesEndpoint(_CampaignViewMixin):

    def _make_zones_endpoint(self):
        return ZonesEndpoint(self.campaign_view, TestRequest())

    @patch(f"{_ENDPOINT}.get_ts_api_url", return_value="https://wcs.example.be/api")
    def test_query_url_contains_campaign_id(self, _mock):
        endpoint = self._make_zones_endpoint()
        url = endpoint.query_url
        self.assertIn("42", url)
        self.assertIn("imio-ideabox-zone", url)

    def test_call_returns_empty_on_no_json(self):
        endpoint = self._make_zones_endpoint()
        with patch.object(endpoint, "_get_json", return_value=None):
            result = endpoint()
        self.assertEqual(result, {"items": [], "items_total": 0})

    def test_call_returns_items_and_total(self):
        zones = [{"id": "1", "text": "Zone A"}, {"id": "2", "text": "Zone B"}]
        endpoint = self._make_zones_endpoint()
        with patch.object(
            endpoint, "_get_json", return_value={"data": zones, "count": 2}
        ):
            result = endpoint()
        self.assertEqual(result["items"], zones)
        self.assertEqual(result["items_total"], 2)


# ---------------------------------------------------------------------------
# TsTopicsEndpoint
# ---------------------------------------------------------------------------


class TestTsTopicsEndpoint(_CampaignViewMixin):

    def _make_ts_topics_endpoint(self):
        return TsTopicsEndpoint(self.campaign_view, TestRequest())

    @patch(f"{_ENDPOINT}.get_ts_api_url", return_value="https://wcs.example.be/api")
    def test_query_url_contains_campaign_id(self, _mock):
        endpoint = self._make_ts_topics_endpoint()
        url = endpoint.query_url
        self.assertIn("42", url)
        self.assertIn("imio-ideabox-theme", url)

    def test_call_returns_empty_on_no_json(self):
        endpoint = self._make_ts_topics_endpoint()
        with patch.object(endpoint, "_get_json", return_value=None):
            result = endpoint()
        self.assertEqual(result, {"items": [], "items_total": 0})

    def test_call_returns_items_and_total(self):
        topics = [{"id": "1", "text": "Topic 1"}]
        endpoint = self._make_ts_topics_endpoint()
        with patch.object(
            endpoint, "_get_json", return_value={"data": topics, "count": 1}
        ):
            result = endpoint()
        self.assertEqual(result["items"], topics)
        self.assertEqual(result["items_total"], 1)


# ---------------------------------------------------------------------------
# TopicsEndpoint
# ---------------------------------------------------------------------------


class TestTopicsEndpoint(_CampaignViewMixin):

    def _make_topics_endpoint(self):
        return TopicsEndpoint(self.campaign_view, TestRequest())

    def test_call_returns_items_and_items_total(self):
        endpoint = self._make_topics_endpoint()
        result = endpoint()
        self.assertIn("items", result)
        self.assertIn("items_total", result)
        self.assertEqual(result["items_total"], len(result["items"]))

    def test_call_items_have_value_and_title(self):
        endpoint = self._make_topics_endpoint()
        result = endpoint()
        for item in result["items"]:
            self.assertIn("value", item)
            self.assertIn("title", item)


# ---------------------------------------------------------------------------
# AllTopicsEndpoint
# ---------------------------------------------------------------------------


class TestAllTopicsEndpoint(_CampaignViewMixin):

    def _make_all_topics_endpoint(self):
        return AllTopicsEndpoint(self.campaign_view, TestRequest())

    def test_call_combines_vocabulary_and_ts_topics(self):
        endpoint = self._make_all_topics_endpoint()
        ts_mock = {"items": [{"id": "ts1", "text": "TS Topic"}], "items_total": 1}
        with patch.object(TsTopicsEndpoint, "__call__", return_value=ts_mock):
            result = endpoint()
        titles = [item["title"] for item in result["items"]]
        self.assertIn("TS Topic", titles)

    def test_call_items_total_reflects_combined_count(self):
        endpoint = self._make_all_topics_endpoint()
        ts_mock = {
            "items": [{"id": "ts1", "text": "A"}, {"id": "ts2", "text": "B"}],
            "items_total": 2,
        }
        with patch.object(TsTopicsEndpoint, "__call__", return_value=ts_mock):
            result = endpoint()
        self.assertEqual(result["items_total"], len(result["items"]))

    def test_call_result_is_sorted_by_title(self):
        endpoint = self._make_all_topics_endpoint()
        ts_mock = {
            "items": [{"id": "z", "text": "Zzz"}, {"id": "a", "text": "Aaa"}],
            "items_total": 2,
        }
        with patch.object(TsTopicsEndpoint, "__call__", return_value=ts_mock):
            result = endpoint()
        titles = [item["title"] for item in result["items"]]
        self.assertEqual(titles, sorted(titles, key=lambda t: t.lower()))


# ---------------------------------------------------------------------------
# Service classes (reply())
# ---------------------------------------------------------------------------


class TestServiceClasses(_CampaignViewMixin):
    """Service classes are thin wrappers around endpoint __call__.

    <plone:service> creates a BrowserView subclass in ZCA, but the imported
    class has no __init__.  We bypass this by using __new__ + manual attribute
    assignment so we can test reply() in isolation.
    """

    def _make_service(self, cls):
        svc = object.__new__(cls)
        svc.context = self.campaign_view
        svc.request = TestRequest()
        return svc

    def test_campaign_endpoint_get_reply(self):
        service = self._make_service(CampaignEndpointGet)
        with patch.object(
            CampaignEndpoint, "__call__", return_value={"items": [], "items_total": 0}
        ):
            result = service.reply()
        self.assertEqual(result, {"items": [], "items_total": 0})

    @patch(
        "plone.api.portal.get_registry_record",
        side_effect=lambda k: {
            "smartweb.iaideabox_api_username": "u",
            "smartweb.iaideabox_api_password": "p",
        }[k],
    )
    def test_auth_campaign_endpoint_get_reply(self, _mock):
        service = self._make_service(AuthCampaignEndpointGet)
        result = service.reply()
        self.assertTrue(result.startswith("Basic "))

    def test_zones_endpoint_get_reply(self):
        service = self._make_service(ZonesEndpointGet)
        with patch.object(
            ZonesEndpoint, "__call__", return_value={"items": [], "items_total": 0}
        ):
            result = service.reply()
        self.assertEqual(result["items_total"], 0)

    def test_ts_topics_endpoint_get_reply(self):
        # TsTopicsEndpointGet.reply() delegates to ZonesEndpoint (see source)
        service = self._make_service(TsTopicsEndpointGet)
        with patch.object(
            ZonesEndpoint, "__call__", return_value={"items": [], "items_total": 0}
        ):
            result = service.reply()
        self.assertIn("items", result)

    def test_topics_endpoint_get_reply(self):
        service = self._make_service(TopicsEndpointGet)
        result = service.reply()
        self.assertIn("items", result)
        self.assertIn("items_total", result)

    def test_all_topics_endpoint_get_reply(self):
        service = self._make_service(AllTopicsEndpointGet)
        ts_mock = {"items": [], "items_total": 0}
        with patch.object(TsTopicsEndpoint, "__call__", return_value=ts_mock):
            result = service.reply()
        self.assertIn("items", result)
