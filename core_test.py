#! usr/bin/env python

from core import GameLoopEvents
from core import GameLoop
from core import GameConfig
import gameloop
import pygame
import random

"""
A simple demo of using the framework that randomly draws
gray circles on a white canvas.

Also demonstrates additional event handling.
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

def keydown():
	print "Keydown pressed!"

gconfig = GameConfig()
gconfig.clock_rate = 10
gconfig.window_size = [500, 500]
gconfig.window_title = "Framework test"
gc_object = GrayCircle(gconfig)
game_loop = GameLoop(gc_object)
game_loop.add_event_handler(pygame.KEYDOWN, keydown)
game_loop.go()
