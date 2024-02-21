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
This is the main entry point of the visualizer, that unites, defines and executes everything else
"""


if __name__ == "__main__":
	#you can either execute this program in standalone mode, 
	#without rerendering the STL model,
	#or in conjuction with the segmentation program, which enables you to rerender it 

	#print(sys.argv,file=sys.stderr)
	print("\n\nSTL Visualizer\n\n",file=sys.stderr)
	stl_location= None
	dataset_location= None
	temp_output_file_location= None
	standalone= True

	if(len(sys.argv) > 1):
		stl_location= sys.argv[1]
		dataset_location= sys.argv[2]
		temp_output_file_location= sys.argv[3]
		standalone= False
		print("Non stand-alone mode",file=sys.stderr)
	else:
		print("stand-alone mode",file=sys.stderr)

	#this renderer is what actually sends all rendering data to the VR
	#essentially, it sets up a custom framebuffer, which is what the VR headset sees
	#and all that is appeneded onto the renderer is sent onto that framebuffer
	renderer = OpenVrGlRenderer(multisample=2)
	controlMod= None
	controlMod=controlInputModule(renderer.poses,dataset_location,temp_output_file_location,standalone)
	renderer.append(ThreeDKnee(renderer.poses,controlMod,stl_location))
	renderer.append(MenuScreen(controlMod))
	renderer.append(TrackedDevicesActor(renderer.poses))
	#This is what gives the renderer its OpenGL context
	with SdlApp(renderer, "VR visualization of a knee bone") as app:
		app.run_loop()