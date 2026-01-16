# from imio.smartweb.common.browser.forms import CustomAddForm
from imio.smartweb.common.ia.browser.categorization_button_add import (
    IACategorizeAddForm as BaseIACategorizeAddForm,
)
from plone.dexterity.browser.add import DefaultAddView


class IACategorizeAddForm(BaseIACategorizeAddForm):

    def update(self):
        return super(IACategorizeAddForm, self).update()


class IACategorizeAddView(DefaultAddView):
    form = IACategorizeAddForm
