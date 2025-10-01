from z3c.form.browser.text import TextWidget
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import IFormLayer
from z3c.form.interfaces import IWidget
from z3c.form.widget import FieldWidget
from zope.component import adapter
from zope.interface import implementer
from zope.interface import implementer_only
from zope.schema.interfaces import ITextLine

from plone.app.z3cform.interfaces import IPloneFormLayer


class ISuggestedIATitlesWidget(IWidget):
    pass


@implementer_only(ISuggestedIATitlesWidget)
class SuggestedIATitlesWidget(TextWidget):
    klass = "text-widget form-control slugify-with-button"

    def update(self):
        super().update()
        self.pattern_options = {
            "sourceSelector": "#form-widgets-title",
            "buttonLabel": "Get titles",
        }


@implementer(IFieldWidget)
@adapter(ITextLine, IPloneFormLayer)
def SuggestedIATitlesFieldWidget(field, request) -> IFieldWidget:
    return FieldWidget(field, SuggestedIATitlesWidget(request))
