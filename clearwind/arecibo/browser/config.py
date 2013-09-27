from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from z3c.form import form
from zope.i18nmessageid import MessageFactory

from clearwind.arecibo.interfaces import IAreciboConfiguration


_ = MessageFactory('clearwind.arecibo')


class AreciboConfigurationForm(RegistryEditForm):
    form.extends(RegistryEditForm)
    schema = IAreciboConfiguration

    form_name = _(u"Arecibo settings")
    label = _(u"Arecibo settings")
    description = _(u"Configure Plone to work with your Arecibo account here.")

AreciboConfigurationView = layout.wrap_form(AreciboConfigurationForm, ControlPanelFormWrapper)
