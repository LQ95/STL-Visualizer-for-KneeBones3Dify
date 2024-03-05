import unittest



from MenuStatus import MenuStatus



class MenuStatusTest(unittest.TestCase):

	


	menu_stat=MenuStatus()

	def test01_init_param(self):
		param = self.menu_stat.getSelectedParam()
		
		self.assertEqual(param,'intensity_threshold')
	

	def test02_param_change(self):
		self.menu_stat.selectNextParam()
		param = self.menu_stat.getSelectedParam()
		
		self.assertNotEqual(param,'intensity_threshold')
		self.assertEqual(param,'convex_hull_dilation')

	def test03_param_unchange(self):
		self.menu_stat.selectPrevParam()
		param = self.menu_stat.getSelectedParam()
		
		self.assertEqual(param,'intensity_threshold')

	def test04_param_increase(self):
		param = self.menu_stat.getSelectedParam()
		
		self.menu_stat.augmentSelectedParam()
		self.assertEqual(self.menu_stat.menu_dict['intensity_threshold'], 650)
		self.menu_stat.augmentSelectedParam()
		self.menu_stat.augmentSelectedParam()
		self.menu_stat.augmentSelectedParam()
		self.assertEqual(self.menu_stat.menu_dict['intensity_threshold'], 800)

	def test05_param_increase(self):

		self.menu_stat.selectNextParam()
		
		self.menu_stat.augmentSelectedParam()
		self.assertEqual(self.menu_stat.menu_dict['convex_hull_dilation'], 7)
		self.menu_stat.augmentSelectedParam()
		self.menu_stat.augmentSelectedParam()
		self.menu_stat.augmentSelectedParam()
		self.assertEqual(self.menu_stat.menu_dict['convex_hull_dilation'], 10)

	def test06_param_decrease(self):

		
		self.menu_stat.diminishSelectedParam()
		self.assertEqual(self.menu_stat.menu_dict['convex_hull_dilation'], 9)
		self.menu_stat.diminishSelectedParam()
		self.menu_stat.diminishSelectedParam()
		self.menu_stat.diminishSelectedParam()
		self.assertEqual(self.menu_stat.menu_dict['convex_hull_dilation'], 6)

	def test07_param_decrease(self):

		
		self.menu_stat.diminishSelectedParam()
		self.assertEqual(self.menu_stat.menu_dict['convex_hull_dilation'], 5)
		self.menu_stat.diminishSelectedParam()
		self.menu_stat.diminishSelectedParam()
		self.menu_stat.diminishSelectedParam()
		self.assertEqual(self.menu_stat.menu_dict['convex_hull_dilation'], 2)

	def test08_param_decrease(self):

		self.menu_stat.selectPrevParam()
		self.menu_stat.diminishSelectedParam()
		self.assertEqual(self.menu_stat.menu_dict['intensity_threshold'], 750)
		self.menu_stat.diminishSelectedParam()
		self.menu_stat.diminishSelectedParam()
		self.menu_stat.diminishSelectedParam()
		self.assertEqual(self.menu_stat.menu_dict['intensity_threshold'], 600)

	def test09_previous_param_selection_looparound(self):


		self.menu_stat.selectPrevParam()
		param = self.menu_stat.getSelectedParam()
		self.assertEqual(param,'re-render')

		self.menu_stat.selectPrevParam()
		param = self.menu_stat.getSelectedParam()
		self.assertEqual(param,'final_dilation')

		self.menu_stat.selectPrevParam()
		param = self.menu_stat.getSelectedParam()
		self.assertEqual(param,'protrusion_removal')

		self.menu_stat.selectPrevParam()
		param = self.menu_stat.getSelectedParam()
		self.assertEqual(param,'final_closing')

		self.menu_stat.selectPrevParam()
		param = self.menu_stat.getSelectedParam()
		self.assertEqual(param,'convex_hull_dilation')

		self.menu_stat.selectPrevParam()
		param = self.menu_stat.getSelectedParam()
		self.assertEqual(param,'intensity_threshold')

		self.menu_stat.selectPrevParam()
		param = self.menu_stat.getSelectedParam()
		self.assertEqual(param,'re-render')


	def test10_next_param_selection_looparound(self):


		self.menu_stat.selectNextParam()
		param = self.menu_stat.getSelectedParam()
		self.assertEqual(param,'intensity_threshold')

		self.menu_stat.selectNextParam()
		param = self.menu_stat.getSelectedParam()
		self.assertEqual(param,'convex_hull_dilation')

		self.menu_stat.selectNextParam()
		param = self.menu_stat.getSelectedParam()
		self.assertEqual(param,'final_closing')

		self.menu_stat.selectNextParam()
		param = self.menu_stat.getSelectedParam()
		self.assertEqual(param,'protrusion_removal')

		self.menu_stat.selectNextParam()
		param = self.menu_stat.getSelectedParam()
		self.assertEqual(param,'final_dilation')

		self.menu_stat.selectNextParam()
		param = self.menu_stat.getSelectedParam()
		self.assertEqual(param,'re-render')

		self.menu_stat.selectNextParam()
		param = self.menu_stat.getSelectedParam()
		self.assertEqual(param,'intensity_threshold')

		


		
	

if __name__ == '__main__':
    unittest.main()