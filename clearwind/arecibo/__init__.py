from AccessControl import ModuleSecurityInfo


ModuleSecurityInfo('clearwind.arecibo.wrapper').declarePublic('arecibo')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
