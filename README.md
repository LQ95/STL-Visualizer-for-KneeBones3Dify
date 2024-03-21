# StlVisualizer for KneeBones3Dify
This repository includes a version of [KneeBones3Dify](https://github.com/gigernau/KneeBones3Dify) that has been modified so that it could work in tandem with a VR STL visualizer.

This version of this software only works on Microsoft Windows.

# Setup
Install Python 3.9.13 https://www.python.org/downloads/release/python-3913/
(check the "Add python 3.9 to PATH" box in the installer)

Install pip (if you have any specific issues with pip during setup, try reverting to version 22.0.4)

install or upgrade setuptools for python

Install [Visual Studio Build Tools for Visual Studio 2022](https://aka.ms/vs/17/release/vs_BuildTools.exe) and check the first box in the components section

<img src=docs/images/Visual_studio_install_1.png width="500">

if you have any issues,try also installing "Windows 10 SDK"(or Windows 11 SDK if you're using Windows 11) and "MSVC v142 - VS2019 C++ Build Tools x64" from the  sidebar "Installation details" checkboxes

<img src=docs/images/Visual_studio_install_2.png width="500">

IMPORTANT: if your command prompt doesn't recognize "python3.9" chances are you need to type "py" instead.
So if any of the instructions below don't work for this reason after installing Python, type "py" instread of "python3.9"



# Setup for KneeBones3Dify

## 1) Install Python modules: 
	python3.9 -m pip install -r requirements.txt
 #### WARNING: a few packages might require manual reinstalling, like SimpleITK, pyvista and scikit-image. 
 #### If reinstalling becomes necessary, check for the correct version in the requirements.txt file
 
## 2) Check Cuda version or Install [CUDA Version 11.5](https://developer.nvidia.com/cuda-11-5-0-download-archive)
	nvcc --version

## 3) Install CuPy module for CUDA 11.5
	python3.9 -m pip install cupy-cuda115

If you have any issues, try installing cupy-cuda11x as well, along with cupy-cuda115

	python3.9 -m pip install cupy-cuda11x

## 4) Install Cucim
Install [git](https://git-scm.com/)


(read https://github.com/rapidsai/cucim/issues/86 to understand more)

Type this into your Windows shell:


	python3.9 -m pip install -e "git+https://github.com/rapidsai/cucim.git@v22.12.00#egg=cucim&subdirectory=python/cucim"
## Optional) How to compile smoothPatch's code if you have modified it :
This step absolutely unnecessary unless you have modified smoothPatch.cpp and want to make use of your custom version.

In this repository, a copy of smoothPatch.dll is already provided.

### Windows ( install https://winlibs.com/ )
	gcc -c smoothPatch.cpp
	gcc -shared -o smoothPatch.dll smoothPatch.o

 # Setup for the Visualizer
 
## 1) Install Python modules: 
	python3.9 -m pip install -r Visualizer/requirements.txt
 
 
## 2) Ensure you have everything you need for the VR visualization

Install Steam and login/register into a Steam account

Install SteamVR

Ensure that you have an OpenVR compatible headset

Verify whether SteamVR might need recalibration

# Usage Example

A dataset example is available at https://github.com/diego-romano/KneeBones3Dify-Annotated-Dataset 

## 1) In the terminal, type the following command:
	
 	python3.9 SegOscan.py

## 2) Startup GUI and input parameters:

Once you run the above command, a GUI will appear on your screen.

<img src=docs/images/startup_gui.png width="500">

Through this GUI, the user can set the dataset directory and all the parameters: intensity threshold, convex hull dilation, final closing, protrusion removal, and final dilation.
Once all fields are populated, the user must click the OK button to proceed with processing.

There is an error handler that checks the validity of the dataset in input. After pressing the button, After pressing the button, the startup GUI appears again.

<img src=docs/images/error_handler.png width="300">

## 3) Execution log on the terminal:
During the software execution, on the terminal, the user can see all the information about the Dicom dataset shape, MRI type, segmentation status, and execution times.

<img src=docs/images/execution_log.png width="1600">

## 4) Output of the first execution:
At the end of the execution, the VR visualization will start and we can see the result of our first render.

<img src=docs/images/output1.png width="600">

### Controls

Touching the left trackpad rotates the model along the Y axis.

Touching the right trackpad rotates the model along the Z axis.

Pushing the trackpad moves the model parallel to the floor.

<img src=docs/images/trackpad_explanation.jpeg width="500">

The model can be dragged around pushing the trigger button on one of the controllers.

<img src=docs/images/controller_trigger_button.jpg width="500">

The menu button opens the menu

<img src=docs/images/Menu_button.webp width="500">


## 5) Changing the input parameters:

If the user chooses to continue, he will have the possibility to change one or more parameters through the vr menu.

<img src=docs/images/vr_menu_changes.png width="500">

### Menu controls
As said the section about the visualization controls, the menu button brings up or exits the menu.

The menu is controlled entirely through presses of the trackpad.

Pressing on the leftmost and rightmost areas of the track pad will modify the currently selected parameter's value.

Pressing on the top and bottom corner changes the selected parameter/menu option.

To re render, select "re-render" and press the center of the trackpad.


## 7) Execution log after parameter modifications:

The software execution restarts from a specific intermediate state where modified input parameters have an actual impact, avoiding the execution of the whole code . New input data will appear on the terminal, followed by the state number from which the execution restarts and the consequent execution log.

<img src=docs/images/execution_log2.png width="900">

## 8) New Output after parameter modifications:

Finally, the user can see the final result after the VR visualization refreshes.

<img src=docs/images/output2.png width="600">

