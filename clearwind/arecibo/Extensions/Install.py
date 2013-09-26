from cStringIO import StringIO
from Products.CMFCore.utils import getToolByName


def install(portal, reinstall=False):
    out = StringIO()
    setupTool = getToolByName(portal, 'portal_setup')
    setupTool.runAllImportStepsFromProfile('profile-clearwind.arecibo:default')
    print >>out, "Installed clearwind.arecibo"
    return out.getvalue()


def uninstall(portal):
    """ Uninstall """
    cp = getToolByName(portal, 'portal_controlpanel')
    if "arecibo" in [c.id for c in cp._actions]:
        cp.unregisterConfiglet("arecibo")
