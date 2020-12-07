"""
Handles all the file handling and export/import process
"""

import os,subprocess, shutil

path = os.path.dirname(__file__).replace("\\", "/")
FILE = path + "/PathFile.txt"
UE_CMD =r""
PROJECT =r""
    
# Fetches the path from PathFile
def FetchPath():
    pathInFile=['','','']
    try:
        with open(FILE, "r") as f:
            lines = f.readlines()
            pathInFile[0] = lines[0].split("=",1)[-1].strip()
            pathInFile[1] = lines[1].split("=",1)[-1].strip()
            pathInFile[2] = lines[2].split("=",1)[-1].strip()
        return pathInFile
    except:
        print("Text File Not Found or File is Missing Data")
        return pathInFile

    
# Saves the new path in file for future reference
def savePathInFile(path, line):
    try:
        fin = open(FILE, 'r')
        lines = fin.readlines()
        lines[line] = path
        fin.close()
        
        fout = open(FILE, 'w')
        fout.writelines(lines)
        fout.close()
    except:
        print("Error Saving paths to file")
        
# Runs the Commandline argument for the UE Imports
def Execute(): 
    #global PROJECT, UE_CMD
   
    if UE_CMD=="":
        print("Unreal Path Error. Check README for more info")
        return
        
    if PROJECT=="":
        print("Path to Unreal Project file is missing. Check README for more info")
        return
        
    cmd = subprocess.Popen( r'"{}" "{}" -run=pythonscript -script={}/UnrealImport.py'.format(UE_CMD,PROJECT,os.path.dirname(__file__).replace("\\", "/")), shell= True)
    
# Deletes the temporary assets in tempExports folder
def DeleteTempAssets():
    folder = os.path.dirname(__file__).replace("\\", "/") + '/tempExports'
    myfiles = os.listdir(folder)
    for file in myfiles:
            os.unlink(folder+ '/' + file)    
    
# Exports the temporary assets in tempExports folder 
def ExportTempAssets():
    import maya.cmds as cmds
    from Interface import getAssetPrefix
    selected = cmds.ls(sl=1,sn=True)

    for item in selected:
        cmds.select(item)
        cmds.file(path + "/tempExports/" + getAssetPrefix() + item +".fbx" ,pr=1,typ="FBX export",es=1, op="groups=0; ptgroups=0; materials=0; smoothing=1; normals=1")

    cmds.select(selected)
    
# Gets the path of Cmd and Project right: used right when the export button is clicked
def SendPaths(ProjectPath):
    from UnrealPath import GetUnrealCMD
    path = GetUnrealCMD()
    global PROJECT, UE_CMD

    if UE_CMD == "":
        if path:
            savePathInFile("UE4Editor-Cmd.exe =" + path  + '\n',0)
            UE_CMD = path

    PROJECT = ProjectPath
    
