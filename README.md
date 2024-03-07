# StlVisualizer for KneeBones3Dify


# Setup 

## 1) Update : 
	sudo apt update
  
## 2) Install dependencies:
    sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev python-tk python3-tk tk-dev python3-pil python3-pil.imagetk

## 3) Install pip3 for Python3: 
	sudo apt install python3-pip  && python3 -m pip install --upgrade pip

## 4) Install Python3 modules: 
	python3 -m pip install -r requirements.txt
	
## 5) Check Cuda version or Install [CUDA](https://developer.nvidia.com/cuda-toolkit)
	nvcc -V

## 6) Install CuPy module ( e.g., for CUDA 11.1 )
	python3 -m pip install cupy-cuda11x

## 7) Compile smoothPatch code:
### Linux
	gcc -shared -o smoothPatch.so smoothPatch.cpp
### Windows ( install https://winlibs.com/ )
	gcc -c smoothPatch.cpp
	gcc -shared -o smoothPatch.dll smoothPatch.o


# Usage Example

A dataset example is available at https://github.com/diego-romano/KneeBones3Dify-Annotated-Dataset 

## 1) In the terminal, type the following command:
	
 	python3 SegOscan.py

## 2) Startup GUI and input parameters:

Once you run the above command, a GUI will appear on your screen.

<img src=docs/images/startup_gui.png width="500">

Through this GUI, the user can set the dataset directory and all the parameters: intensity threshold, convex hull dilation, final closing, protrusion removal, and final dilation.
Once all fields are populated, the user must click the OK button to proceed with processing.

There is an error handler that checks the validity of the dataset in input. After pressing the button, the startup GUI appears again.

<img src=docs/images/error_handler.png width="300">

## 3) Execution log on the terminal:
During the software execution, on the terminal, the user can see all the information about the Dicom dataset shape, MRI type, segmentation status, and execution times.

<img src=docs/images/execution_log.png width="600">

## 4) Output of the first execution:
At the end of the execution, the VR visualization will start and we can see the result of our first render

<img src=docs/images/output1.png width="600">

## 5) Input parameters changes:

If the user chooses to continue, he will have the possibility to change one or more parameters through the vr menu.

<img src=docs/images/vr_menu_changes.png width="500">


## 7) Execution log after parameter modifications:

The software execution restarts from a specific intermediate state where modified input parameters have an actual impact, avoiding the execution of the whole code . New input data will appear on the terminal, followed by the state number from which the execution restarts and the consequent execution log.

<img src=docs/images/execution_log2.png width="600">

## 8) New Output after parameter modifications:

Finally, the user can see the final result in a new window.

<img src=docs/images/output2.png width="600">

