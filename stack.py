class Stack(object):
	"""docstring for Stack"""

	def __init__(self):
		super(Stack, self).__init__()
		self.stack = []

	def __str__(self):
		ret = ""
		for d in reversed(self.stack):
			ret = ret + str(d) + '\n'
		return str(ret)

	"""
	Length: returns amount of elements in the stack
	"""
	@property
	def length(self):
		return len(self.stack)

	"""
	Top: returns the top element of the stack
	"""
	@property
	def top(self):
		if self.length > 0:
			return self.stack[-1]
		return ' '
	@property
	def top2(self):
		if self.length > 1:
			return self.stack[-2]
		return ' '
	"""
	Push: appends element at the top of the stack
	"""
	def push(self, arg):
		self.stack.append(arg)


	"""
	Pop: removes the top element of the stack
	"""
	def pop(self):
		if self.length > 0:
			return self.stack.pop()