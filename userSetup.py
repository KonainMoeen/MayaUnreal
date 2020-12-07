import pymel.core as pm
import Interface


def initPlugin():
    Interface.CreateShelf()
    print("Maya To Unreal Started")
    

pm.evalDeferred("initPlugin()")


    