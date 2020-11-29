"""
This Module:
- Adds the plugin to Maya (Creates a shelf and deletes the old shelf)

"""
import maya.cmds as cmds
import maya.mel as mel
import os


def createShelf():
    path_ = os.path.dirname(__file__).replace("\\", "/")
    print(path_)
    shelfName_ = "MayaToUnreal"
    imgPath = os.path.join( path_, "Logo.png" ).replace("\\", "/")
    cmd_ = ("""import maya.cmds as cmds
path_ = 'PATH'
selected = cmds.ls(sl=1,sn=True)

for item in selected:
    cmds.select(item)
    cmds.file(path_ + "\Exports\ " + item +".fbx" ,pr=1,typ="FBX export",es=1, op="groups=0; ptgroups=0; materials=0; smoothing=1; normals=1")

cmds.select(selected)
import Initiator""").replace("PATH", os.path.dirname(__file__).replace("\\", "/"))
    
    shelftoplevel = mel.eval("$gShelfTopLevel = $gShelfTopLevel;")
    shelfList_ = cmds.tabLayout(shelftoplevel, query=True, childArray=True)

    # try:
    #     DeleteMayaOldShelf()
    # except:
    #     pass

    if shelftoplevel != None:
        if shelfName_ in shelfList_:
            try:
                for element in cmds.shelfLayout(shelfName_, q=1, ca=1):
                    cmds.deleteUI(element)
            except:
                pass
        else:
            mel.eval("addNewShelfTab " + shelfName_ + ";")
            
        cmds.shelfButton( label="Push", command=cmd_, parent=shelfName_, image=imgPath)
        cmds.saveAllShelves(shelftoplevel)
        
        
        
def DeleteMayaOldShelf(shelfName = "MayaToUnreal"):
    try:
        shelfExists = cmds.shelfLayout(shelfName, ex=True)
        if shelfExists:
            mel.eval('deleteShelfTab %s' % shelfName)
            gShelfTopLevel = mel.eval('$tmpVar=$gShelfTopLevel')
            cmds.saveAllShelves(gShelfTopLevel)
        else:
            return
    except:
        pass

