import numpy as np
class Node:
    def __init__(self, id = None, name = None, in_channels = 1, out_channels = 1, kernel_size = 3, 
    	stride = 1, padding = 0):
    	self.fa = np.array([], dtype = str)
    	self.next = np.array([], dtype = str)
    	self.id = id
    	self.name = name
    	self.in_channels = in_channels
    	self.out_channels = out_channels
    	self.kernel_size = kernel_size
    	self.stride = stride
    	self.padding = padding
    	self.in_shape = np.array([], dtype = int)
    	self.out_shape = np.array([], dtype = int)

    def add_fa(self, f):
    	self.fa = np.append(self.fa, f)
    def add_next(self, nx):
    	self.next = np.append(self.next, nx)


class Vector:
	def __init__(self):
		self.n = 0
		self.N = 1000
		self.arr = np.empty(self.N, dtype = Node)

	def get(self, indx):
		if not 0 <= indx < self.n:
			raise ValueError('invalid index')
		return self.arr[indx]
	def push_back(self, node):
		if self.n == self.N :
			self.arr = np.concatenate((self.arr, np.empty(1000, dtypte = Node)))
			self.N = self.N + 1000
		self.arr[self.n] = node
		self.n = self.n + 1	
	def delete(self, indx):
		if not 0 <= indx < self.n:
			raise ValueError('invalid index')
		while indx < self.n - 1:
			self.arr[indx] = self.arr[indx + 1]
			indx = indx + 1
		self.n = self.n - 1
	def empty(self):
		return self.n == 0
	def size(self):
		return self.n
