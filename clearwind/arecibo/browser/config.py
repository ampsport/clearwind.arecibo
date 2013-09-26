from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.app.controlpanel.form import ControlPanelForm 
from zope.component import adapts
from zope.formlib import form
from zope.i18nmessageid import MessageFactory
from zope.interface import implements

from clearwind.arecibo.interfaces import IAreciboConfiguration


_ = MessageFactory('clearwind.arecibo')

class AreciboConfigurationForm(ControlPanelForm):
    form_fields = form.Fields(IAreciboConfiguration)

    description = _(u"Configure Plone to work with your Arecibo account here.")
    form_name = _(u"Arecibo settings")
    label = _(u"Arecibo settings")

class AreciboControlPanelAdapter(SchemaAdapterBase):
    adapts(IPloneSiteRoot)
    implements(IAreciboConfiguration)

    account_number = ProxyFieldProperty(IAreciboConfiguration['account_number'])
    app_name = ProxyFieldProperty(IAreciboConfiguration['app_name'])
    transport = ProxyFieldProperty(IAreciboConfiguration['transport'])
    ignore_localhost = ProxyFieldProperty(IAreciboConfiguration['ignore_localhost'])
