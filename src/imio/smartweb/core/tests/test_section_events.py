# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from datetime import datetime
from freezegun import freeze_time
from imio.smartweb.core import config
from imio.smartweb.core.browser.forms import SectionEventsCustomEditForm
from imio.smartweb.core.contents import ISectionEvents
from imio.smartweb.core.contents.sections.views import SECTION_ITEMS_HASH_KEY
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.tests.utils import get_json
from imio.smartweb.core.tests.utils import mock_agenda_scope
from imio.smartweb.core.tests.utils import mock_entity_agendas
from plone import api
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.z3cform.interfaces import IPloneFormLayer
from plone.dexterity.browser.add import DefaultAddForm
from plone.testing.zope import Browser
from time import sleep
from z3c.form.browser.radio import RadioFieldWidget
from z3c.relationfield import RelationValue
from zope.annotation.interfaces import IAnnotations
from zope.component import getUtility
from zope.component import queryMultiAdapter
from zope.interface import alsoProvides
from zope.interface import Invalid
from zope.intid.interfaces import IIntIds
from zope.publisher.browser import TestRequest
from zope.schema.interfaces import IVocabularyFactory

import json
import re
import requests_mock
import transaction


class TestSectionEvents(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

    def setUp(self):
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.portalpage = api.content.create(
            container=self.portal,
            type="imio.smartweb.PortalPage",
            id="Portal page",
        )
        self.json_events = get_json("resources/json_rest_events.json")
        self.json_specific_event = get_json("resources/json_rest_specific_events.json")
        self.rest_events_view = api.content.create(
            container=self.portal,
            type="imio.smartweb.EventsView",
            title="Rest events view",
        )
        self.events = api.content.create(
            container=self.portalpage,
            type="imio.smartweb.SectionEvents",
            title="My events",
        )

    @requests_mock.Mocker()
    @freeze_time("2021-11-15")
    def test_events(self, m):
        intids = getUtility(IIntIds)
        self.events.related_events = "e73e6a81afea4a579cd0da2773af8d29"
        self.events.linking_rest_view = RelationValue(
            intids.getId(self.rest_events_view)
        )
        view = queryMultiAdapter((self.portalpage, self.request), name="full_view")
        self.assertIn("My events", view())
        events_view = queryMultiAdapter(
            (self.events, self.request), name="carousel_view"
        )
        self.assertEqual(events_view.items, [])
        url = "http://localhost:8080/Plone/@events?selected_agendas=e73e6a81afea4a579cd0da2773af8d29&metadata_fields=container_uid&metadata_fields=category_title&metadata_fields=local_category&metadata_fields=topics&metadata_fields=start&metadata_fields=end&metadata_fields=has_leadimage&metadata_fields=modified&metadata_fields=UID&event_dates.query=2021-11-15&event_dates.range=min&b_size=6&translated_in_en=1&sort_on=event_dates"
        m.get(url, text=json.dumps(self.json_events))
        self.assertEqual(events_view.items[0][0].get("title"), "Journée de l'ATL")
        self.assertEqual(len(events_view.items[0]), 2)
        self.events.events_source = "selection"
        self.events.specific_related_events = ["1178188bddde4ced95a6cf8bf04c443c"]
        url = "http://localhost:8080/Plone/@events?UID=1178188bddde4ced95a6cf8bf04c443c&metadata_fields=container_uid&metadata_fields=category_title&metadata_fields=local_category&metadata_fields=topics&metadata_fields=start&metadata_fields=end&metadata_fields=has_leadimage&metadata_fields=modified&metadata_fields=UID&event_dates.query=2021-11-15&event_dates.range=min&b_size=6&translated_in_en=1"
        m.get(url, text=json.dumps(self.json_specific_event))
        self.assertEqual(len(events_view.items[0]), 1)
        self.assertEqual(events_view.items[0][0].get("title"), "Bonne cheville")

    @requests_mock.Mocker()
    @freeze_time("2021-11-15")
    def test_events_source(self, m):
        intids = getUtility(IIntIds)
        self.events.related_events = "e73e6a81afea4a579cd0da2773af8d29"
        self.events.linking_rest_view = RelationValue(
            intids.getId(self.rest_events_view)
        )
        self.events.specific_related_events = ["1178188bddde4ced95a6cf8bf04c443c"]
        agenda_url = "http://localhost:8080/Plone/@events?selected_agendas=e73e6a81afea4a579cd0da2773af8d29&metadata_fields=container_uid&metadata_fields=category_title&metadata_fields=local_category&metadata_fields=topics&metadata_fields=start&metadata_fields=end&metadata_fields=has_leadimage&metadata_fields=modified&metadata_fields=UID&event_dates.query=2021-11-15&event_dates.range=min&b_size=6&translated_in_en=1&sort_on=event_dates"
        m.get(agenda_url, text=json.dumps(self.json_events))
        selection_url = "http://localhost:8080/Plone/@events?UID=1178188bddde4ced95a6cf8bf04c443c&metadata_fields=container_uid&metadata_fields=category_title&metadata_fields=local_category&metadata_fields=topics&metadata_fields=start&metadata_fields=end&metadata_fields=has_leadimage&metadata_fields=modified&metadata_fields=UID&event_dates.query=2021-11-15&event_dates.range=min&b_size=6&translated_in_en=1"
        m.get(selection_url, text=json.dumps(self.json_specific_event))
        events_view = queryMultiAdapter(
            (self.events, self.request), name="carousel_view"
        )
        # the agenda is the default source: hand-picked events stay dormant
        self.assertEqual(self.events.events_source, "agenda")
        self.assertEqual(len(events_view.items[0]), 2)
        self.assertEqual(events_view.items[0][0].get("title"), "Journée de l'ATL")
        # switching the source is what activates the hand-picked selection
        self.events.events_source = "selection"
        self.assertEqual(len(events_view.items[0]), 1)
        self.assertEqual(events_view.items[0][0].get("title"), "Bonne cheville")

    @freeze_time("2021-11-15")
    @requests_mock.Mocker()
    def test_hand_picked_items_link_to_the_default_events_view(self, m):
        # A hand-picked event is put forward whatever agenda it sits in, so it
        # cannot link to linking_rest_view (which shows one agenda plus the ones
        # populating it). It links to the control panel's default events view,
        # and BaseEventsEndpoint retries unscoped by UID so the detail page
        # resolves.
        intids = getUtility(IIntIds)
        self.events.related_events = "e73e6a81afea4a579cd0da2773af8d29"
        self.events.linking_rest_view = RelationValue(
            intids.getId(self.rest_events_view)
        )
        self.events.events_source = "selection"
        self.events.specific_related_events = ["1178188bddde4ced95a6cf8bf04c443c"]
        selection_url = "http://localhost:8080/Plone/@events?UID=1178188bddde4ced95a6cf8bf04c443c&metadata_fields=container_uid&metadata_fields=category_title&metadata_fields=local_category&metadata_fields=topics&metadata_fields=start&metadata_fields=end&metadata_fields=has_leadimage&metadata_fields=modified&metadata_fields=UID&event_dates.query=2021-11-15&event_dates.range=min&b_size=6&translated_in_en=1"
        m.get(selection_url, text=json.dumps(self.json_specific_event))
        default_view = api.content.create(
            container=self.portal,
            type="imio.smartweb.EventsView",
            title="Default events view",
        )
        events_view = queryMultiAdapter(
            (self.events, self.request), name="carousel_view"
        )

        # no default events view configured yet: nothing to link to. The linking
        # view is NOT used as a fallback -- it plays no part in this mode, and
        # the invariant refuses to save such a section in the first place.
        self.assertEqual(events_view.item_view_url, "")
        self.assertEqual(events_view.see_all_url, "")

        api.portal.set_registry_record(
            "smartweb.default_events_view", default_view.UID()
        )
        events_view = queryMultiAdapter(
            (self.events, self.request), name="carousel_view"
        )
        self.assertTrue(
            events_view.items[0][0]["url"].startswith(default_view.absolute_url())
        )
        # "see all" goes to the same default view, not to the linking view
        self.assertEqual(events_view.see_all_url, default_view.absolute_url())

        # an agenda section is unaffected: its items stay on the linking view
        agenda_url = "http://localhost:8080/Plone/@events?selected_agendas=e73e6a81afea4a579cd0da2773af8d29&metadata_fields=container_uid&metadata_fields=category_title&metadata_fields=local_category&metadata_fields=topics&metadata_fields=start&metadata_fields=end&metadata_fields=has_leadimage&metadata_fields=modified&metadata_fields=UID&event_dates.query=2021-11-15&event_dates.range=min&b_size=6&translated_in_en=1&sort_on=event_dates"
        m.get(agenda_url, text=json.dumps(self.json_events))
        self.events.events_source = "agenda"
        events_view = queryMultiAdapter(
            (self.events, self.request), name="carousel_view"
        )
        self.assertTrue(
            events_view.items[0][0]["url"].startswith(
                self.rest_events_view.absolute_url()
            )
        )
        self.assertEqual(events_view.see_all_url, self.rest_events_view.absolute_url())

    def test_events_source_invariant(self):
        class Data:
            events_source = "selection"
            linking_rest_view = None
            related_events = "e73e6a81afea4a579cd0da2773af8d29"
            specific_related_events = []

        # "selection" without a single event picked is not a usable section
        with self.assertRaises(Invalid):
            ISectionEvents.validateInvariants(Data())

        Data.specific_related_events = ["1178188bddde4ced95a6cf8bf04c443c"]
        # ...nor is it while the control panel has no default events view: that
        # is where a hand-picked item links, linking_rest_view plays no part
        with self.assertRaises(Invalid):
            ISectionEvents.validateInvariants(Data())

        default_view = api.content.create(
            container=self.portal,
            type="imio.smartweb.EventsView",
            title="Default events view",
        )
        api.portal.set_registry_record(
            "smartweb.default_events_view", default_view.UID()
        )
        # a hand-picked section validates without any linking view
        ISectionEvents.validateInvariants(Data())

        # "agenda" needs a linking view, since that is what scopes it
        Data.events_source = "agenda"
        with self.assertRaises(Invalid):
            ISectionEvents.validateInvariants(Data())

        intids = getUtility(IIntIds)
        Data.linking_rest_view = RelationValue(intids.getId(self.rest_events_view))

        # ...and an agenda
        Data.related_events = None
        with self.assertRaises(Invalid):
            ISectionEvents.validateInvariants(Data())

        Data.related_events = "e73e6a81afea4a579cd0da2773af8d29"
        ISectionEvents.validateInvariants(Data())

    def test_linking_rest_view_comes_first(self):
        # the two source fields are scoped by the linking view, so the editor
        # has to choose it before them
        names = list(ISectionEvents.names(all=False))
        self.assertLess(names.index("linking_rest_view"), names.index("events_source"))
        self.assertLess(names.index("events_source"), names.index("related_events"))
        self.assertLess(
            names.index("related_events"), names.index("specific_related_events")
        )

    @requests_mock.Mocker()
    def test_events_source_invariant_rejects_an_out_of_scope_agenda(self, m):
        agenda_uid = "aaaa0000aaaa0000aaaa0000aaaa0005"
        mock_agenda_scope(m, agenda_uid, populating=[("in-scope-uid", "CPAS")])
        self.rest_events_view.selected_agenda = agenda_uid

        intids = getUtility(IIntIds)
        self.events.linking_rest_view = RelationValue(
            intids.getId(self.rest_events_view)
        )

        class Data:
            events_source = "agenda"
            linking_rest_view = None
            related_events = "out-of-scope-uid"
            specific_related_events = []

        Data.linking_rest_view = self.events.linking_rest_view

        with self.assertRaises(Invalid):
            ISectionEvents.validateInvariants(Data())

        Data.related_events = "in-scope-uid"
        ISectionEvents.validateInvariants(Data())

    def test_events_source_radio_widget(self):
        # browser/static/src/edit.js hides the field that does not match the
        # chosen source, addressing the radio inputs by name and switching on
        # their value, so both must keep the shape the script expects.
        widget = RadioFieldWidget(
            ISectionEvents["events_source"].bind(self.events), self.request
        )
        widget.id = "form-widgets-events_source"
        widget.name = "form.widgets.events_source"
        widget.update()
        soup = BeautifulSoup(widget.render())
        radios = soup.find_all("input", {"type": "radio"})
        self.assertEqual(
            [radio["name"] for radio in radios],
            ["form.widgets.events_source", "form.widgets.events_source"],
        )
        self.assertEqual([radio["value"] for radio in radios], ["agenda", "selection"])

    @requests_mock.Mocker()
    def test_edit_js_dom_contract(self, m):
        # browser/static/src/edit.js addresses these three widgets by id and
        # relies on their pattern classes. A change here silently breaks the
        # cascade, so pin it.
        # rendering the form binds specific_related_events, hence the
        # entity-wide EventsFromEntity vocabulary
        mock_entity_agendas(m)
        m.get(
            re.compile(re.escape(config.EVENTS_URL) + r"/@search\?selected_agendas="),
            text=json.dumps({"items": []}),
        )
        transaction.commit()
        browser = Browser(self.layer["app"])
        browser.handleErrors = False
        browser.addHeader(
            "Authorization", "Basic %s:%s" % (TEST_USER_NAME, TEST_USER_PASSWORD)
        )
        browser.open(
            "{}/++add++imio.smartweb.SectionEvents".format(
                self.portalpage.absolute_url()
            )
        )
        soup = BeautifulSoup(browser.contents, "html.parser")

        linking = soup.find(id="form-widgets-linking_rest_view")
        self.assertIn("pat-contentbrowser", linking["class"])

        related = soup.find(id="form-widgets-related_events")
        self.assertEqual(related.name, "select")
        self.assertIn("pat-select2", related["class"])

        specific = soup.find(id="form-widgets-specific_related_events")
        self.assertIn("pat-select2", specific["class"])
        self.assertIn("@@getVocabulary", specific["data-pat-select2"])

    @requests_mock.Mocker()
    def test_events_source_invariant_on_edit_form(self, m):
        # the invariant must surface as a form error on a real submission, not
        # only when called directly: this is what stops an editor saving
        # "selection" with an empty selection.
        m.get(
            f"{config.EVENTS_URL}/@search?UID=7c69f9a738ec497c819725c55888ee31",
            text=json.dumps(get_json("resources/json_events_entities_raw_mock.json")),
        )
        m.get(
            f"{config.EVENTS_URL}/imio-events-entity/@search?portal_type=imio.events.Agenda&sort_on=sortable_title&b_size=1000000&metadata_fields=UID",
            text=json.dumps(get_json("resources/json_events_agendas_raw_mock.json")),
        )
        agenda_uid = "64f4cbee9a394a018a951f6d94452914"
        mock_agenda_scope(m, agenda_uid)
        self.rest_events_view.selected_agenda = agenda_uid
        # the ScopedAgendas vocabulary resolves the linking view either from
        # the request or, failing that, from the context -- the edit form's
        # context is self.events, so setting it there is what puts agenda_uid
        # in scope for the widget validating the submission below.
        intids = getUtility(IIntIds)
        self.events.linking_rest_view = RelationValue(
            intids.getId(self.rest_events_view)
        )

        def submit(source):
            form_data = {
                "form.widgets.title": "My events",
                "form.widgets.events_source": [source],
                "form.widgets.events_source-empty-marker": "1",
                "form.widgets.related_events": [agenda_uid],
                "form.widgets.specific_related_events": [],
                "form.widgets.linking_rest_view": [self.rest_events_view.UID()],
                "form.widgets.nb_results_by_batch": ["3"],
                "form.widgets.max_nb_batches": "2",
                "form.widgets.link_text": "See all events",
                "form.widgets.ICategoryDisplay.show_categories_or_topics": ["category"],
                "form.widgets.IOrientation.orientation": ["paysage"],
            }
            request = TestRequest(form=form_data)
            alsoProvides(request, IPloneFormLayer)
            form = SectionEventsCustomEditForm(self.events, request)
            form.update()
            data, errors = form.extractData()
            return [getattr(error, "message", None) or str(error) for error in errors]

        # "selection" with nothing picked is refused...
        self.assertEqual(submit("selection"), ["Please select at least one event."])
        # ...while the very same submission on the agenda source goes through
        self.assertEqual(submit("agenda"), [])

    @requests_mock.Mocker()
    def test_out_of_scope_agenda_is_refused_by_the_edit_form(self, m):
        # the invariant must fire on a REAL submission. On the form path
        # data.linking_rest_view is the EventsView itself, not a RelationValue
        # (RelationChoiceContentBrowserWidgetConverter.toFieldValue returns
        # res[0].getObject()), so reading only ``.to_object`` left the scope
        # empty and the "scope and" guard skipped the whole check -- a
        # misconfigured section saved happily. The hand-built RelationValue test
        # above could never catch that, since the form never produces that
        # shape.
        agenda_uid = "aaaa0000aaaa0000aaaa0000aaaa0010"
        mock_agenda_scope(m, agenda_uid, populating=[("in-scope-uid", "CPAS")])
        # the form prunes specific_related_events on update(), which builds the
        # entity-wide EventsFromEntity vocabulary
        mock_entity_agendas(m)
        m.get(
            re.compile(re.escape(config.EVENTS_URL) + r"/@search\?selected_agendas="),
            text=json.dumps({"items": []}),
        )
        self.rest_events_view.selected_agenda = agenda_uid
        intids = getUtility(IIntIds)
        self.events.linking_rest_view = RelationValue(
            intids.getId(self.rest_events_view)
        )
        # storing the bad agenda is what keeps it offered by the ScopedAgendas
        # vocabulary, so the widget accepts it and the invariant is the only
        # thing standing between it and a saved, permanently broken section
        self.events.related_events = "out-of-scope-uid"

        def submit(agenda):
            form_data = {
                "form.widgets.title": "My events",
                "form.widgets.events_source": ["agenda"],
                "form.widgets.events_source-empty-marker": "1",
                "form.widgets.related_events": [agenda],
                "form.widgets.specific_related_events": [],
                "form.widgets.linking_rest_view": [self.rest_events_view.UID()],
                "form.widgets.nb_results_by_batch": ["3"],
                "form.widgets.max_nb_batches": "2",
                "form.widgets.link_text": "See all events",
                "form.widgets.ICategoryDisplay.show_categories_or_topics": ["category"],
                "form.widgets.IOrientation.orientation": ["paysage"],
            }
            request = TestRequest(form=form_data)
            alsoProvides(request, IPloneFormLayer)
            form = SectionEventsCustomEditForm(self.events, request)
            form.update()
            data, errors = form.extractData()
            return [getattr(error, "message", None) or str(error) for error in errors]

        self.assertEqual(
            submit("out-of-scope-uid"),
            ["This agenda is not displayed by the selected events view."],
        )
        # an agenda populating the view's own agenda goes through
        self.assertEqual(submit("in-scope-uid"), [])

    @requests_mock.Mocker()
    def test_events_source_invariant_on_add_form(self, m):
        # the add form is the harsher case: its context is the container, so an
        # invariant reaching for a field the current validation pass does not
        # carry reads it off the PortalPage instead of the section.
        m.get(
            f"{config.EVENTS_URL}/@search?UID=7c69f9a738ec497c819725c55888ee31",
            text=json.dumps(get_json("resources/json_events_entities_raw_mock.json")),
        )
        m.get(
            f"{config.EVENTS_URL}/imio-events-entity/@search?portal_type=imio.events.Agenda&sort_on=sortable_title&b_size=1000000&metadata_fields=UID",
            text=json.dumps(get_json("resources/json_events_agendas_raw_mock.json")),
        )
        agenda_uid = "aaaa0000aaaa0000aaaa0000aaaa0006"
        mock_agenda_scope(m, agenda_uid)
        self.rest_events_view.selected_agenda = agenda_uid
        request = TestRequest(
            form={
                "form.widgets.title": "My events",
                "form.widgets.events_source": ["agenda"],
                "form.widgets.events_source-empty-marker": "1",
                "form.widgets.related_events": [agenda_uid],
                "form.widgets.specific_related_events": [],
                "form.widgets.linking_rest_view": [self.rest_events_view.UID()],
                "form.widgets.nb_results_by_batch": ["3"],
                "form.widgets.max_nb_batches": "2",
                "form.widgets.link_text": "See all events",
                "form.widgets.ICategoryDisplay.show_categories_or_topics": ["category"],
                "form.widgets.IOrientation.orientation": ["paysage"],
            }
        )
        alsoProvides(request, IPloneFormLayer)
        # the add form's context is the container (self.portalpage), which has
        # no linking_rest_view to fall back on, so the ScopedAgendas vocabulary
        # can only find the linking view through the request -- but it reads
        # the *global* one via getRequest(), not this locally built one, so it
        # is set here too, exactly as the linking view's own widget submission
        # does for a real request.
        self.request.form["linking_rest_view"] = self.rest_events_view.UID()
        try:
            form = DefaultAddForm(self.portalpage, request)
            form.portal_type = "imio.smartweb.SectionEvents"
            form.update()
            data, errors = form.extractData()
        finally:
            del self.request.form["linking_rest_view"]
        messages = [getattr(error, "message", None) or str(error) for error in errors]
        self.assertEqual(messages, [])

    @requests_mock.Mocker()
    def test_specific_related_events_survive_remote_outage(self, m):
        # WEB-4338's cleanup prunes any stored uid the vocabulary doesn't
        # recognize, merely on opening the edit form. An empty
        # EventsFromEntity vocabulary means "cannot tell" -- here, the remote
        # being unreachable -- never "every stored value is invalid": it must
        # not silently wipe a hand-picked selection.
        m.get(
            f"{config.EVENTS_URL}/@search?UID=7c69f9a738ec497c819725c55888ee31",
            text=json.dumps(get_json("resources/json_events_entities_raw_mock.json")),
        )
        m.get(
            f"{config.EVENTS_URL}/imio-events-entity/@search?portal_type=imio.events.Agenda&sort_on=sortable_title&b_size=1000000&metadata_fields=UID",
            text=json.dumps(get_json("resources/json_events_agendas_raw_mock.json")),
        )
        intids = getUtility(IIntIds)
        self.rest_events_view.selected_agenda = "aaaa0000aaaa0000aaaa0000aaaa0099"
        self.events.linking_rest_view = RelationValue(
            intids.getId(self.rest_events_view)
        )
        self.events.events_source = "selection"
        self.events.specific_related_events = [
            "1178188bddde4ced95a6cf8bf04c443c",
            "97902f2e26774a369035117d56381a2a",
        ]
        m.get(
            re.compile(re.escape(config.EVENTS_URL) + r"/@search\?selected_agendas="),
            status_code=503,
        )
        request = TestRequest()
        alsoProvides(request, IPloneFormLayer)
        form = SectionEventsCustomEditForm(self.events, request)
        form.update()
        self.assertEqual(
            self.events.specific_related_events,
            [
                "1178188bddde4ced95a6cf8bf04c443c",
                "97902f2e26774a369035117d56381a2a",
            ],
        )

    @requests_mock.Mocker()
    def test_events_modified(self, m):
        today = datetime.now()
        today_str = today.strftime("%Y-%m-%d")
        intids = getUtility(IIntIds)
        self.events.related_events = "e73e6a81afea4a579cd0da2773af8d29"
        self.events.linking_rest_view = RelationValue(
            intids.getId(self.rest_events_view)
        )
        annotations = IAnnotations(self.events)
        self.assertIsNone(annotations.get(SECTION_ITEMS_HASH_KEY))

        events_view = queryMultiAdapter(
            (self.events, self.request), name="carousel_view"
        )
        url = f"http://localhost:8080/Plone/@events?selected_agendas=e73e6a81afea4a579cd0da2773af8d29&metadata_fields=container_uid&metadata_fields=category_title&metadata_fields=local_category&metadata_fields=topics&metadata_fields=start&metadata_fields=end&metadata_fields=has_leadimage&metadata_fields=modified&metadata_fields=UID&event_dates.query={today_str}&event_dates.range=min&b_size=6&translated_in_en=1&sort_on=event_dates"
        m.get(url, text=json.dumps(self.json_events))
        self.assertEqual(len(events_view.items[0]), 2)
        hash_1 = annotations.get(SECTION_ITEMS_HASH_KEY)
        self.assertIsNotNone(hash_1)
        first_modification = self.portalpage.ModificationDate()

        sleep(1)
        url = f"http://localhost:8080/Plone/@events?selected_agendas=e73e6a81afea4a579cd0da2773af8d29&metadata_fields=container_uid&metadata_fields=category_title&metadata_fields=local_category&metadata_fields=topics&metadata_fields=start&metadata_fields=end&metadata_fields=has_leadimage&metadata_fields=modified&metadata_fields=UID&event_dates.query={today_str}&event_dates.range=min&b_size=6&translated_in_en=1&sort_on=event_dates"
        m.get(url, text="{}")
        self.assertEqual(len(events_view.items), 0)
        next_modification = self.portalpage.ModificationDate()
        hash_2 = annotations.get(SECTION_ITEMS_HASH_KEY)
        self.assertNotEqual(hash_1, hash_2)
        self.assertNotEqual(first_modification, next_modification)

        sleep(1)
        self.assertEqual(len(events_view.items), 0)
        last_modification = self.portalpage.ModificationDate()
        hash_3 = annotations.get(SECTION_ITEMS_HASH_KEY)
        self.assertEqual(hash_2, hash_3)
        self.assertEqual(next_modification, last_modification)

    @requests_mock.Mocker()
    def test_events_not_modified_for_anonymous(self, m):
        intids = getUtility(IIntIds)
        self.events.related_events = "e73e6a81afea4a579cd0da2773af8d29"
        self.events.linking_rest_view = RelationValue(
            intids.getId(self.rest_events_view)
        )
        m.get("http://localhost:8080/Plone/@events", text=json.dumps(self.json_events))
        annotations = IAnnotations(self.events)
        first_modification = self.portalpage.ModificationDate()

        logout()
        events_view = queryMultiAdapter(
            (self.events, self.request), name="carousel_view"
        )
        self.assertEqual(len(events_view.items[0]), 2)
        self.assertIsNone(annotations.get(SECTION_ITEMS_HASH_KEY))
        self.assertEqual(self.portalpage.ModificationDate(), first_modification)

    @requests_mock.Mocker()
    def test_orientation(self, m):
        today = datetime.now()
        today_str = today.strftime("%Y-%m-%d")
        intids = getUtility(IIntIds)
        self.events.related_events = "e73e6a81afea4a579cd0da2773af8d29"
        self.events.linking_rest_view = RelationValue(
            intids.getId(self.rest_events_view)
        )
        events_view = queryMultiAdapter(
            (self.events, self.request), name="carousel_view"
        )
        url = f"http://localhost:8080/Plone/@events?selected_agendas=e73e6a81afea4a579cd0da2773af8d29&metadata_fields=container_uid&metadata_fields=category_title&metadata_fields=local_category&metadata_fields=topics&metadata_fields=start&metadata_fields=end&metadata_fields=has_leadimage&metadata_fields=modified&metadata_fields=UID&event_dates.query={today_str}&event_dates.range=min&b_size=6&translated_in_en=1&sort_on=event_dates"
        m.get(url, text=json.dumps(self.json_events))

        self.assertIn("paysage_vignette", events_view.items[0][0]["image"])
        self.events.orientation = "portrait"
        self.assertIn("portrait_vignette", events_view.items[0][0]["image"])

    @requests_mock.Mocker()
    def test_show_categories_or_topics(self, m):
        today = datetime.now()
        today_str = today.strftime("%Y-%m-%d")
        intids = getUtility(IIntIds)
        self.events.related_events = "e73e6a81afea4a579cd0da2773af8d29"
        self.events.linking_rest_view = RelationValue(
            intids.getId(self.rest_events_view)
        )
        events_view = queryMultiAdapter(
            (self.events, self.request), name="carousel_view"
        )
        url = f"http://localhost:8080/Plone/@events?selected_agendas=e73e6a81afea4a579cd0da2773af8d29&metadata_fields=container_uid&metadata_fields=category_title&metadata_fields=local_category&metadata_fields=topics&metadata_fields=start&metadata_fields=end&metadata_fields=has_leadimage&metadata_fields=modified&metadata_fields=UID&event_dates.query={today_str}&event_dates.range=min&b_size=6&translated_in_en=1&sort_on=event_dates"
        m.get(url, text=json.dumps(self.json_events))
        self.assertEqual(events_view.items[0][0]["category"], "Local Category title")
        self.assertEqual(events_view.items[0][1]["category"], "Presse")
        self.events.show_categories_or_topics = "category"
        self.assertEqual(events_view.items[0][0]["category"], "Local Category title")
        self.events.show_categories_or_topics = "topic"
        self.assertEqual(events_view.items[0][0]["category"], "Education")
        self.events.show_categories_or_topics = ""
        self.assertEqual(events_view.items[0][0]["category"], "")

    @requests_mock.Mocker()
    @freeze_time("2026-05-13")
    def test_whole_day_dates_converted_to_brussels_timezone(self, m):
        # Régression: un événement whole_day stocké comme 16/05 00:00→23:59
        # Bruxelles (= 15/05 22:00→16/05 21:59:59 UTC en CEST) s'affichait
        # "du 15/05 au 17/05" parce que view.py utilisait les datetimes UTC
        # bruts avec strftime('%d') dans macros.pt. Le rendu doit utiliser
        # le jour en TZ Europe/Brussels.
        intids = getUtility(IIntIds)
        self.events.related_events = "e73e6a81afea4a579cd0da2773af8d29"
        self.events.linking_rest_view = RelationValue(
            intids.getId(self.rest_events_view)
        )
        payload = {
            "items": [
                {
                    "@id": "http://localhost:8080/Plone/test-event",
                    "UID": "test-whole-day-uid",
                    "title": "Whole Day Event",
                    "description": "Test",
                    "start": "2026-05-15T22:00:00+00:00",
                    "end": "2026-05-16T21:59:59+00:00",
                    "modified": "2026-05-13T10:00:00+00:00",
                    "has_leadimage": False,
                }
            ]
        }
        m.get(
            requests_mock.ANY,
            text=json.dumps(payload),
        )
        events_view = queryMultiAdapter(
            (self.events, self.request), name="carousel_view"
        )
        item = events_view.items[0][0]
        start = item["event_date"]["start"]
        end = item["event_date"]["end"]
        # Bug si view.py ne fait pas astimezone(Europe/Brussels):
        # start.day == 15 (UTC) au lieu de 16 (Brussels)
        self.assertEqual(
            start.day,
            16,
            f"start.day doit être 16 en TZ Brussels, reçu {start.day} "
            f"(tzinfo={start.tzinfo}, raw={start.isoformat()})",
        )
        # Idem pour end: en UTC c'est 16/05 21:59:59, en Brussels 16/05 23:59:59
        self.assertEqual(end.day, 16)
        # is_multi_dates doit retourner False car les deux sont sur le 16/05
        # en TZ Brussels (donc macros.pt rend "On 16" et non "From 15 to 16").
        self.assertFalse(events_view.is_multi_dates(start, end))

    def test_linking_rest_view_vocabulary_is_site_wide(self):
        # Regression: a SectionEvents inside a minisite (INavigationRoot) must
        # accept a linking_rest_view pointing to an EventsView located outside
        # the minisite. With the navigation-root-scoped Catalog vocabulary
        # that was used before, validation raised ConstraintNotSatisfied.
        from imio.smartweb.core.behaviors.minisite import IImioSmartwebMinisite
        from zope.interface import alsoProvides

        minisite = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            id="minisite",
        )
        alsoProvides(minisite, IImioSmartwebMinisite)
        page = api.content.create(
            container=minisite,
            type="imio.smartweb.PortalPage",
            id="home",
        )
        section = api.content.create(
            container=page,
            type="imio.smartweb.SectionEvents",
            title="Section in minisite",
        )

        factory = getUtility(
            IVocabularyFactory, "imio.smartweb.vocabulary.EventsViewsSite"
        )
        vocabulary = factory(section)
        self.assertIn(api.content.get_uuid(self.rest_events_view), vocabulary)

    def test_linking_rest_view_only_accepts_an_events_view(self):
        # with the Catalog vocabulary this field accepted any content, and the
        # scoping then silently degraded to no scope at all
        page = api.content.create(
            container=self.portal, type="imio.smartweb.PortalPage", id="not-a-view"
        )
        field = ISectionEvents["linking_rest_view"].bind(self.events)
        field.validate(self.rest_events_view)
        with self.assertRaises(Invalid):
            field.validate(page)
