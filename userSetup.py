import pymel.core as pm
import Interface


pm.evalDeferred("initPlugin()")

def initPlugin():
    Interface.CreateShelf()
    



    