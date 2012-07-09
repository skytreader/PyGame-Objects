#! usr/bin/python2

from core import GameLoopEvents
from core import GameConfig
from core import GameLoop

import pygame

class RectangleShape(GameLoopEvents):
	
	def __init__(self):
		super(RectangleShape, self).__init__()
	
	def loop_invariant(self):
		return True
