#! usr/bin/python2

from gameloop import GameLoopEvents
from gameloop import GameConfig
from gameloop import GameLoop

import pygame

class RectangleShape(GameLoopEvents):
	
	def __init__(self):
		super(RectangleShape, self).__init__()
	
	def loop_invariant(self):
		return True
