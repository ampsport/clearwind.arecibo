

def importVarious(context): 
    if context.readDataFile("clearwind.arecibo.txt") is None:
        return
    portal = context.getSite()
