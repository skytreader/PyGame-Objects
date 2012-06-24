#! usr/bin/python2

import pygame

WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
LIGHT_GRAY = [218, 218, 218]

class GameConfig:
	"""
	Encapsulation of various configurations needed by a
	GameLoop object
	
	Defaults:
		clock_rate = 0
		window_size = [0, 0]
		window_title = ""
	"""
	
	def __init__(self):
		self.clock_rate = 0
		self.window_size = [0, 0]
		self.window_title = ""

class GameLoop:
	"""
	A basic PyGame Game Loop
	"""
	
	def __init__(self, loop_events, game_configurations):
		self.__loop_events = loop_events
		self.__clock_rate = game_configurations.clock_rate
		self.__window_size = game_configurations.window_size
		self.__window_title = game_configurations.window_title
	
	def go(self):
		pygame.init()
		window = self.__loop_events.invoke_window(self.__window_size)
		window.fill(WHITE)
		pygame.display.set_caption(self.__window_title)
		clock = pygame.time.Clock()
		loop_control = True
		
		while loop_control and self.__loop_events.loop_invariant():
			clock.tick(self.__clock_rate)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					loop_control = False
			
			self.__loop_events.loop_event()
			pygame.display.flip()
		
		pygame.quit()
	
class GameLoopEvents(object):
	"""
	Encapsulates the stuff that happens inside a game loop.
	"""
	
	def __init__(self):
		pass
	
	def loop_invariant(self):
		"""
		Condition to check that keeps the game loop going.
		"""
		pass
	
	def invoke_window(self, window_size):
		"""
		Create a PyGame window and return it so that the GameLoop
		can access it too.
		"""
		pass
	
	def loop_event(self):
		"""
		Holds the code that will be repeatedly executed.
		"""
		pass
