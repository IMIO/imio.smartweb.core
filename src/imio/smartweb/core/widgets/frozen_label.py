# -*- coding: utf-8 -*-

from html import escape
from xml.sax.saxutils import quoteattr
from z3c.form.browser.text import TextWidget
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import NO_VALUE
from z3c.form.widget import FieldWidget
from zope.interface import implementer


class FrozenLabelTextWidget(TextWidget):
    """Render a TextLine column as a read-only label while still submitting it.

    A ``mode="display"`` column looks right but emits no input, so it is not
    submitted and ``DictRow._validate`` rejects every row on save with
    ``AttributeNotFoundError``. ``readonly=True`` is worse: it overwrites the
    row value with the field's single ``default``, so it cannot carry a
    per-row-distinct value. This widget keeps the field in input mode -- so
    extraction is inherited unchanged from TextWidget -- yet renders only a
    span plus a hidden input.
    """

    def render(self):
        value = self.value
        if value is NO_VALUE or value is None:
            value = ""
        elif isinstance(value, (list, tuple)):
            # In a DataGrid the sub-widget value is the raw field value; a
            # list would otherwise render its first character only.
            value = value[0] if value else ""
        value = str(value)
        return (
            '<span class="dgf-frozen-label">{label}</span>'
            '<input type="hidden" name={name} value={value} />'
        ).format(
            label=escape(value),
            name=quoteattr(self.name),
            value=quoteattr(value),
        )


@implementer(IFieldWidget)
def FrozenLabelTextFieldWidget(field, request) -> IFieldWidget:
    return FieldWidget(field, FrozenLabelTextWidget(request))
