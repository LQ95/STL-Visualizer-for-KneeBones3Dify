import unittest
from TextureControl import TextureControl


class TextureControlTest(unittest.TestCase):

	
	width = 300

	tex_cont=TextureControl(width)
	height = tex_cont.height
	menu_dict = {}

		
	menu_dict['intensity_threshold'] = 600
	menu_dict['convex_hull_dilation'] = 6
	menu_dict['final_closing'] = 8
	menu_dict['protrusion_removal'] = 3
	menu_dict['final_dilation'] = 1


	def test_generate(self):
		texoutput=self.tex_cont.generateTexture(self.menu_dict,'intensity_threshold')
		self.assertEqual(len(texoutput),self.width * self.height)

	def test_flag_rerendering(self):
		self.tex_cont.flagRerendering()
		self.assertEqual(self.tex_cont.parameterTextDescriptions['re-render'], "Re-rendering,\n please wait")

	def test_unflag_rerendering(self):
		self.tex_cont.unflagRerendering()
		self.assertEqual(self.tex_cont.parameterTextDescriptions['re-render'], "Re-render")

		



if __name__ == '__main__':
    unittest.main()