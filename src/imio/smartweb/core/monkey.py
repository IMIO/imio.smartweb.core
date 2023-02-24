# -*- coding: utf-8 -*-
import six


def toWidgetValue(self, value):
    """Converts from field value to widget tokenized widget value.

    :param value: Field value.
    :type value: list |tuple | set

    :returns: Items separated using separator defined on widget
    :rtype: string
    """
    if not value:
        return self.field.missing_value
    vocabulary = self.widget.get_vocabulary()
    tokenized_value = []
    for term_value in value:
        if vocabulary is not None:
            try:
                term = vocabulary.getTerm(term_value)
                tokenized_value.append(term.token)
                continue
            except (LookupError, ValueError):
                pass
        tokenized_value.append(six.text_type(term_value))
    return getattr(self.widget, "separator", ";").join(tokenized_value)
