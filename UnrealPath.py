"""
Get unreal commandline path
"""

import os

def FindEpicFolder():
    basePath = 'C:/Program Files'
    drives = [ chr(x) + ":/" for x in range(65,91) if os.path.exists(chr(x) + ":") ]
    
    if 'Epic Games' in os.listdir(basePath):
        return basePath + 'Epic Games/'
    else:
        for item in drives:
            if 'Epic Games' in os.listdir(item):
                return item + 'Epic Games/'

    return False
        

def GetUnrealVersion(path):
    from Handler import FindUnrealProjectVersion
    version = FindUnrealProjectVersion()
    backupversion = ''
    for foldername in os.listdir(path):   
            if foldername == 'UE_'+ version:
                return foldername
            elif foldername.startswith('UE_'):
                backupversion = foldername
    if backupversion:
        print("Project Version is different from installed Unreal Version")
        return backupversion
    else:
        return False

def GetUnrealCMD():
    path = ''
    if FindEpicFolder():
        path = FindEpicFolder()
        if GetUnrealVersion(path):
            path = path + GetUnrealVersion(path) +'/Engine/Binaries/Win64/UE4Editor-Cmd.exe'
            return path
        else:
            return False
    else:
        return False
