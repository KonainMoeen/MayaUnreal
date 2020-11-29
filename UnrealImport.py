import unreal
import os

def importAsset():
    model = []
    modelnames = os.listdir(os.path.dirname(__file__).replace("\\", "/") + "/Exports")
    for item in modelnames:
        model.append(os.path.dirname(__file__).replace("\\", "/") + '/Exports/' + item)
    tasks = []
    count = 0
    
    while count < len(model):
        modeltask = buildImportTask(model[count],'/Game/MayaToUnreal')
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
    deleteTempAssets()
    
def deleteTempAssets():
    folder = os.path.dirname(__file__).replace("\\", "/") + '/Exports'
    
    myfiles = os.listdir(folder)
    for file in myfiles:
        os.unlink(folder+ '/' + file)

if __name__ == "__main__":
    importAsset()



