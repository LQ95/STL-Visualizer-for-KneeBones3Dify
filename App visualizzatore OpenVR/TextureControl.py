import numpy
from PIL import Image, ImageDraw, ImageFont,ImagePalette
import math
class TextureControl(object):
	#inizializzato con la larghezza, il resto è tutto parametrizzato di conseguenza
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
		self.evidenced_fill_color = self.green
		self.first_column_x = math.ceil(self.width/36)
		self.second_column_x = math.ceil(self.width/1.7)
		

		
		self.parameterCoordinates={
		'intensity_threshold':(self.first_column_x,math.ceil(self.height/5.8)),
		'convex_hull_dilation':(self.first_column_x,math.ceil(self.height/2.3)),
		'final_closing':(self.first_column_x,math.ceil(self.height/1.45)),
		'protrusion_removal':(self.second_column_x,math.ceil(self.height/5.8)),
		'final_dilation':(self.second_column_x,math.ceil(self.height/2.3)),
		're-render':(self.second_column_x,math.ceil(self.height/1.16))
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

		logo_path = "C:\\Users\\mrapo\\Desktop\\KneeBones3Dify-main CODICE SU CUI SI DEVE LAVORARE\\logo\\KneeBones3Dify_logo.png"
		logo = Image.open(logo_path )
		logo = logo.resize( (math.ceil(self.width/3.7),math.ceil(self.height/4.6)) )
		logo_attachment_point_coords = (-math.ceil(self.width/78), -math.ceil(self.height/80))
		tex.paste(logo, logo_attachment_point_coords)
		default_fill_color = self.default_fill_color
		evidenced_fill_color = self.evidenced_fill_color
		text_fill_color = default_fill_color
		parameterCoordinates=self.parameterCoordinates
		param_value= ""
		print ("GENERO TEXTURE")
		print(menu_dict)
		print("parametro selezionato:")
		print(selected_param)
		print ("\n\n\n\n\n")
		#scrivi
		#evidenzia il testo del parametro selezionato
		title_coords=(math.ceil(self.width/2.75),math.ceil(self.height/70))

		d.text(title_coords, "Parameter Menu",font=fnt, fill=text_fill_color)

		if(selected_param == 'intensity_threshold'):
			text_fill_color = evidenced_fill_color
		print("evidenzia? text fill color:")
		print(text_fill_color)

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

		


		#converti
		tex_array= numpy.array(list(tex.getdata()))  
		#tex_bytes= tex.tobytes()    
		#min_val = numpy.min(img_array)
		#max_val = numpy.max(img_array)
		#img_array_normalized = (img_array - min_val) / (max_val - min_val)
		return tex_array

	def modifyTexture(self,menu_dict,selected_param):
		print ("MODIFICO TEXTURE")
		print(menu_dict)
		print("parametro selezionato:")
		print(selected_param)
		print ("\n\n\n\n\n")
		tex=self.tex
		#Setup per scriverci sopra
		d = self.draw
		fnt = self.fnt
		default_fill_color = self.default_fill_color
		evidenced_fill_color = self.evidenced_fill_color
		text_fill_color = evidenced_fill_color
		parameterValueTextDistance = self.parameterValueTextDistance

		#ritrova le coordinate del parametro nuovo e del parametro precedentemente evidenziato o modificato
		param_coordinates=self.parameterCoordinates[selected_param]
		text_desc=self.parameterTextDescriptions[selected_param]

		if(selected_param !=self.prevParameter):
			text_fill_color = default_fill_color
			prev_param_coordinates=self.parameterCoordinates[self.prevParameter]
			prev_text_desc=self.parameterTextDescriptions[self.prevParameter]
			d.text(prev_param_coordinates, prev_text_desc,font=fnt, fill=text_fill_color)
			if(self.prevParameter !='re-render'):
				#se non ho selezionato opzione re render stampa valore numerico
				prev_parameter_value_text_coords = (prev_param_coordinates[0],prev_param_coordinates[1] + parameterValueTextDistance)
				prev_param_value=str(menu_dict[self.prevParameter])
				d.text(prev_parameter_value_text_coords, prev_param_value,font=fnt, fill=text_fill_color)
			
			text_fill_color=evidenced_fill_color
			d.text(param_coordinates, text_desc,font=fnt, fill=text_fill_color)

		if(selected_param !='re-render'):
			#se non ho selezionato opzione re render stampa valore numerico
			parameter_value_text_coords = (param_coordinates[0],param_coordinates[1] + parameterValueTextDistance)
		
			#cancella solo l'area dove bisogna riscrivere il valore
			tex.paste( self.black, (parameter_value_text_coords[0], parameter_value_text_coords[1], parameter_value_text_coords[0]+math.ceil(self.width/9), parameter_value_text_coords[1]+self.fontsize))

			param_value=str(menu_dict[selected_param])
			d.text(parameter_value_text_coords, param_value,font=fnt, fill=text_fill_color)


		self.prevParameter=selected_param

		tex_array= numpy.array(list(tex.getdata()))  

		return tex_array


	def generateEmptyBackground(self, color):
		img= list()

		for i in range(30):
			for j in range(20):
				img.append([color[0],color[1],color[2],1.0])

		return numpy.array(img)

	def generateSampleImage(self):
		img= list()

		for i in range(30):
			for j in range(20):
				img.append([i*j/602,i*j/601,i*j/600,1.0])

		return numpy.array(img)



