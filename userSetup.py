import pymel.core as pm
import MayaInterface


def initPlugin():
    MayaInterface.createShelf()
    print("Maya To Unreal Started")
    

pm.evalDeferred("initPlugin()")


    