#! usr/bin/env python

from ...components.core import Colors
from ...components.core import GameConfig
from ...components.core import GameLoop
from ...components.core import GameLoopEvents
from ...components.core import GameScreen

from ...components.shapes import Point
from ...components.shapes import PointShape

import math

"""
Renders a scene full of fractal trees.

@author Chad Estioco
"""

class TreeScreen(GameScreen):
	
	def __init__(self, screen_size):
		super(GameScreen, self).__init__(screen_size)
		self.__line_stack = []
	
	@property
	def line_stack(self):
		return self.__line_stack
	
	def draw_screen(self, window):
		super(GameScreen, self).draw_screen(window)
		line_pointshape = self.line_stack.pop()
		line_pointshape.draw(window)

class TreeLoopEvents(GameLoopEvents):
	
	# The angle at which branches branch off, in radians
	BRANCH_ANGLE = 0.523598776
	
	def __init__(self, config, screen, initial_length):
		super(TreeLoopEvents, self).__init__(config, screen)
		self.__wood_length = initial_length
	
	@property
	def wood_length(self):
		return self.__wood_length
	
	@wood_length.setter
	def wood_length(self, l):
		self.__wood_length = l
	
	def loop_invariant(self):
		parent_invariant = super(TreeLoopEvents, self).loop_invariant()
		return len(self.game_screen.line_stack) and parent_invariant
	
	def loop_setup(self):
		center_x = self.config.window_size[GameConfig.WIDTH_INDEX] / 2
		bottom_y = self.config.window_size[GameConfig.WIDTH_INDEX]
		endpoint_y = bottom_y - self.wood_length
		line_pointshape = PointShape([Point(center_x, bottom_y), Point(center_x, endpoint_y)])
		self.game_screen.line_stack.push(line_pointshape)
	
	def loop_event(self):
		line_stack_length = len(self.game_screen.line_stack)
		current_line = self.game_screen.line_stack(line_stack_length - 1)
		
		super(TreeLoopEvents, self).loop_event()
		
		# Grow the new branches 1/3 and 2/3 of the way on the current branch
		# These define the starting points. y-coordinates first, then x
		point_list = current_line.point_list
		y_length = math.fabs(point_list[0].y - point_list[1].y + 1)
		y_branch1 = math.floor(0.33 * y_length)
		y_branch2 = math.floor(0.66 * y_length)
		
		x_length = math.fabs(point_list[0].x - point_list[1].x + 1)
		x_branch1 = math.floor(0.33 * x_length)
		x_branch2 = math.floor(0.66 * y_length)
		
		
