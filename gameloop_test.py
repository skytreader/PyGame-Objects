#! usr/bin/python2

from gameloop import GameLoopEvents
from gameloop import GameLoop
from gameloop import GameConfig
import gameloop
import pygame
import random

class GrayCircle(GameLoopEvents):
	
	def __init__(self):
		pygame_obj = pygame
		super(GrayCircle, self).__init__(pygame_obj)
		self.__pygame_object = pygame_obj
		self.__limit = 100
		self.__count = 0
	
	def loop_invariant(self):
		return self.__count < self.__limit
	
	def invoke_window(self, window_size):
		self.__window = self.__pygame_object.display.set_mode(window_size)
		return self.__window
	
	def loop_event(self):
		x = random.randint(0, 500)
		y = random.randint(0, 500)
		self.__pygame_object.draw.circle(self.__window, [218, 218, 218], [x, y], 50, 2)
		self.__count += 1

gc_object = GrayCircle()
gconfig = GameConfig()
gconfig.clock_rate = 10
gconfig.window_size = [500, 500]
gconfig.window_title = "Framework test"
game_loop = GameLoop(gc_object, gconfig)
game_loop.go()
