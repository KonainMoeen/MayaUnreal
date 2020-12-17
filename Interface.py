"""
Handles all the interface and the data received from the interface
"""
import maya.cmds as cmds
import maya.mel as mel
import os
import Handler


projectTextField = ''
project_path= ''
content_path= ''
prefix = ''
#This generates the shelf button
def CreateShelf():
    path_ = os.path.dirname(__file__).replace("\\", "/")
    shelfName_ = "MayaToUnreal"
    imgPath = os.path.join( path_, "Logo.png" ).replace("\\", "/")
    
    cmd_="""
from Interface import MayaToUnrealMenu
MayaToUnrealMenu()
"""
    shelftoplevel = mel.eval("$gShelfTopLevel = $gShelfTopLevel;")
    shelfList_ = cmds.tabLayout(shelftoplevel, query=True, childArray=True)

    try:
        DeleteMayaOldShelf()
    except:
        pass

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
            mel.eval('deleteShelfTab {}'.format(shelfName))
            gShelfTopLevel = mel.eval('$tmpVar=$gShelfTopLevel')
            cmds.saveAllShelves(gShelfTopLevel)
        else:
            return
    except:
        pass
    
#This is a helper function for changing the text in the textfield of menu when the user selects a file using the menu button
def openPathSelection(*args):
    path = mel.eval('fileDialog -m 0 -t ""')
    if path == '':
        return

    elif(args[0] == 1):
        project_path = cmds.textField( projectTextField, edit=True, tx=path )
        Handler.savePathInFile("Project Path =" + cmds.textField(project_path, q=1, text=1) + '\n', args[0])


#This is the Menu that is shown in Maya on button click
def MayaToUnrealMenu():
    global projectTextField, cmd_path, project_path, content_path, prefix
    pathInFile = Handler.FetchPath()
    Window = cmds.window('Maya to Unreal',mnb = False, mxb = False)
    #Main Layout
    cmds.columnLayout(bgc=(0.878, 0.874, 0.890),adjustableColumn=1 )

    #PROJECT ROW
    cmds.rowColumnLayout( numberOfColumns=3, columnAttach=(1, 'right', 4), columnWidth=[(1, 100), (2, 400), (3, 25)], adjustableColumn=2 , bgc=(0.878, 0.874, 0.890))

    # Project UI
    cmds.text( label=' *Unreal Project :'  )
    projectTextField = cmds.textField(w=200)
    project_pathbtn = cmds.button(l=': :', align='right', width=25, bgc=(0.109, 0.215, 0.368), command =btnProjectPath)
    project_path = cmds.textField( projectTextField, edit=True, enterCommand=('cmds.setFocus(\"' + projectTextField + '\")'), tx=pathInFile[1] )
    
    cmds.setParent('..')
    cmds.rowColumnLayout(numberOfColumns=5, columnAttach=(1, 'right', 2), columnWidth=[(1, 100), (2, 150),(3,100),(4,150),(5, 25)],bgc=(0.878, 0.874, 0.890),adjustableColumn=2)
    
    # Assets path UI
    cmds.text(label=' Content Location : ')
    contentTextField = cmds.textField(w=145)
    content_path = cmds.textField( contentTextField, edit=True, enterCommand=('cmds.setFocus(\"' + contentTextField + '\")'), tx=pathInFile[2] )
    
    # Name Prefix UI
    cmds.text( label=' Asset Name Prefix : '  )
    prefixTextField = cmds.textField(w=145)
    prefix = cmds.textField( prefixTextField, edit=True, enterCommand=('cmds.setFocus(\"' + contentTextField + '\")') )
    
    cmds.text(' ')

    cmds.setParent('..')
    cmds.rowColumnLayout(co=[(1,'both',160)],columnWidth=[(1, 100)],adjustableColumn=1  )
    # Button UI
    cmds.button(l='Export to Unreal',height=30, bgc=(0.109, 0.215, 0.368), command=btnExecute)
    
    cmds.showWindow( Window )
    
# This is the main workflow
def StartExportProcess(*args):
    saveContentPath()
    Handler.SendPaths(args[0])
    Handler.DeleteTempAssets()
    Handler.ExportTempAssets()
    Handler.EnablePythonPlugin()
    Handler.Execute()
        
def btnExecute(*args):
    StartExportProcess(cmds.textField(project_path, q=1, text=1))
    
def btnProjectPath(*args):
    openPathSelection(1)      
    
    
def saveContentPath():
    Handler.savePathInFile("Content Path =" + cmds.textField(content_path, q=1, text=1), 2)

def getAssetPrefix():
    return cmds.textField(prefix, q=1, text=1)
