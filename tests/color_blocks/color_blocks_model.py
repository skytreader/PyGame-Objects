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
	
	def __init__(self, grid_width, grid_height):
		"""
		Initializes a Color Blocks game with the given parameters
		"""
		untaken = ColorBlocksModel.UNTAKEN
		self.__quadratic_grid = QuadraticGrid(grid_width, grid_height)
		self.__populate()
	
	@property
	def grid(self):
		return self.__quadratic_grid.grid
	
	@property
	def quadratic_grid(self):
		return self.__quadratic_grid
	
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
		
		TODO: We should only be checking in the four directions---no diagonals!
		"""
		adjacent_stack = [(row, col)]
		
		while len(adjacent_stack):
			cur_block = adjacent_stack.pop()
			adjacent_blocks = self.quadratic_grid.get_adjacent(cur_block[0], cur_block[1])
			adj_count = len(adjacent_blocks)
			
			for i in range(adj_count):
				block = adjacent_blocks[i]
				if self.grid[block[0]][block[1]] == self.grid[row][col]:
					adjacent_stack.insert(0, adjacent_blocks[i])
			
			self.grid[cur_block[0]][cur_block[1]] = ColorBlocksModel.UNTAKEN
