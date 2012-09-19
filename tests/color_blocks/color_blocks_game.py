#! usr/bin/env python

from ...components.core import Colors
from ...components.core import GameConfig
from ...components.core import GameScreen

class ColorBlocksScreen(GameScreen):
	
	def __init__(self, dimensions):
		super(GameScreen, self).__init__(dimensions)
