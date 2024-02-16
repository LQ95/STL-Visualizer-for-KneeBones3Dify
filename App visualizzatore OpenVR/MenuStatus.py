
#classe ausiliaria per gestire lo stato del menù fuori dalla classe di controllo

class MenuStatus(object):
	def __init__(self):
		self.menu_dict = {}

		#parametri da dare alla app che rifà la generazione del modello 3D
		self.menu_dict['intensity_threshold'] = 600
		self.menu_dict['convex_hull_dilation'] = 6
		self.menu_dict['final_closing'] = 8
		self.menu_dict['protrusion_removal'] = 3
		self.menu_dict['final_dilation'] = 1

		#parametri necessari per il controllo
		self.menu_dict['enabled'] = False
		self.menu_dict['modified'] = False
		self.menu_dict['re-rendering'] = False

		#parametri interni
		self.param_array= ('intensity_threshold','convex_hull_dilation','final_closing','protrusion_removal','final_dilation','re-render')
		self.selected_param = 0


	def getSelectedParam(self):
		return self.param_array[self.selected_param]

	#selezione
	def selectNextParam(self):
		curr_param=self.selected_param+1
		array_length=len(self.param_array)
		if(curr_param < array_length):
			self.selected_param += 1
		elif(curr_param >= array_length ):
			self.selected_param = 0


	def selectPrevParam(self):
		curr_param=self.selected_param-1
		array_length=len(self.param_array)
		if(curr_param >= 0):
			self.selected_param -= 1
		elif(curr_param < 0 ):
			self.selected_param = array_length -1

	#modifica
	def augmentSelectedParam(self):
		param=self.getSelectedParam()
		quantity=1
		if (param == "intensity_threshold"):
			quantity = 50
		if (param == "re-render"):
			return
		self.menu_dict[param] += quantity

	def diminishSelectedParam(self):
		param=self.getSelectedParam()
		quantity=1
		if (param == "intensity_threshold"):
			quantity = 50
		if (param == "re-render"):
			return
		if(self.menu_dict[param] > 0):
			self.menu_dict[param] -= quantity




