from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from plone.app.z3cform.interfaces import IPloneFormLayer
from z3c.form.browser.text import TextWidget
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import IWidget
from z3c.form.widget import FieldWidget
from zope.component import adapter
from zope.i18n import translate
from zope.interface import implementer
from zope.interface import implementer_only
from zope.schema.interfaces import ITextLine


class ISuggestedIATitlesWidget(IWidget):
    pass


@implementer_only(ISuggestedIATitlesWidget)
class SuggestedIATitlesWidget(TextWidget):
    klass = "text-widget form-control suggestedtitles-with-button"

    def update(self):
        super().update()
        self.pattern_options = {
            "sourceSelector": "#form-widgets-title",
            "buttonLabel": "Get titles",
        }

    @property
    def data_pat_plone_modal(self):
        language = api.portal.get_current_language(context=self.context)
        title = translate(_("Title suggestions"), target_language=language)
        return f"title: {title}; width: 600; loadLinksWithinModal: false"


@implementer(IFieldWidget)
@adapter(ITextLine, IPloneFormLayer)
def SuggestedIATitlesFieldWidget(field, request) -> IFieldWidget:
    return FieldWidget(field, SuggestedIATitlesWidget(request))
