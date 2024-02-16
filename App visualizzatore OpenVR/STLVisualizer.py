#from CubeMod import CubeMod
from ThreeDKnee import ThreeDKnee 
from MenuScreen import MenuScreen 
from openvr.gl_renderer import OpenVrGlRenderer
from openvr.color_cube_actor import ColorCubeActor
from openvr.tracked_devices_actor import TrackedDevicesActor
from openvr.glframework.sdl_app import SdlApp
from controlModule import controlInputModule
import sys


"""
Minimal sdl programming example which colored OpenGL cube scene that can be closed by pressing ESCAPE.
"""


if __name__ == "__main__":
	print(sys.argv)
	stl_location= None
	dataset_location= None
	temp_output_file_location= None
	standalone= True

	if(len(sys.argv) > 1):
		stl_location= sys.argv[1]
		dataset_location= sys.argv[2]
		temp_output_file_location= sys.argv[3]
		standalone= False
	
	renderer = OpenVrGlRenderer(multisample=2)
	controlMod= None
	controlMod=controlInputModule(renderer.poses,dataset_location,temp_output_file_location)
	renderer.append(ThreeDKnee(renderer.poses,controlMod,stl_location))
	renderer.append(MenuScreen(controlMod))
	renderer.append(TrackedDevicesActor(renderer.poses))
	with SdlApp(renderer, "Visualizzazione di un ginocchio in VR") as app:
		app.run_loop()