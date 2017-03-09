
import os
import glob
import unittest

class TestC(unittest.TestCase):

	path = ''
	parser = None
	def setup(self, parser, p='testcases'):
		self.path = p
		self.parser = parser
		

	def runTest(self):
		print('-------- test mode --------')
		try:
			
			for file in glob.glob(os.path.join(self.path, '*.co')):
				print('checking ' + str(file))
				f = open(file,'r')
				data = f.read()
				f.close()
				#Se aplica la gramatica
				if self.parser.parse(data, tracking=True) == 'ok':
					print('Test ok')
				else:
					print('Error')				
		except EOFError:
			print(EOFError)
