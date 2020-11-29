import pymel.core as pm
import MayaInterface
pm.evalDeferred("initPlugin()")

def initPlugin():
    MayaInterface.createShelf()
    print("Maya To Unreal Started")
    
    