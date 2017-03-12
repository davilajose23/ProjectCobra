class functions_dir(object):
	'''docstring for functions_dir'''
	def __init__(self):
		super(functions_dir, self).__init__()
		self.scope = 'global'
		self.functions = {}
		self.functions['global'] = ({}, None)
		self.variables_dict = 0
		self.return_type = 1

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
	def scope(self):
		return self.scope



		