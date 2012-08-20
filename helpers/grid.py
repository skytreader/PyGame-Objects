#! usr/bin/env python

"""
This file contains models for grids.
"""

class QuadraticGrid(object):
	"""
	AKA Cartesian Grid.
	
	TODO: Raise errors for invalid indices.
	"""
	
	def __init__(self, grid_height, grid_width):
		self.__grid = [[i for i in range(grid_width)] for j in range(grid_height)]
	
	@property
	def grid(self):
		return self.__grid
	
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
		limit = len(items)
		unique = []
		
		for i in range(limit):
			if items[i] not in unique:
				unique.append(items[i])
		
		return unique
	
	def get_adjacent(self, row, col):
		"""
		Returns a list of all the adjacent cells to (row, col). The list
		contains tuples of the index coordinates of the adjacent blocks.
		"""
		rows = self.__list_unique(row, self.__incr(row, len(self.grid)), self.__decr(row))
		cols = self.__list_unique(col, self.__incr(col, len(self.grid[0])), self.__decr(col))
		adjacent = []
		
		# Cartesian product rows and cols, sans the combination (rows, cols)
		for i in range(len(rows)):
			for j in range(len(cols)):
				if rows[i] == row and cols[j] == col:
					pass
				else:
					adjacent.append((rows[i], cols[j]))
		
		return adjacent
