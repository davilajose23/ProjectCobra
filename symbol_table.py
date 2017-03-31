class functions_dir(object):
	'''docstring for functions_dir'''
	def __init__(self):
		super(functions_dir, self).__init__()
		''' 
			Las funciones son entradas en el diccionario functions.
			A cada funcion le corresponde de valor una lista.
			Esta lista contiene otro diccionario para varibales, y un return type, y cantidad de args
			Scope global del programa se inicia con diccionario de variables globales vacio.
			No se tiene un return type para el scope global.
			Scope es el function_id de cada funcion.
		'''
		self.functions = {}
		self.functions['global'] = [ None, {}, 0]

		# 0 es el indice de la lista de una funcion para accesar su return type
		self.return_type = 0

		# 1 es el indice de la lista de una funcion para accesar a su diccionario de variables
		self.variables_dict = 1

		# 2 es el indide de la lista de una funcion para indicar la cantidad de argumentos que espera
		self.expected_arguments = 2

		self.scope = 'global'
		self.evaluating = False
		self.last_type = None
		self.cont = 1

	# Add function to fuctions directory
	def add_function(self, function_id):
		# Verify if function already exists
		if self.functions.get(function_id, None) is not None:
			raise NameError('Function already declared! Function: ' + str(function_id))
		else:
			self.functions[function_id] = [None, {}, 0]

	# Validate function exists
	def validate_function(self, function_id):
		if self.functions.get(function_id, None) is None:
			raise ValueError('Function not declared! Name: ' + str(function_id))

	# Incrementa cantidad de argumentos esperados por una funcion
	def increase_expected_arguments(self):
		self.functions[self.scope][self.expected_arguments] += 1

	def set_return_type(self, function_return_type):
		self.functions[self.scope][self.return_type] = function_return_type

	# Change the current scope from global to function scope
	def set_scope(self, scope):
		self.scope = scope

	# Reset scope to global
	def reset_scope(self):
		self.scope = 'global'

	# Add variable to current scope
	def add_var(self, variable_id, var_type, value=0):
		# Consider, when making cuadruples, determine type and value
		if self.functions[self.scope][self.variables_dict].get(variable_id, None) is None:
			self.functions[self.scope][self.variables_dict][variable_id] = [value, var_type]
		else:
			raise KeyError('Variable already declared! Var: ' + str(variable_id))

	# Validate variable exists
	def validate_variable(self, variable_id):
		# Look for variable in current scope
		if self.functions[self.scope][self.variables_dict].get(variable_id, None) is None:
			# Look for variable in global scope
			if self.functions['global'][self.variables_dict].get(variable_id, None) is None:
				raise ValueError('Variable not declared! Var: ' + str(variable_id))

	def start_evaluating(self):
		self.evaluating = True

	def finish_evaluating(self):
		self.evaluating = False

	def set_type(self, last_type):
		self.last_type = last_type

	def get_func_dir(self):
		return self.functions

	def get_var(self, variable_id):
		if variable_id in self.functions[self.scope][self.variables_dict]:
			return self.functions[self.scope][self.variables_dict].get(variable_id)
		elif variable_id  in self.functions['global'][self.variables_dict]:
			return self.functions['global'][self.variables_dict].get(variable_id)
		return None

	@property
	def current_scope(self):
		return self.scope

	def printeame(self):
		print('************ Functions Directory ************\n')
		for key,val in self.functions.iteritems():
			pass
			print(str(val[0]) + ' ' + str(key) + '()')
			for k,v in val[1].iteritems():
				pass
				print('\t' + str(v[1]) + ' ' + str(k) + ' = ' + str(v[0]))
			print('')
		print('*********************************************')