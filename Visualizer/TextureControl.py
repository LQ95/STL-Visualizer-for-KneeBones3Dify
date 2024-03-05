import numpy
from PIL import Image, ImageDraw, ImageFont,ImagePalette
import math
import sys
import os
class TextureControl(object):
	#initialized with a width, the size of everything else is computed from it
	def __init__(self,width):
		self.width=width
		self.height=math.ceil(self.width/1.5)
		self.fontsize = math.ceil(self.height/15)
		self.tex= Image.new('RGBA',(self.width,self.height), color= 'black')
		#self.palette=[0,0,0,255,0,0,255,255,255]
		self.fnt=ImageFont.truetype('arial.ttf', self.fontsize)
		self.draw= ImageDraw.Draw(self.tex)
		black_RGB=(0,0,0)
		white_RGB=(255,255,255)
		green_RGB=(0,255,0)
		black_grayscale=0
		white_grayscale=255
		grey_grayscale=128
		self.black=black_RGB
		self.white=white_RGB
		self.green=green_RGB
		self.default_fill_color = self.white
		self.highlighted_fill_color = self.green
		self.first_column_x = math.ceil(self.width/36)
		self.second_column_x = math.ceil(self.width/1.7)
		

		
		self.parameterCoordinates={
		'intensity_threshold':(self.first_column_x,math.ceil(self.height/5.8)),
		'convex_hull_dilation':(self.first_column_x,math.ceil(self.height/2.3)),
		'final_closing':(self.first_column_x,math.ceil(self.height/1.45)),
		'protrusion_removal':(self.second_column_x,math.ceil(self.height/5.8)),
		'final_dilation':(self.second_column_x,math.ceil(self.height/2.3)),
		're-render':(self.second_column_x,math.ceil(self.height/1.45))
		}

		self.parameterTextDescriptions={
		'intensity_threshold':"Intensity threshold",
		'convex_hull_dilation':"Convex hull dilation",
		'final_closing':"Final closing",
		'protrusion_removal':"Protrusion removal",
		'final_dilation':"Final dilation",
		're-render':"Re-render"
		}

		self.parameterValueTextDistance = math.ceil(self.fontsize*1.5)
		self.prevParameter='intensity_threshold'

	def generateTexture(self,menu_dict,selected_param):
		#self.tex.putpalette(self.palette)
		#genera l'immagine 
		tex=self.tex

		#Setup per scriverci sopra
		d = self.draw
		fnt = self.fnt

		logo_path = os.path.abspath(".\\logo\\KneeBones3Dify_logo.png")
		logo = Image.open(logo_path )
		logo = logo.resize( (math.ceil(self.width/3.7),math.ceil(self.height/4.6)) )
		logo_attachment_point_coords = (-math.ceil(self.width/78), -math.ceil(self.height/80))
		tex.paste(logo, logo_attachment_point_coords)
		default_fill_color = self.default_fill_color
		highlighted_fill_color = self.highlighted_fill_color
		text_fill_color = default_fill_color
		parameterCoordinates=self.parameterCoordinates
		param_value= ""
		#print ("GENERATING MENU TEXTURE",file=sys.stderr)
		#print(menu_dict,file=sys.stderr)
		#print("selected paramter:",file=sys.stderr)
		#print(selected_param,file=sys.stderr)
		#print ("\n\n\n\n\n",file=sys.stderr)
		
		#write
		#color the selected parameter differently
		title_coords=(math.ceil(self.width/2.75),math.ceil(self.height/70))

		d.text(title_coords, "Parameter Menu",font=fnt, fill=text_fill_color)

		if(selected_param == 'intensity_threshold'):
			text_fill_color = highlighted_fill_color
		

		param_coordinates= parameterCoordinates['intensity_threshold']
		d.text(param_coordinates, "Intensity threshold",font=fnt, fill=text_fill_color)
		param_value = str(menu_dict["intensity_threshold"])

		param_value_coords= (param_coordinates[0],param_coordinates[1] + self.parameterValueTextDistance)
		d.text(param_value_coords, param_value,font=fnt, fill=text_fill_color)

		text_fill_color = default_fill_color


		param_coordinates= parameterCoordinates['convex_hull_dilation']

		d.text(param_coordinates, "Convex hull dilation",font=fnt, fill=text_fill_color)
		param_value=str(menu_dict["convex_hull_dilation"])

		param_value_coords= (param_coordinates[0],param_coordinates[1] + self.parameterValueTextDistance)
		d.text(param_value_coords, param_value,font=fnt, fill=text_fill_color)
		


		param_coordinates= parameterCoordinates['final_closing']

		d.text(param_coordinates, "Final closing",font=fnt, fill=text_fill_color)
		param_value=str(menu_dict["final_closing"])

		param_value_coords= (param_coordinates[0],param_coordinates[1] + self.parameterValueTextDistance)
		d.text(param_value_coords, param_value,font=fnt, fill=text_fill_color)


		param_coordinates= parameterCoordinates['protrusion_removal']

		d.text(param_coordinates, "Protrusion removal",font=fnt, fill=text_fill_color)
		
		param_value=str(menu_dict["protrusion_removal"])
		param_value_coords= (param_coordinates[0],param_coordinates[1] + self.parameterValueTextDistance)
		d.text(param_value_coords, param_value,font=fnt, fill=text_fill_color)

		param_coordinates= parameterCoordinates['final_dilation']

		d.text(param_coordinates, "Final dilation",font=fnt, fill=text_fill_color)
		param_value=str(menu_dict["final_dilation"])
		
		param_value_coords= (param_coordinates[0],param_coordinates[1] + self.parameterValueTextDistance)
		d.text(param_value_coords, param_value,font=fnt, fill=text_fill_color)

		param_coordinates= parameterCoordinates['re-render']

		d.text(param_coordinates, "Re-render",font=fnt, fill=text_fill_color)

		tex.save('pil_test.png')

		


		#converting image into into numpy array
		tex_array= numpy.array(list(tex.getdata()))  
	
		return tex_array

	def modifyTexture(self,menu_dict,selected_param):
		#print ("MODIFYING MENU TEXTURE",file=sys.stderr)
		#print(menu_dict,file=sys.stderr)
		#print("selected parameter:",file=sys.stderr)
		#print(selected_param,file=sys.stderr)
		#print ("\n\n\n\n\n",file=sys.stderr)
		tex=self.tex
		#Setup needed to write on the texture
		d = self.draw
		fnt = self.fnt
		default_fill_color = self.default_fill_color
		highlighted_fill_color = self.highlighted_fill_color
		text_fill_color = highlighted_fill_color
		parameterValueTextDistance = self.parameterValueTextDistance

		#find the coordinates od the new paramter and of the one that was previously selected or modified
		param_coordinates=self.parameterCoordinates[selected_param]
		text_desc=self.parameterTextDescriptions[selected_param]

		if(selected_param !=self.prevParameter):
			text_fill_color = default_fill_color
			prev_param_coordinates=self.parameterCoordinates[self.prevParameter]
			prev_text_desc=self.parameterTextDescriptions[self.prevParameter]
			d.text(prev_param_coordinates, prev_text_desc,font=fnt, fill=text_fill_color)
			if(self.prevParameter !='re-render'):
				#If the previous paramter wasn't "re-render", the value is also printed
				prev_parameter_value_text_coords = (prev_param_coordinates[0],prev_param_coordinates[1] + parameterValueTextDistance)
				
				#only delete where the numeric value must be printed
				tex.paste( self.black, (prev_parameter_value_text_coords[0], prev_parameter_value_text_coords[1], prev_parameter_value_text_coords[0]+math.ceil(self.width/9), prev_parameter_value_text_coords[1]+self.fontsize))
				
				prev_param_value=str(menu_dict[self.prevParameter])
				d.text(prev_parameter_value_text_coords, prev_param_value,font=fnt, fill=text_fill_color)
			
			text_fill_color=highlighted_fill_color
			d.text(param_coordinates, text_desc,font=fnt, fill=text_fill_color)

		if(selected_param !='re-render'):
			
			parameter_value_text_coords = (param_coordinates[0],param_coordinates[1] + parameterValueTextDistance)
		
			#only delete where the numeric value must be changed
			tex.paste( self.black, (parameter_value_text_coords[0], parameter_value_text_coords[1], parameter_value_text_coords[0]+math.ceil(self.width/9), parameter_value_text_coords[1]+self.fontsize))

			param_value=str(menu_dict[selected_param])
			d.text(parameter_value_text_coords, param_value,font=fnt, fill=text_fill_color)


		self.prevParameter=selected_param

		tex_array= numpy.array(list(tex.getdata()))  

		return tex_array


	def flagRerendering(self):
		#print ("FLAGGING RE-RENDERING",file=sys.stderr)
		
		#print ("\n\n\n\n\n",file=sys.stderr)
		tex=self.tex
		#Setup needed to write on the texture
		d = self.draw
		fnt = self.fnt
		parameterCoordinates=self.parameterCoordinates

		param_coordinates= parameterCoordinates['re-render']

		d.text(param_coordinates, "Re-rendering,\n please wait",font=fnt, fill=self.highlighted_fill_color)
		self.parameterTextDescriptions['re-render']= "Re-rendering,\n please wait"
		tex_array= numpy.array(list(tex.getdata()))  

		return tex_array

	def unflagRerendering(self):
		#print ("RESTORING DEFAULT RENDER TEXT",file=sys.stderr)
		
		#print ("\n\n\n\n\n",file=sys.stderr)
		tex=self.tex
		#Setup per scriverci sopra
		d = self.draw
		fnt = self.fnt
		parameterCoordinates=self.parameterCoordinates
		param_coordinates= parameterCoordinates['re-render']
		tex.paste( self.black, (param_coordinates[0], param_coordinates[1], param_coordinates[0]+math.ceil(self.width/3), param_coordinates[1]+math.ceil(self.fontsize *2.2) ) )

		d.text(param_coordinates, "Re-render",font=fnt, fill=self.default_fill_color)
		self.parameterTextDescriptions['re-render']= "Re-render"

		tex_array= numpy.array(list(tex.getdata()))  

		return tex_array



	#these are unused and can be removed

	# def generateEmptyBackground(self, color):
	# 	img= list()

	# 	for i in range(30):
	# 		for j in range(20):
	# 			img.append([color[0],color[1],color[2],1.0])

	# 	return numpy.array(img)

	# def generateSampleImage(self):
	# 	img= list()

	# 	for i in range(30):
	# 		for j in range(20):
	# 			img.append([i*j/602,i*j/601,i*j/600,1.0])

	# 	return numpy.array(img)



