#! usr/bin/env python

"""
This file contains models for grids.
"""

class QuadraticGrid(object):
	"""
	AKA Cartesian Grid.
	"""
	
	def __init__(self, grid_width, grid_height):
		self.__grid = [[untaken for i in range(grid_width)] for j in range(grid_height)]
	
	@property
	def grid(self):
		return self.__grid
	
	def __incr(self, index):
		if index == (len(self.grid) - 1):
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
		
		Test cases:
			The grid is just one row.
			
			The grid is just one column.
		"""
		rows = self.__list_unique(row, self.__incr(row), self.__decr(row))
		cols = self.__list_unique(col, self.__incr(col), self.__decr(col))
		adjacent = []
		
		# Cartesian product rows and cols, sans the combination (rows, cols)
		for i in range(len(rows)):
			for j in range(len(cols)):
				if rows[i] == row and cols[j] == col:
					pass
				else:
					adjacent.append((rows[i], cols[j]))
		
		return adjacent
