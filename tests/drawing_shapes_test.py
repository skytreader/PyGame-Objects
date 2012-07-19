#! usr/bin/env python

from ..components.core import GameLoopEvents
from ..components.core import GameConfig
from ..components.core import GameLoop
from ..components.core import Colors

from ..components.shapes import PointShape
from ..components.shapes import Point

import pygame

"""
Shows a four-sided figure gliding across the screen.

@author Chad Estioco
"""

class RandomDrawing(GameLoopEvents):
	"""
	Wanted to draw a rectangle but oh, what the hey...ended up with
	an arrow-like object! :))
	"""
	
	def __init__(self, config):
		super(RandomDrawing, self).__init__(config)
		self.__ps = PointShape()
		self.__ps.add_point(Point(3, 5))
		self.__ps.add_point(Point(15, 25))
		self.__ps.add_point(Point(10, 40))
		self.__ps.add_point(Point(30, 28))
	
	def loop_invariant(self):
		return True
	
	def loop_event(self):
		self.window.fill(Colors.WHITE)
		self.__ps.draw(self.window)
		self.__ps.translate(10, 10)

if __name__ == "__main__":
	gconfig = GameConfig()
	gconfig.clock_rate = 10
	gconfig.window_size = [500, 500]
	rect = RandomDrawing(gconfig)
	gl = GameLoop(rect)
	gl.go()
