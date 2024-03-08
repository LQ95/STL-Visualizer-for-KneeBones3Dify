# StlVisualizer for KneeBones3Dify

# Setup
Install Python 3.9.13 https://www.python.org/downloads/release/python-3913/
Install pip (if you have any specific issues with pip during setup, try reverting to version 22.0.4)

# Setup for KneeBones3Dify

## 1) Install Python modules: 
	python3.9 -m pip install -r requirements.txt
	
## 2) Check Cuda version or Install [CUDA](https://developer.nvidia.com/cuda-toolkit)
	nvcc --version

## 3) Install CuPy module ( e.g., for CUDA 11.1 )
	python3.9 -m pip install cupy-cuda11x
 
## 4) Install Cucim
install git 
(read https://github.com/rapidsai/cucim/issues/86 to understand more)
type this into your Windows shell


	py -m pip install -e "git+https://github.com/rapidsai/cucim.git@v22.12.00#egg=cucim&subdirectory=python/cucim"
## Optional) Compile smoothPatch code if you have modified it ():
### Windows ( install https://winlibs.com/ )
	gcc -c smoothPatch.cpp
	gcc -shared -o smoothPatch.dll smoothPatch.o

 # Setup for the Visualizer
## 1) Install Python3 modules: 
	python3.9 -m pip install -r Visualizer/requirements.txt
## 2) Ensure that you have an OpenVR compatible headset


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
At the end of the execution, the VR visualization will start and we can see the result of our first render

<img src=docs/images/output1.png width="600">

## 5) Input parameters changes:

If the user chooses to continue, he will have the possibility to change one or more parameters through the vr menu.

<img src=docs/images/vr_menu_changes.png width="500">


## 7) Execution log after parameter modifications:

The software execution restarts from a specific intermediate state where modified input parameters have an actual impact, avoiding the execution of the whole code . New input data will appear on the terminal, followed by the state number from which the execution restarts and the consequent execution log.

<img src=docs/images/execution_log2.png width="900">

## 8) New Output after parameter modifications:

Finally, the user can see the final result after the VR visualization refreshes.

<img src=docs/images/output2.png width="600">

