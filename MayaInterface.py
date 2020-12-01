"""
This Module:
- Adds the plugin to Maya (Creates a shelf and deletes the old shelf)

"""
import maya.cmds as cmds
import maya.mel as mel
import os
import Initiator


ueTextField = ''
projectTextField = ''
cmd_path = ''
project_path=''
#This generates the shelf button
def CreateShelf():
    path_ = os.path.dirname(__file__).replace("\\", "/")
    print(path_)
    shelfName_ = "MayaToUnreal"
    imgPath = os.path.join( path_, "Logo.png" ).replace("\\", "/")
    
    cmd_="""
from MayaInterface import MayaToUnrealMenu
MayaToUnrealMenu()
"""
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
        
#This is a helper function for changing the text in the textfield of menu when the user selects a file using the menu button
def openPathSelection(*args):
    path = mel.eval('fileDialog -m 0 -t ""')
    if path == '':
        return
    
    if(args[0] == 0):
        cmd_path = cmds.textField( ueTextField, edit=True, tx=path )
        Initiator.savePathInFile("UE4Editor-Cmd.exe =" + cmds.textField(cmd_path, q=1, text=1)  + '\n', args[0])

    elif(args[0] == 1):
        project_path = cmds.textField( projectTextField, edit=True, tx=path )
        Initiator.savePathInFile("Project Path =" + cmds.textField(project_path, q=1, text=1), args[0])


#This is the Menu that is shown in Maya on button click
def MayaToUnrealMenu():
    global ueTextField, projectTextField, cmd_path, project_path
    pathInFile = Initiator.FetchPath()
    
    
    Window = cmds.window('Maya to Unreal',mnb = False, mxb = False)
    cmds.rowColumnLayout( numberOfColumns=3, columnAttach=(1, 'both', 0), columnWidth=[(1, 110), (2, 180)], adjustableColumn=2 )
    cmds.text( label='Unreal Editor Cmd : ')
    ueTextField = cmds.textField(w=200)
    cmd_pathbtn = cmds.button(l='::', align='right', width=25, command =btnCmdPath)

    cmds.text( label='Unreal Project : '  )
    projectTextField = cmds.textField(w=200)
    project_pathbtn = cmds.button(l='::', align='right', width=25, command =btnProjectPath)


    cmd_path = cmds.textField( ueTextField, edit=True, enterCommand=('cmds.setFocus(\"' + ueTextField + '\")'), tx=pathInFile[0] )
    project_path = cmds.textField( projectTextField, edit=True, enterCommand=('cmds.setFocus(\"' + projectTextField + '\")'), tx=pathInFile[1] )
    cmds.text('')
    cmds.button(l='Export to Unreal',width=100, command=btnExecute)
    
    cmds.showWindow( Window )
    
# This is the main workflow
def StartExportProcess(*args):
    Initiator.SendPaths(args[0], args[1])
    Initiator.DeleteTempAssets()
    Initiator.ExportTempAssets()
    Initiator.Execute()
    
    
def btnExecute(*args):
    StartExportProcess(cmds.textField(cmd_path, q=1, text=1),cmds.textField(project_path, q=1, text=1))
    
def btnProjectPath(*args):
    openPathSelection(1)    
    
def btnCmdPath(*args):
    openPathSelection(0)    
    
# def DeleteMayaOldShelf(shelfName = "MayaToUnreal"):
#     try:
#         shelfExists = cmds.shelfLayout(shelfName, ex=True)
#         if shelfExists:
#             mel.eval('deleteShelfTab %s' % shelfName)
#             gShelfTopLevel = mel.eval('$tmpVar=$gShelfTopLevel')
#             cmds.saveAllShelves(gShelfTopLevel)
#         else:
#             return
#     except:
#         pass
    