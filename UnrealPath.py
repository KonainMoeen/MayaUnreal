"""
Get unreal commandline path
"""

import os

def findEpicFolder():
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
    from Interface import getUnrealVersion
    version = getUnrealVersion()
    print(version)
    for foldername in os.listdir(path):
        if foldername.startswith('UE_' + version):
            print('Found Preferred Unreal Version')
            return foldername
        elif foldername.startswith('UE_'):
            return foldername
        
def GetUnrealCMD():
    path = ''
    if findEpicFolder():
        path = findEpicFolder()
        path = path + GetUnrealVersion(path) +'/Engine/Binaries/Win64/UE4Editor-Cmd.exe'
         
        return path
    else:
        return False
