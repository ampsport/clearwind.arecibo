default_profile = "profile-clearwind.arecibo:default"

def importVarious(context): 
    if context.readDataFile("clearwind.arecibo.txt") is None:
        return
    portal = context.getSite()


def upgrade_1_to_2(context):
    context.runImportStepFromProfile(default_profile, 'plone.app.registry')