import os
import glob
import unittest

class TestC(unittest.TestCase):

	path = ''
	parser = None
	parser_copy = None

	def set_up(self, parser, p='testcases'):
		self.parser_copy = parser
		self.path = p

	def setUp(self):
		self.parser = self.parser_copy

	def tearDown(self):
		self.parser = None

	def custom_test_file(self, filename):
		try:
			file = glob.glob(os.path.join(self.path, filename))
			print('checking ' + str(file))
			f = open(file, 'r')
			data = f.read()
			f.close()
			#Se aplica la gramatica
			if self.parser.parse(data, tracking=True) == 'ok':
				print('-------------------- OK --------------------')
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

suite = unittest.TestLoader().loadTestsFromTestCase(TestC)
alltests = unittest.TestSuite(suite)