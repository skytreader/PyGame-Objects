#! usr/bin/env python

from ..components.core import GameLoopEvents
from ..components.core import GameLoop
from ..components.core import GameConfig
import pygame
import random

"""
A simple demo of using the framework that randomly draws
gray circles on a white canvas.

Also demonstrates additional event handling.

@author Chad Estioco
"""

class GrayCircle(GameLoopEvents):
	
	def __init__(self, config):
		super(GrayCircle, self).__init__(config)
		self.__limit = 100
		self.__count = 0
	
	def loop_invariant(self):
		return self.__count < self.__limit
	
	def loop_event(self):
		x = random.randint(0, 500)
		y = random.randint(0, 500)
		pygame.draw.circle(self.window, [218, 218, 218], [x, y], 50, 2)
		self.__count += 1

class GrayCircleLoop(GameLoop):
	
	def __init__(self, events):
		super(GrayCircleLoop, self).__init__(events)
	
	def keydown(self, event):
		print "Keydown pressed!"
		print event.key
	
	def attach_event_handlers(self):
		self.add_event_handler(pygame.event.Event(pygame.KEYDOWN), self.keydown)

gconfig = GameConfig()
gconfig.clock_rate = 10
gconfig.window_size = [500, 500]
gconfig.window_title = "Framework test"
gc_object = GrayCircle(gconfig)
game_loop = GrayCircleLoop(gc_object)
game_loop.go()
