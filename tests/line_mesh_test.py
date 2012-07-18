#! usr/bin/env python

from ..components.core import GameLoop, GameLoopEvents, GameConfig, Colors
from ..components.shapes import Point, PointShape

import random

"""
Demo stuff for PointShape.
"""

class LineMesh(GameLoopEvents):
	"""
	Creates a line mesh with a triangle for its initial shape.
	
	You can change the number of mutations the triangle undergoes
	by setting self.__limit.
	
	I want a 500x500 window!
	"""
	
	def __init__(self, config):
		super(LineMesh, self).__init__(config)
		self.__limit = 200
		self.__count = 0
		
		self.__triangle = PointShape([Point(250, 50), Point(50, 350), Point(400, 250)])
	
	def loop_invariant(self):
		return self.__count < self.__limit
	
	def loop_event(self):
		self.window.fill(Colors.WHITE)
		self.__triangle.draw(self.window)
		self.__triangle.add_point(Point(random.randint(0, 500), random.randint(0, 500)))
		
		self.__count += 1

config = GameConfig()
config.window_size = [500, 500]
config.clock_rate = 10
config.window_title = "Line Mesh"
ms = LineMesh(config)
game_loop = GameLoop(ms)
game_loop.go()
