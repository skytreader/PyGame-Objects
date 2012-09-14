#! usr/bin/env python

from ...components.core import Colors
from ...components.core import GameConfig
from ...components.core import GameLoop
from ...components.core import GameLoopEvents
from ...components.core import GameScreen

from ...components.shapes import Point
from ...components.shapes import PointShape

import random

"""
Demonstrates new functionality of modifying a PointShape by
adding a point anywhere in the shape (no longer just at the
end).

Of course, the end result does not really look like a mutating
amoeba because we are just adding Points randomly; the resulting
vertices might intersect each other.

@author Chad Estioco
"""

class AmoebaScreen(GameScreen):
	
	def __init__(self, screen_size):
		super(AmoebaScreen, self).__init__(screen_size)
		#Assumming a 500x500 screen.
		self.__mutating_shape = PointShape([Point(250, 50), Point(50, 350), Point(400, 250)])
	
	@property
	def mutating_shape(self):
		return self.__mutating_shape
	
	def draw_screen(self, window):
		super(AmoebaScreen, self).draw_screen(window)
		self.mutating_shape.draw(window)

class AmoebaLoopEvents(GameLoopEvents):
	
	def __init__(self, config, game_screen):
		super(AmoebaLoopEvents, self).__init__(config, game_screen)
		self.__i = 0
		self.__limit = 200
	
	def loop_invariant(self):
		parent_invariant = super(AmoebaLoopEvents, self).loop_invariant()
		return self.__i < self.__limit and parent_invariant
	
	def loop_event(self):
		self.window.fill(Colors.WHITE)
		
		upper_bound = len(super(AmoebaLoopEvents, self).game_screen.mutating_shape.point_list) - 1
		insertion_point = random.randint(0, upper_bound)
		
		rand_x = random.randint(0, self.config.window_size[GameConfig.WIDTH_INDEX])
		rand_y = random.randint(0, self.config.window_size[GameConfig.HEIGHT_INDEX])
		
		super(AmoebaLoopEvents, self).game_screen.mutating_shape.add_point(Point(rand_x, rand_y), insertion_point)
		
		super(AmoebaLoopEvents, self).loop_event()
		
		self.__i += 1

gameconfig = GameConfig()
gameconfig.window_size = [500, 500]
gameconfig.clock_rate = 12
gameconfig.window_title = "Mutating Amoeba"

game_screen = AmoebaScreen(gameconfig.window_size)

loop_events = AmoebaLoopEvents(gameconfig, game_screen)
gameloop = GameLoop(loop_events)
gameloop.go()
