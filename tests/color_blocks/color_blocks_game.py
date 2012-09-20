#! usr/bin/env python

from ...components.core import Colors
from ...components.core import GameConfig
from ...components.core import GameScreen

from color_blocks_model import ColorBlocksModel

class ColorBlocksScreen(GameScreen):
	
	def __init__(self, dimensions, grid_size):
		"""
		Instantiates a ColorBlocksScreen instance.
		
		@param dimensions
		  The dimensions of the screen. An iterable whose first element
		  is taken for the width while the second one is taken for the
		  height.
		@param grid_size
		  The size of the grid, in squares per dimension. First element
		  is taken for the width while the second one is taken for the
		  height.
		"""
		super(GameScreen, self).__init__(dimensions)
		self.__game_model = ColorBlocksModel(grid_size[0], grid_size[1])
	
	@property
	def game_model(self):
		return self.__game_model
