from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.registry.field import Text as PersistentText
from plone.registry.field import TextLine as PersistentTextLine
from plone.registry.interfaces import IPersistentField
from plone import api
from plone.app.z3cform.interfaces import IPloneFormLayer
from z3c.form.browser.text import TextWidget
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import IWidget
from z3c.form.widget import FieldWidget
from zope.component import adapter
from zope.component.hooks import getSite
from zope.i18n import translate
from zope.interface import implementer
from zope.interface import implementer_only
from zope.schema import TextLine
from zope.schema import Text
from zope.schema.interfaces import IText
from zope.schema.interfaces import ITextLine


class ISuggestedIATitlesWidget(IWidget):
    pass


class ISVGIconPreviewField(ITextLine):
    pass


class ISVGUploadField(IText):
    pass


class ISVGIconPreviewWidget(IWidget):
    pass


class ISVGUploadWidget(IWidget):
    pass


@implementer(ISVGIconPreviewField)
class SVGIconPreviewField(TextLine):
    pass


@implementer(ISVGUploadField)
class SVGUploadField(Text):
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


@implementer_only(ISVGIconPreviewWidget)
class SVGIconPreviewWidget(TextWidget):
    klass = "smartweb-svg-icon-preview-widget"

    @property
    def resolver_url(self):
        site = getSite()
        if site is not None:
            return f"{site.absolute_url()}/@@smartwebiconresolver"
        return "@@smartwebiconresolver"


@implementer_only(ISVGUploadWidget)
class SVGUploadWidget(TextWidget):
    klass = "smartweb-svg-upload-widget"


@implementer(IFieldWidget)
@adapter(ITextLine, IPloneFormLayer)
def SVGIconPreviewFieldWidget(field, request) -> IFieldWidget:
    return FieldWidget(field, SVGIconPreviewWidget(request))


@implementer(IFieldWidget)
@adapter(ISVGUploadField, IPloneFormLayer)
def SVGUploadFieldWidget(field, request) -> IFieldWidget:
    return FieldWidget(field, SVGUploadWidget(request))


def _clone_persistent_field(field, persistent_class):
    instance = persistent_class.__new__(persistent_class)
    instance.__dict__.update(field.__dict__)
    return instance


@implementer(IPersistentField)
@adapter(ISVGIconPreviewField)
def persistentSVGIconPreviewField(field):
    return _clone_persistent_field(field, PersistentTextLine)


@implementer(IPersistentField)
@adapter(ISVGUploadField)
def persistentSVGUploadField(field):
    return _clone_persistent_field(field, PersistentText)
