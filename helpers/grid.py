#! usr/bin/env python

import math

"""
This file contains models for grids.
"""

class DimensionException(Exception):
	"""
	Use this exception when indicating wrong dimensions for
	grids (i.e., if you set a minimum/maximum dimensions for
	your grids).
	"""
	
	def __init__(self, msg):
		self.msg = msg
	
	def __str__(self):
		return str(msg)

class Grid(object):
	"""
	A grid must be drawable (and traversable)!
	"""
	
	def draw_grid(self, window, x_offset, y_offset):
		"""
		Subclasses must implement this!
		"""
		pass
	
	def traverse(self):
		"""
		TODO: What happens here? :\
		"""
		pass

class QuadraticGrid(Grid):
	"""
	AKA Cartesian Grid.
	
	TODO: Raise errors for invalid indices.
	"""
	
	def __init__(self, grid_width, grid_height, hv_neighbors = True, diag_neighbors = True):
		"""
		Creates an instance of a quadratic grid.
		
		@param grid_width
		@param grid_height
		@param hv_neighbors
		  If set to true, we consider the blocks above and below, left and right
		  of a given block as a block's neighbors.
		  
		  Defaults to true.
		@param diag_neighbors
		  If set to true, we consider the blocks at the upper left/right and lower
		  left/right of a given block as a block's neighbors.
		  
		  Defaults to true.
		"""
		super(QuadraticGrid, self).__init__()
		
		if type(grid_width) != type(0) or type(grid_height) != type(0):
			raise TypeError("Grid dimensions must be specified as ints.")
		
		if grid_width <= 0 or grid_height <= 0:
			raise ValueError("Grid dimensions must be positive.")
		
		self.__grid = [[i for i in range(grid_width)] for j in range(grid_height)]
		self.__hv_neighbors = hv_neighbors
		self.__diag_neighbors = diag_neighbors
	
	@property
	def grid(self):
		return self.__grid
	
	@property
	def hv_neighbors(self):
		return self.__hv_neighbors
	
	@hv_neighbors.setter
	def hv_neighbors(self, hvn):
		self.__hv_neighbors = hvn
	
	@property
	def diag_neighbors(self):
		return self.__diag_neighbors
	
	@diag_neighbors.setter
	def diag_neighbors(self, dn):
		self.__diag_neighbors = dn
	
	def __incr(self, index, dimension_length):
		if index == (dimension_length - 1):
			return index
		else:
			return index + 1
	
	def __decr(self, index):
		if index == 0:
			return index
		else:
			return index - 1
	
	def __list_unique(self, *items):
		unique = []
		
		for i in items:
			if i not in unique:
				unique.append(i)
		
		return unique
	
	def __hv_adj(self, current_block, is_height):
		"""
		Returns the adjacent list for only one dimension as determined
		by argument is_height.
		
		The return value is a list of tuples.
		"""
		adjacent = []
		
		if is_height:
			dim_len = len(self.grid)
			static_index = 1
			trans_index = 0
		else:
			dim_len = len(self.grid[0])
			static_index = 0
			trans_index = 1
		
		move_dim = current_block[trans_index]
		
		increased = self.__incr(move_dim, dim_len)
		decreased = self.__decr(move_dim)
		
		if increased == move_dim:
			pass
		else:
			t = []
			t.insert(trans_index, increased)
			t.insert(static_index, current_block[static_index])
			adjacent.append(tuple(t))
		
		if decreased == move_dim:
			pass
		else:
			t = []
			t.insert(trans_index, decreased)
			t.insert(static_index, current_block[static_index])
			adjacent.append(tuple(t))
		
		return adjacent
	
	def __diag_adj(self, current_block):
		"""
		Returns _the whole_ adjacent list of diagonals (in contrast to
		__hv_adj) above.
		"""
		row = current_block[0]
		col = current_block[1]
		
		rows = self.__list_unique(self.__incr(row, len(self.grid)), self.__decr(row))
		cols = self.__list_unique(self.__incr(col, len(self.grid[0])), self.__decr(col))
		adjacent = []
		
		for i in range(len(rows)):
			for j in range(len(cols)):
				if rows[i] != row and cols[j] != col:
					adjacent.append((rows[i], cols[j]))
		
		return adjacent
	
	def get_adjacent(self, row, col):
		"""
		Returns a list of all the adjacent cells to block (row, col), depending
		on the set-up of the invoking object. The return list contains tuples of
		the index coordinates of the adjacent blocks.
		"""
		
		if type(row) != type(0) or type(col) != type(0):
			raise TypeError("Parameters should be of type int.")
		
		if row > len(self.grid) or col > len(self.grid[0]) or row < 0 or col < 0:
			raise IndexError("Invalid index!")
		
		current_block = (row, col)
		hv_adj = []
		diag_adj = []
		
		if self.hv_neighbors:
			hv_rows = self.__hv_adj(current_block, True)
			hv_cols = self.__hv_adj(current_block, False)
			hv_adj = hv_rows
			limit = len(hv_cols)
			
			for i in range(limit):
				hv_adj.append(hv_cols[i])
		
		if self.diag_neighbors:
			diag_adj = self.__diag_adj(current_block)
		
		limit = len(hv_adj)
		for i in range(limit):
			if hv_adj[i] not in diag_adj and hv_adj[i] != current_block:
				diag_adj.append(hv_adj[i])
		
		return diag_adj

class TriangularGrid(Grid):
	"""
	Represents a triangular grid.
	"""
	
	def __init__(self, grid_width, grid_height):
		"""
		Given the grid width and the grid height, we determine the origin
		to be (floor(grid_width/2), floor(grid_height/2)). Take note of
		this.
		
		Indices less than the origin coordinates are taken as negative.
		Use these indices when referring to points in this grid.
		"""
		super(Grid, self).__init__()
		self.__origin_x = math.floor(grid_width / 2)
		self.__origin_y = math.floor(grid_height / 2)
