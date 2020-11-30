import maya.mel as mel
import os,subprocess, shutil

path = os.path.dirname(__file__).replace("\\", "/")
FILE = path + "/PathFile.txt"
UE_CMD =r""
PROJECT =r""
    
def fetchPath():
    try:
        with open(FILE, "r") as f:
            lines = f.readlines()
            global UE_CMD, PROJECT
            UE_CMD = lines[0].split("=",1)[-1].strip()
            PROJECT = lines[1].split("=",1)[-1].strip()
    except:
        print("File Not Found")

def getPath():
    var = mel.eval('fileDialog -m 0 -t ""')
    var = r"{}".format(var).strip()
    return var
 
def savePath(path, line):
    with open(FILE, "r+") as f:
        lines = f.readlines()
        lines[line] = path
        f.seek(0)
        f.writelines(lines)
        
def Execute(): 
    fetchPath()    
    global PROJECT, UE_CMD
   
    if UE_CMD=="":
        print("Path to Unreal Engine Cmd (UE4Editor-Cmd.exe) is missing.")
        UE_CMD = r"{}".format(getPath())
        savePath("UE4Editor-Cmd.exe =" + UE_CMD + '\n', 0)
        return
        
    if PROJECT=="":
        print("Path to Unreal Project file (ProjectName.uproject) is missing.")
        PROJECT = r"{}".format(getPath())
        savePath("Project Path =" + PROJECT, 1)
        return
        
    cmd = subprocess.Popen( r'"{}" "{}" -run=pythonscript -script={}/UnrealImport.py'.format(UE_CMD,PROJECT,os.path.dirname(__file__).replace("\\", "/")), shell= True)
    
    
def deleteTempAssets():
    folder = os.path.dirname(__file__).replace("\\", "/") + '/tempExports'
    myfiles = os.listdir(folder)
    for file in myfiles:
            os.unlink(folder+ '/' + file)    
    
