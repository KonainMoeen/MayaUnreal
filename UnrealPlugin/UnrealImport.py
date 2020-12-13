"""
Handles all the import process inside Unreal
"""
import unreal
import os

def SetupAsset():
    model = []
    modelnames = os.listdir(os.path.dirname(__file__).replace("\\", "/") + "/tempExports")
    for item in modelnames:
        model.append(os.path.dirname(__file__).replace("\\", "/") + '/tempExports/' + item)
    
    importAsset(model)
    
def importAsset(model):
    count = 0
    tasks = []
    contentlocation = '/Game/' + getContentPath()
    while count < len(model):
        modeltask = buildImportTask(model[count],contentlocation)
        tasks.append(modeltask)
        count += 1

    for items in tasks:
        executeTasks([items])
    
def buildImportTask(filename,destination):
    task = unreal.AssetImportTask()
    task.set_editor_property('automated', True)
    task.set_editor_property('destination_path', destination)
    task.set_editor_property('filename', filename)
    task.set_editor_property('replace_existing', True)
    task.set_editor_property('save', True)
    return task

def executeTasks(tasks):
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
    

def getContentPath():
    pathInFile=['','','']
    try:
        with open(os.path.dirname(__file__).replace("\\", "/") + "/PathFile.txt", "r") as f:
            lines = f.readlines()
            pathInFile[2] = lines[2].split("=",1)[-1].strip()
        return pathInFile[2].replace("\\", "/")
    except:
        print("File Not Found or File is Missing Data")
        return ''

if __name__ == "__main__":
    SetupAsset()



