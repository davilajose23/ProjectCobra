class functions_dir(object):
	'''docstring for functions_dir'''
	def __init__(self):
		super(functions_dir, self).__init__()
		''' 
			Las funciones son entradas en el diccionario functions.
			A cada funcion le corresponde de valor una tupla.
			Esta tupla contiene otro diccionario para varibales, y un return type
			Scope global del programa se inicia con diccionario de variables globales vacio.
			No se tiene un return type para el scope global.
			Scope es el function_id de cada funcion.
		'''
		self.functions = {}
		self.functions['global'] = ({}, None)

		# 0 es el indice de la tupla de una funcion para accesar a su diccionario de variables
		self.variables_dict = 0

		# 1 es el indice de la tupla de una funcionpara accesar su return type
		self.return_type = 1
		self.scope = 'global'

	# Add function to fuctions directory
	def insert_function(self, function_id):
		# Verify if function already exists
		if self.functions.get(function_id) is not None:
			raise NameError('Function already declared!')
		else:
			self.functions[function_id] = ({}, None)

	# Validate function exists
	def validate_function(self, function_id):
		if self.functions.get(function_id) is None:
			raise ValueError('Function not declared')

	def set_return_type(self, function_id, function_return_type):
		self.fuctions[scope][return_type] = function_return_type

	# Change the current scope from global to function scope
	def set_scope(self, scope):
		self.scope = scope

	# Reset scope to global
	def reset_scope(self):
		self.scope = 'global'

	# Add variable to current scope
	def add_var(self, variable_id, value, var_type):
		self.functions[scope][variables_dict][variable_id] = (value, var_type)

	# Validate variable exists
	def validate_variable(self, variable_id):
		# Look for variable in current scope
		if self.functions[scope][variables_dict].get(variable_id) is None:
			# Look for variable in global scope
			if self.functions['global'][variables_dict].get(variable_id) is None:
				raise ValueError('Variable not declared!')

	@property
	def current_scope(self):
		return self.scope



		