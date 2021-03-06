import os
import glob
import unittest
#from parser import parser as global_parser

class TestC(unittest.TestCase):

	path = ''
	parser = None
	parser_copy = None

	def init(self, global_parser):
		self.parser_copy = global_parser
		

	def setUp(self):
		self.parser = self.parser_copy

	def tearDown(self):
		self.parser = None

	def custom_test_file(self, filename):
		try:
			file = glob.glob(os.path.join(self.path, 'testcases/' + filename))
			print('checking ' + str(file))
			f = open(str(file[0]), 'r')
			data = f.read()
			f.close()
			#Se aplica la gramatica
			if self.parser.parse(data, tracking=True) == 'ok':
				print('--------------------- OK ----------------------')
			else:
				print('-------------------- ERROR --------------------')
		except EOFError:
			print(EOFError)
		
	def test_call_function_ok(self):
		self.custom_test_file('call_function_test_ok.co')

	def test_condition_ok(self):
		self.custom_test_file('condition_test_ok.co')

	def test_condition_fail(self):
		self.custom_test_file('condition_test_fail.co')

	def test_for_ok(self):
		self.custom_test_file('for_i_from_to_ok.co')

	def test_for_fail(self):
		self.custom_test_file('for_i_from_to_fail.co')

	def test_function_ok(self):
		self.custom_test_file('function_test_ok.co')

	def test_function_fail(self):
		self.custom_test_file('function_test_fail.co')

	def test_main_ok(self):
		self.custom_test_file('main_test_ok.co')

	def test_main_fail(self):
		self.custom_test_file('main_test_fail.co')

	def test_variables_ok(self):
		self.custom_test_file('variables_test_ok.co')

	def test_variables_fail(self):
		self.custom_test_file('variables_test_fail.co')

	def test_while_ok(self):
		self.custom_test_file('while_test_ok.co')

	def test_while_fail(self):
		self.custom_test_file('while_test_fail.co')

	def runIT(self):
		unittest.main()

	def runTest(self):
		suite = unittest.TestLoader().loadTestsFromTestCase(TestC)
		alltests = unittest.TestSuite(suite)
		unittest.TextTestRunner().run(suite)

suite = unittest.TestLoader().loadTestsFromTestCase(TestC)
alltests = unittest.TestSuite(suite)
