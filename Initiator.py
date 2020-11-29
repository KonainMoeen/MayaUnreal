import maya.mel as m
import os,subprocess, shutil
path = os.path.dirname(__file__).replace("\\", "/")
FILE = path + "/PathFile.txt"#os.listdir(os.path.dirname(__file__).replace("\\", "/") + "PathFile.txt")
print(FILE)
UE_CMD = r""
PROJECT = r""



def fetchPath():
    try:
        with open(FILE, "r") as f:
            lines = f.readlines()
            global UE_CMD, PROJECT
            UE_CMD = lines[0].split("=",1)[-1]
            UE_CMD = UE_CMD[:-1]
            PROJECT = lines[1].split("=",1)[-1]
    except:
        print("File Not Found")

def getPath():
    var = m.eval('fileDialog -m 0 -t ""')
    var = r"{}".format(var)
    return var
 
def savePath(path, line):
    with open(FILE, "r") as f:
        lines = f.readlines()
    lines[line] = path
    with open(os.getcwd() + '/'+ FILE, "w") as f:
        print(os.getcwd() + '/'+ FILE)
        f.writelines(lines)
        

fetchPath()


if UE_CMD=="":
    print("UE is EMPTY")
    UE_CMD = r"{}".format(getPath())
    savePath("UE4Editor-Cmd.exe =" + UE_CMD + '\n', 0)
    
if PROJECT=="":
    print("PROJECT is EMPTY")
    PROJECT = r"{}".format(getPath())
    savePath("Project Path =" + PROJECT, 1)


cmd = subprocess.Popen( r'"{}" "{}" -run=pythonscript -script={}/UnrealImport.py'.format(UE_CMD,PROJECT,os.path.dirname(__file__).replace("\\", "/")), shell= True)

