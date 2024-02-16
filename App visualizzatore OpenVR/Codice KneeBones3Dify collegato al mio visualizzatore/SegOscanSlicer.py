import logging
import slicer
import SurfaceToolbox
import sys
import tempfile

#add stl and transform it
nm = tempfile.gettempdir() +"\\MRI.stl"
#segmentation = slicer.util.loadSegmentation(r'C:\Users\Gianluca\Desktop\MEDIA\Datasets\2.stl')
model = slicer.util.loadModel(nm)
#model = slicer.util.loadModel(r'C:\\Users\\Gianluca\\Desktop\\MEDIA\\Datasets\\2.stl')
print("Model loaded")
model.GetDisplayNode().SetColor(.5, .5, .5)
scalePointCoord = [2, 2, 2]
srLogic = slicer.modules.surfacetoolbox.logic()
#srLogic.SetSurfaceToolboxActive(True)
parameterNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScriptedModuleNode")
logic = SurfaceToolbox.SurfaceToolboxLogic()
#logic.setDefaultParameters(parameterNode)
#inputModelNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode", "2")
parameterNode.SetNodeReferenceID("inputModel", "vtkMRMLModelNode4")
#outputModelNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelNode", "output")
parameterNode.SetNodeReferenceID("outputModel", "vtkMRMLModelNode4")
#parameterNode.SetNodeReferenceID("outputModel", segmentation.GetID())




def isVRInitialized():
    """Determine if VR has been initialized
    """
    vrLogic = slicer.modules.virtualreality.logic()
    if (vrLogic is None
        or vrLogic.GetVirtualRealityViewNode() is None
        or not vrLogic.GetVirtualRealityViewNode().GetVisibility()
        or not vrLogic.GetVirtualRealityViewNode().GetActive()):
        return False
    return True

def vrCamera():
    # Get VR module widget
    if not isVRInitialized():
        return None
    # Get VR camera
    vrViewWidget = slicer.modules.virtualreality.viewWidget()
    if vrViewWidget is None:
      return None
    rendererCollection = vrViewWidget.renderWindow().GetRenderers()
    if rendererCollection.GetNumberOfItems() < 1:
        logging.error('Unable to access VR renderers')
        return None

    return rendererCollection.GetItemAsObject(0).GetActiveCamera()



assert isVRInitialized() is False
assert vrCamera() is None

vrLogic = slicer.modules.virtualreality.logic()
vrLogic.SetVirtualRealityActive(True)
#print(dir(vrLogic.SetMRMLScene()))

position = [0,0,0]
vrCamera = vrCamera()
#print(dir(vrCamera))
#Questo codice non sembra funzionare
#vrCamera.SetEyePosition(position)
#vrCamera.SetParallelProjection(2)
vrCamera.SetWindowCenter(0,0.5)
vrCamera.Yaw(-1.57)
vrCamera.Zoom(1)
vrCamera.SetViewAngle(0)

#vrCamera.SetPosition(position)
#vrCamera.SetDistance(0.5)
#print(vrCamera.GetPosition())
#print(vrCamera.GetViewUp())
#vrCamera.UpdateViewport(0)

#print(dir(slicer.modules.virtualreality.viewWidget().renderWindow().GetRenderers().GetItemAsObject(0)))
#vrCamera.ApplyTransform(vrLogic)


#print(vars(slicer.modules.virtualreality))

#print(inspect.getmembers(slicer.modules.virtualreality, predicate=inspect.ismethod))

#print((slicer.modules.virtualreality.viewWidget().renderWindow().GetRenderers().GetClassName()))

slicer.modules.virtualreality.viewWidget().renderWindow().GetRenderers().GetItemAsObject(0).SetViewPoint(position)

#print(vrCamera)
slicer.modules.virtualreality.viewWidget().renderWindow().GetRenderers().GetItemAsObject(0).RemoveAllLights()
colorBG = [0,0,0]
colorVolume = [0.5,0.5,0.5]
vrView=getNode('VirtualRealityView')
vrView.SetBackgroundColor(colorBG)
vrView.SetBackgroundColor2(colorBG)
#vrCam=getNode('VirtualRealityCamera')
#print(vrCam)



# idss = vtk.vtkStringArray()
# model.GetDisplayNode().GetVisibleModelIDs(idss)
# segment = segmentation.GetModel(idss.GetValue(0))




#queste trasformazioni funzionano solo se questo codice resta qui


parameterNode.SetParameter("scale", "true")
parameterNode.SetParameter("scaleX", "0.70")
parameterNode.SetParameter("scaleY", "0.70")
parameterNode.SetParameter("scaleZ", "0.70")

parameterNode.SetParameter("translate", "true")
parameterNode.SetParameter("translateCenterToOrigin", "true")
parameterNode.SetParameter("translateX", "-30")
parameterNode.SetParameter("translateY", "275")
parameterNode.SetParameter("translateZ", "-40")


parameterNode.SetParameter("rotate", "true")
parameterNode.SetParameter("rotateX", "135")
parameterNode.SetParameter("rotatey", "45")
parameterNode.SetParameter("rotatez", "90")
# parameterNode.SetParameter("smoothingBoundarySmoothing", "false")
# parameterNode.SetParameter("decimationBoundaryDeletion", "false")
# parameterNode.SetParameter("HideFromEditors", "false")
#parameterNode.SetParameter("Debug", "true")

logic.applyFilters(parameterNode)
# inputModel = parameterNode.GetNodeReference("inputModel")
# outputModel = parameterNode.GetNodeReference("outputModel")


# layoutManager = slicer.app.layoutManager()
#threeDView = slicer.modules.virtualreality.viewWidget()
#print(dir(threeDView))
# threeDView.resetFocalPoint()
# threeDView.yaw()
# threeDView.yaw()
# threeDView.yaw()
# threeDView.yaw()
# threeDView.yaw()
# threeDView.yaw()
# threeDView.yaw()


#vtkMRMLVirtualRealityViewNodeActive
#parameterNode2 = slicer.modules.virtualreality.AddNewNodeByClass("vtkOpenVRCamera")
#vrLogic.setDefaultParameters(parameterNode2)
#print(parameterNode2)
#parameterNode.SetNodeReferenceID("vrCamera", "vtkMRMLModelNode4")

#parameterNode2.SetParameter("Position", position)
#vrLogic.applyFilters(parameterNode2)
#parameterNode2 = slicer.modules.virtualreality.mrmlScene.AddNewNodeByClass("vtkMRMLScriptedModuleNode")

slicer.modules.virtualreality.optimizeSceneForVirtualReality()
slicer.modules.virtualreality.updateViewFromReferenceViewCamera()
slicer.modules.virtualreality.viewWidget().updateViewFromReferenceViewCamera()

threeDView = slicer.app.layoutManager().threeDWidget(0).threeDView()
threeDView.resetFocalPoint()
