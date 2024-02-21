import openvr
import math
import numpy
import os
import sys
from MenuStatus import MenuStatus

#Auxiliary class that handles control of the model in VR

class controlInputModule:
	def __init__(self, pose_array, dataset_loc = None, temp_output_file_loc = None, standalone = False):
		
		#control parameters
		self.rotationAmount = 0
		self.translationDelta = [0,0,0]
		self.rotationAxis = [0,0,1]
		#ids
		self.left_controller_id= None 
		self.right_controller_id= None
		
		#variables relating to internal state that need to be stored
		self.last_left_angle= 0
		self.last_right_angle= 0

		self.left_isdragging = False
		self.right_isdragging = False
		self.last_left_pos = None
		self.last_right_pos = None
		self.left_pause_pressed= False
		self.right_pause_pressed= False
		
		#device poses
		self.pose_array=pose_array  
		
		self.lockedRotation= 0

		#outputs that needs to be stored
		self.rotationMatrix=numpy.array([[1,0,0,0],
		[0,1,0,0],
		[0,0,1,0],
		[0,0,0,1]], dtype = numpy.float32)
		
		self.controllerRotationMatrix=numpy.array([[1,0,0,0],
		[0,1,0,0],
		[0,0,1,0],
		[0,0,0,1]], dtype = numpy.float32)

		self.trackpadRotationMatrix=numpy.array([[1,0,0,0],
		[0,1,0,0],
		[0,0,1,0],
		[0,0,0,1]], dtype = numpy.float32)
		
		#auxiliary matrices
		self.controllerRotationMatrix_static=numpy.array([[1,0,0,0],
		[0,1,0,0],
		[0,0,1,0],
		[0,0,0,1]], dtype = numpy.float32)
		self.controllerRotationMatrix_reset=numpy.array([[1,0,0,0],
		[0,1,0,0],
		[0,0,1,0],
		[0,0,0,1]], dtype = numpy.float32)
		
		
		#variables relating to external state that need to be stored and modified here
		self.paused= False
		self.re_rendering = False
		


		self.temp_file_modified = None

		
		if(dataset_loc!= None):
			self.dataset_location = dataset_loc
		if(temp_output_file_loc!= None):
			self.temp_output_file_location = temp_output_file_loc

		#menu state variables
		self.menuStatus = MenuStatus()
		self.left_pause_pressed = False
		self.right_pause_pressed = False

		self.right_menu_enabled = False
		self.left_menu_enabled = False
		
		self.left_trackpad_pressed = False
		self.right_trackpad_pressed = False

		
		#if this flag is true we are in standalone mode and re rendering functionalities are not usable
		self.standalone_mode = standalone

	def getDelta(self,pos1,pos2):
		return [pos1[0] - pos2[0], pos1[1] - pos2[1], pos1[2] - pos2[2]]


	def getFinalDelta(self,pos1,pos2):


		return [pos1[0] + pos2[0], pos1[1] + pos2[1], pos1[2] + pos2[2]] 


	def get_controller_ids(self):

		left = None
		right = None
		for i in range(openvr.k_unMaxTrackedDeviceCount):
			device_class = openvr.VRSystem().getTrackedDeviceClass(i)
			if device_class == openvr.TrackedDeviceClass_Controller:
				role = openvr.VRSystem().getControllerRoleForTrackedDeviceIndex(i)
				if role == openvr.TrackedControllerRole_RightHand:
					right = i
				if role == openvr.TrackedControllerRole_LeftHand:
					left = i
		return left, right

	def get_controller_pos(self,controller_id):
		controller_pose = self.pose_array[controller_id]
		controller_matrix=controller_pose.mDeviceToAbsoluteTracking
		return [controller_matrix[0][3],controller_matrix[1][3],controller_matrix[2][3]]

	def get_controller_rotation(self,controller_id):
		controller_pose = self.pose_array[controller_id]
		controller_matrix=controller_pose.mDeviceToAbsoluteTracking
		return numpy.array([[controller_matrix[0][0],controller_matrix[0][1],controller_matrix[0][2],0],
		[controller_matrix[1][0],controller_matrix[1][1],controller_matrix[1][2],0],
		[controller_matrix[2][0],controller_matrix[2][1],controller_matrix[2][2],0],
		[0,0,0,1.0]], dtype = numpy.float32)


	def get_rotation_matrix(self,axis, angle):         
		axis = axis/numpy.linalg.norm(axis)
		s = math.sin(angle)
		c = math.cos(angle)
		oc = 1.0 - c
		matrix =numpy.array([[oc * axis[0] * axis[0] + c,           oc * axis[0] * axis[1] - axis[2] * s,  oc * axis[2] * axis[0] + axis[1] * s,  0.0],
				[oc * axis[0] * axis[1] + axis[2] * s,  oc * axis[1] * axis[1] + c,           oc * axis[1] * axis[2] - axis[0] * s,  0.0],
				[oc * axis[2] * axis[0] - axis[1] * s,  oc * axis[1] * axis[2] + axis[0] * s,  oc * axis[2] * axis[2] + c,           0.0],
				[0.0,                                0.0,                                0.0,                                1.0]], dtype = numpy.float32)

		return matrix
    
    #generate the outputstring that is used by segmentation program to regenereate the STL model
	def packParametersIntoOutputString(self,menu_dict):
		print("creating output string",file=sys.stderr)
		outputString = self.dataset_location
		separator="%"

		outputString += separator + str(menu_dict['intensity_threshold'])
		outputString += separator + str(menu_dict['convex_hull_dilation'])
		outputString += separator + str(menu_dict['final_closing'])
		outputString += separator + str(menu_dict['protrusion_removal'])
		outputString += separator + str(menu_dict['final_dilation']) +"\n"
		#print("returning output string",file=sys.stderr)
		#print(outputString,file=sys.stderr)
		return outputString
    	



	
	def from_controller_state_to_dict(self,pControllerState):
		# docs: https://github.com/ValveSoftware/openvr/wiki/IVRSystem::GetControllerState
		d = {}
		d['unPacketNum'] = pControllerState.unPacketNum
        
		# on trigger .y is always 0.0 says the docs
		d['trigger'] = pControllerState.rAxis[1].x
        
		# 0.0 on trigger is fully released
		# -1.0 to 1.0 on joystick and trackpads
		d['trackpad_x'] = pControllerState.rAxis[0].x
		d['trackpad_y'] = pControllerState.rAxis[0].y
        
        # These are published and always 0.0
        # for i in range(2, 5):
        #     d['unknowns_' + str(i) + '_x'] = pControllerState.rAxis[i].x
        #     d['unknowns_' + str(i) + '_y'] = pControllerState.rAxis[i].y
		d['ulButtonPressed'] = pControllerState.ulButtonPressed
		d['ulButtonTouched'] = pControllerState.ulButtonTouched
        
        # To make easier to understand what is going on
        # Second bit marks menu button
		d['menu_button'] = bool(pControllerState.ulButtonPressed >> 1 & 1)
        
        # 32nd bit marks trackpad
		d['trackpad_pressed'] = bool(pControllerState.ulButtonPressed >> 32 & 1)
		d['trackpad_touched'] = bool(pControllerState.ulButtonTouched >> 32 & 1)
        
        # third bit marks grip button
		d['grip_button'] = bool(pControllerState.ulButtonPressed >> 2 & 1)
        
        # System button can't be read, if you press it
        # the controllers stop reporting
		return d

	#model control routine
	def control(self):
		localRotationAmount = 0
		localTranslationDelta = [0,0,0]
		leftTranslationDelta = [0,0,0]
		rightTranslationDelta = [0,0,0]
		localRotationAxis = [0,1,0]
		modified = 0
		trackpadRotationMatrix=numpy.array([[1,0,0,0],
		[0,1,0,0],
		[0,0,1,0],
		[0,0,0,1]], dtype = numpy.float32)
		
 
         #controllers
		if self.left_controller_id is None or self.right_controller_id is None:
			self.left_controller_id, self.right_controller_id = self.get_controller_ids()
            
		if self.left_controller_id or self.right_controller_id:
			#left controller
			if self.left_controller_id != None:
				currentpose= self.pose_array[self.left_controller_id]
				result, pControllerState = openvr.VRSystem().getControllerState(self.left_controller_id)
				controller_dict = self.from_controller_state_to_dict(pControllerState)
				#print(controller_dict,file=sys.stderr)
				#when we pause and bring up the menu, the model is shifted forward
				#when we quit the menu it is shifted back to it's original posiion
				if (controller_dict['menu_button'] == True and self.left_pause_pressed == False):
					self.paused = not self.paused
					self.left_pause_pressed = True
					if(self.paused):
						leftTranslationDelta[2]= leftTranslationDelta[2] -3
					else:
						leftTranslationDelta[2]= leftTranslationDelta[2] +3
				elif(controller_dict['menu_button'] == False):
					self.left_pause_pressed = False

				#print("pause:",file=sys.stderr)
				#print(self.paused,file=sys.stderr)

				
				#when you press on the trackpad, the model is translated in relation to where your finger is pressing
				if (controller_dict['trackpad_pressed'] == True and self.paused == False):
					leftTranslationDelta[0]= controller_dict['trackpad_x']/45
					leftTranslationDelta[2]= -controller_dict['trackpad_y']/45
				
				#touch the trackpad without pressing it to make the model spin on the y axis
				elif (controller_dict['trackpad_touched'] == True and self.paused == False):
					
					if (self.last_left_angle== 0):
						self.last_left_angle=math.asin(controller_dict['trackpad_y'])
						modified = 1
					
					else:
						#print("left track pad touched",file=sys.stderr)
						
						localRotationAmount = math.asin(controller_dict['trackpad_y']) - self.last_left_angle
						localRotationAxis = [0,1,0]
						numpy.matmul(self.trackpadRotationMatrix,self.get_rotation_matrix(localRotationAxis, localRotationAmount), out = self.trackpadRotationMatrix)
						self.last_left_angle=math.asin(controller_dict['trackpad_y'])
						modified = 1
				#pulling the trigger activates the code that handles drag
				#only one controller at time can be the one who is dragging
				if(controller_dict['trigger'] == 1.0 and self.lockedRotation !=2 and self.paused == False):
					#print("left trigger touched. left controller position: ",file=sys.stderr)
					#print(self.get_controller_pos(self.left_controller_id),file=sys.stderr)
					if (self.left_isdragging == False):
						self.left_isdragging = True
						self.last_left_pos = self.get_controller_pos(self.left_controller_id)
						self.controllerRotationMatrix_reset=numpy.linalg.inv(self.get_controller_rotation(self.left_controller_id))
						self.lockedRotation = 1
					
					elif(currentpose.bPoseIsValid):
						#print("valide pose.",file=sys.stderr)
						leftTranslationDelta = self.getDelta(self.get_controller_pos(self.left_controller_id), self.last_left_pos)
						
						self.controllerRotationMatrix=self.get_controller_rotation(self.left_controller_id)
						numpy.matmul(self.controllerRotationMatrix,self.controllerRotationMatrix_reset,out=self.controllerRotationMatrix)
						numpy.matmul(self.controllerRotationMatrix_static,self.controllerRotationMatrix,out=self.controllerRotationMatrix)
						
						#print("local delta,from the left controller:",file=sys.stderr)
						#print(leftTranslationDelta,file=sys.stderr)
						self.last_left_pos = self.get_controller_pos(self.left_controller_id)
						self.lockedRotation = 1
					else:
						self.left_isdragging = False
						leftTranslationDelta =[0,0,0]
				else:
					self.left_isdragging = False
					#leftTranslationDelta =[0,0,0]
					if(self.lockedRotation !=2):
						self.controllerRotationMatrix_static=self.controllerRotationMatrix
					self.lockedRotation = 0

			#right controller
			if self.right_controller_id != None:
				currentpose= self.pose_array[self.right_controller_id]
				result, pControllerState = openvr.VRSystem().getControllerState(self.right_controller_id)
				controller_dict = self.from_controller_state_to_dict(pControllerState)
				#print(controller_dict,file=sys.stderr)
				#pause
				if (controller_dict['menu_button'] == True and self.right_pause_pressed == False):
					self.paused = not self.paused
					self.right_pause_pressed = True
					if(self.paused):
						rightTranslationDelta[2]= rightTranslationDelta[2] -3
					else:
						rightTranslationDelta[2]= rightTranslationDelta[2] +3
				elif(controller_dict['menu_button'] == False):
					self.right_pause_pressed = False
				#print("pausa:",file=sys.stderr)
				#print(self.paused,file=sys.stderr)
				#translating using the trackpad
				if (controller_dict['trackpad_pressed'] == True and self.paused == False):
					rightTranslationDelta[0]= controller_dict['trackpad_x']/45
					rightTranslationDelta[2]= -controller_dict['trackpad_y']/45
				#gira
				elif (controller_dict['trackpad_touched'] == True and self.paused == False):
					
					if (self.last_right_angle== 0):
						self.last_right_angle= math.asin(controller_dict['trackpad_y'])
						modified = 1
					
					else:
						#print("trackpad destro toccato. rotationAmount:",file=sys.stderr)
						localRotationAmount = math.asin(controller_dict['trackpad_y']) - self.last_right_angle
						#print(localRotationAmount,file=sys.stderr)
						localRotationAxis = [0,0,1]
						numpy.matmul(self.trackpadRotationMatrix,self.get_rotation_matrix(localRotationAxis, localRotationAmount), out = self.trackpadRotationMatrix)
						self.last_right_angle= math.asin(controller_dict['trackpad_y'])
						modified = 1
				#drag
				if(controller_dict['trigger'] == 1.0 and self.lockedRotation != 1 and self.paused == False):
					#print("trigger destro toccato.",file=sys.stderr)
					#print(self.get_controller_pos(self.right_controller_id),file=sys.stderr)
					if (self.right_isdragging == False):
						self.right_isdragging = True
						self.last_right_pos = self.get_controller_pos(self.right_controller_id)
						self.controllerRotationMatrix_reset=numpy.linalg.inv(self.get_controller_rotation(self.right_controller_id))
						self.lockedRotation = 2

					elif(currentpose.bPoseIsValid):
						#print("posa valida.",file=sys.stderr)
						rightTranslationDelta = self.getDelta(self.get_controller_pos(self.right_controller_id),self.last_right_pos)
						self.last_right_pos=self.get_controller_pos(self.right_controller_id)
						
						self.controllerRotationMatrix = self.get_controller_rotation(self.right_controller_id)
						numpy.matmul(self.controllerRotationMatrix,self.controllerRotationMatrix_reset,out=self.controllerRotationMatrix)
						numpy.matmul(self.controllerRotationMatrix_static,self.controllerRotationMatrix,out=self.controllerRotationMatrix)
						self.lockedRotation = 2
					
					else:
						self.right_isdragging = False
						rightTranslationDelta =[0,0,0]				
				else:
					self.right_isdragging = False
					#rightTranslationDelta =[0,0,0]
					if (self.lockedRotation !=1):
						self.controllerRotationMatrix_static=self.controllerRotationMatrix
					self.lockedRotation = 0

		if (modified == 0):
			self.last_left_angle = 0
			self.last_right_angle = 0

		localTranslationDelta =self.getFinalDelta(leftTranslationDelta,rightTranslationDelta)
		#print("local translation delta:",file=sys.stderr)
		#print(localTranslationDelta,file=sys.stderr)
		numpy.matmul(self.controllerRotationMatrix,self.trackpadRotationMatrix,out=self.rotationMatrix)
		
		#numpy.matmul(self.rotationMatrix,localRotationMatrix,out=self.rotationMatrix)
		#self.rotationMatrix = localRotationMatrix
		
		
		self.translationDelta = self.getFinalDelta(self.translationDelta,localTranslationDelta)
		#print("final translation delta:",file=sys.stderr)
		#print(self.translationDelta,file=sys.stderr)           

            
    

		return self.translationDelta,self.rotationMatrix

		#menu control
	def menuControl(self):
		status=self.menuStatus.menu_dict
		#print("entering menu control, menu status:",file=sys.stderr)
		#print("stato:",file=sys.stderr)
		#print(status,file=sys.stderr)
		status['modified'] = False


		if self.left_controller_id is None or self.right_controller_id is None:
			self.left_controller_id, self.right_controller_id = self.get_controller_ids()
		if self.left_controller_id or self.right_controller_id:
			#print("there is at least one controller",file=sys.stderr)
			#left controller
			if self.left_controller_id != None:
				#print("left controller:",file=sys.stderr)
				currentpose= self.pose_array[self.left_controller_id]
				result, pControllerState = openvr.VRSystem().getControllerState(self.left_controller_id)
				controller_dict = self.from_controller_state_to_dict(pControllerState)
				#print(controller_dict,file=sys.stderr)
				if (controller_dict['menu_button'] == True and self.left_menu_enabled == False):
					status['enabled'] = not status['enabled']
					status['modified'] = True
					#print("pause was pressed",file=sys.stderr)
					self.left_menu_enabled = True
				elif(controller_dict['menu_button'] == False):
					self.left_menu_enabled = False
				#print("paused:",file=sys.stderr)
				#print(self.paused,file=sys.stderr)
				#print("menu is visible:",file=sys.stderr)
				#print(status['enabled'],file=sys.stderr)
				if (controller_dict['trackpad_pressed'] == True and self.paused == True and self.left_trackpad_pressed == False):
					self.left_trackpad_pressed= True
					status['modified'] = True
					trackpad_y= controller_dict['trackpad_y'] 
					trackpad_x= controller_dict['trackpad_x']
					#print("modified flag is true",file=sys.stderr)
				
					if (trackpad_y > -0.3 and trackpad_y < 0.5 and trackpad_x> 0.5 ):
						self.menuStatus.augmentSelectedParam()
					elif (trackpad_y > -0.3 and trackpad_y < 0.5 and trackpad_x< -0.5 ):
						self.menuStatus.diminishSelectedParam()
					elif (trackpad_y < -0.6 ):
						self.menuStatus.selectNextParam()
					elif (trackpad_y > 0.6 ):
						self.menuStatus.selectPrevParam()
					else:
						selected= self.menuStatus.getSelectedParam()
						if (selected == "re-render" and self.re_rendering == False and self.standalone_mode == False):
							#print("re-rendering has been selected",file=sys.stderr)
							output_string= self.packParametersIntoOutputString(self.menuStatus.menu_dict)
							#print("apro il file:",file=sys.stderr)
							#this writes to a file that the segmenting program is waiting to be modified
							outputfile = open(self.temp_output_file_location,"w") 
							#print("writing to file",file=sys.stderr)
							
							outputfile.write(output_string)
							outputfile.close()
							self.temp_file_modified = os.path.getmtime(self.temp_output_file_location)
							self.re_rendering = True
							status['re-rendering']= True

				elif(controller_dict['trackpad_pressed'] == False):
					self.left_trackpad_pressed= False



			#right controller
			if self.right_controller_id != None:
				#print("right controller:",file=sys.stderr)
				currentpose= self.pose_array[self.right_controller_id]
				result, pControllerState = openvr.VRSystem().getControllerState(self.right_controller_id)
				controller_dict = self.from_controller_state_to_dict(pControllerState)
				#print(controller_dict,file=sys.stderr)
				if (controller_dict['menu_button'] == True and self.right_menu_enabled == False):
					status['enabled'] = not status['enabled']
					status['modified'] = True
					self.right_menu_enabled = True
				elif(controller_dict['menu_button'] == False):
					self.right_menu_enabled = False
				#print("pause:",file=sys.stderr)
				#print(self.paused,file=sys.stderr)
				#print("is menu visible :",file=sys.stderr)
				#print(status['enabled'],file=sys.stderr)
				#parameter selection and modification 
				if (controller_dict['trackpad_pressed'] == True and self.paused == True and self.right_trackpad_pressed == False):
					self.right_trackpad_pressed= True
					trackpad_y= controller_dict['trackpad_y'] 
					trackpad_x= controller_dict['trackpad_x']
					status['modified'] = True
					print("ho premuto e risulta modificato",file=sys.stderr)
					if (trackpad_y > -0.3 and trackpad_y < 0.5 and trackpad_x> 0.5 ):
						self.menuStatus.augmentSelectedParam()
					elif (trackpad_y > -0.3 and trackpad_y < 0.5 and trackpad_x< -0.5 ):
						self.menuStatus.diminishSelectedParam()
					elif (trackpad_y < -0.6 ):
						self.menuStatus.selectNextParam()
					elif (trackpad_y> 0.6 ):
						self.menuStatus.selectPrevParam()
					else:
						selected= self.menuStatus.getSelectedParam()
						if (selected == "re-render" and self.re_rendering == False and self.standalone_mode == False):
							#print("re-rendering has been selected",file=sys.stderr)
							output_string= self.packParametersIntoOutputString(self.menuStatus.menu_dict)
							#print("apro il file:",file=sys.stderr)
							#this writes to a file that the segmenting program is waiting to be modified
							outputfile =open(self.temp_output_file_location,"w") 
							#print("writing to file",file=sys.stderr)
							
							outputfile.write(output_string)
							outputfile.close()
							self.temp_file_modified = os.path.getmtime(self.temp_output_file_location)
							self.re_rendering = True
							status['re-rendering']= True
				elif(controller_dict['trackpad_pressed'] == False):
					self.right_trackpad_pressed= False



		self.menuStatus.menu_dict = status
		return status,self.menuStatus.getSelectedParam()

