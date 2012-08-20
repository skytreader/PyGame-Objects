#! usr/bin/env python

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
		self.__grid = [[untaken for i in range(grid_width)] for j in range(grid_height)]
		self.__populate()
	
	@property
	def grid(self):
		return self.__grid
	
	def __populate(self):
		height = len(self.grid)
		width = len(self.grid[0])
		block_index_max = len(ColorBlocksModel.BLOCKS) - 1
		
		for i in range(height):
			for j in range(width):
				block = ColorBlocksModel.BLOCKS[random.randint(0, block_index_max)]
				self.grid[i][j] = block
