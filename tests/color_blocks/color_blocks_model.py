#! usr/bin/env python

from ...helpers.grid import QuadraticGrid

import random

class ColorBlocksModel(object):
	"""
	A Color Blocks game will be represented by an n x m grid. Each cell
	will be represented by a character in ColorBlocksModel.BLOCKS . Since,
	when collapsing blocks, it will happen that the overall grid becomes
	less than the original, removed blocks will be represented by
	ColorBlocksModel.UNTAKEN .
	"""
	
	BLOCKS = "01234"
	UNTAKEN = "."
	
	def __init__(self, grid_width, grid_height, min_score = 1):
		"""
		Initializes a Color Blocks game with the given parameters
		
		@param grid_width
		@param grid_height
		@param min_score
		  The minimum number of blocks required to make a score.
		"""
		untaken = ColorBlocksModel.UNTAKEN
		self.__quadratic_grid = QuadraticGrid(grid_width, grid_height, True, False)
		self.__populate()
		self.__min_score = min_score
		self.__score = 0
	
	@property
	def grid(self):
		return self.__quadratic_grid.grid
	
	@property
	def quadratic_grid(self):
		return self.__quadratic_grid
	
	@property
	def min_score(self):
		return self.__min_score
	
	@min_score.setter
	def min_score(self, min_score):
		self.__min_score = min_score
	
	@property
	def score(self):
		return self.__score
	
	@score.setter
	def score(self, score):
		self.__score = score
	
	def __populate(self):
		height = len(self.grid)
		width = len(self.grid[0])
		block_index_max = len(ColorBlocksModel.BLOCKS) - 1
		
		for i in range(height):
			for j in range(width):
				block = ColorBlocksModel.BLOCKS[random.randint(0, block_index_max)]
				self.grid[i][j] = block
	
	def toggle(self, row, col):
		"""
		Removes the block at position (row, col) and all adjacent blocks of
		the same color.
		
		Returns the number of blocks removed from the grid.
		
		@param row
		  The row index of the block to be toggled.
		@param col
		  The column index of the block to be toggled.
		@return The number of blocks removed from the grid or false if the block
		indicated is untaken.
		"""
		points = 0
		original = self.grid[row][col]
		
		if original == ColorBlocksModel.UNTAKEN:
			return False
		
		adjacent_stack = [(row, col)]
		adj_same_color = []
		inspected = []
		
		while len(adjacent_stack):
			cur_block = adjacent_stack.pop()
			inspected.append(cur_block)
			adj_same_color.append(cur_block)
			adjacent_blocks = self.quadratic_grid.get_adjacent(cur_block[0], cur_block[1])
			adj_count = len(adjacent_blocks)
			
			for i in range(adj_count):
				block = adjacent_blocks[i]
				if self.grid[block[0]][block[1]] == original and \
				  block not in adjacent_stack and block not in inspected:
					adjacent_stack.append(adjacent_blocks[i])
		
		if len(adj_same_color) >= self.min_score:
			for cur_block in adj_same_color:
				self.grid[cur_block[0]][cur_block[1]] = ColorBlocksModel.UNTAKEN
				points += 1
		
		return points
	
	def __find_empty_column(self):
		"""
		Looks for empty columns in the grid. Returns the index of an
		empty column. If there are multiple empty columns, only the
		first one is returned. If there are no empty columns in the
		grid, the value -1 is returned.
		"""
		for col in range(self.grid[0]):
			empty_found = True
			
			for row in range(self.grid):
				if self.grid[row][col] != ColorBlocksModel.UNTAKEN:
					empty_found = False
					break
			
			if empty_found:
				return col
		
		return -1
	
	def __translate_empty_col(self, col_index):
		limit = len(self.grid[0])
		
		for i in range(self.grid):
			col = col_index + 1
			
			while col < limit:
				self.grid[i][col - 1] = self.grid[i][col]
	
	def collapse(self):
		"""
		Removes empty columns by "collapsing" the space left.
		"""
		empty_col = self.__find_empty_column()
		self.__translate_empty_col(empty_col)
	
	def __str__(self):
		board = ""
		height = len(self.grid)
		
		for i in range(height):
			board += str(self.grid[i]) + "\n"
		
		return board
