#! usr/bin/env python

from ...components.common_shapes import Rectangle

from ...components.core import Colors
from ...components.core import GameConfig
from ...components.core import GameLoop
from ...components.core import GameLoopEvents
from ...components.core import GameScreen

from ...components.shapes import Point

class DisplayRectangle(GameScreen):	
	
	def __init__(self, screen_size):
		super(DisplayRectangle, self).__init__(screen_size)
		self.__rectangle = Rectangle(Point(10, 10), Point(40, 40), Colors.BLACK)
	
	@property
	def rectangle(self):
		return self.__rectangle
	
	def draw_screen(self, window):
		super(DisplayRectangle, self).draw_screen(window)
		self.rectangle.draw(window)

if __name__ == "__main__":
	config = GameConfig()
	config.clock_rate = 12
	config.window_size = [500, 500]
	config.window_title = "Rectangle Test"
	rscreen = DisplayRectangle(config.window_size)
	rloop_events = GameLoopEvents(config, rscreen)
	loop = GameLoop(rloop_events)
	loop.go()
