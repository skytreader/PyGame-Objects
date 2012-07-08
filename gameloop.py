#! usr/bin/python2

import pygame

"""
This encapsulates what happens in a game loop.

Usage
  (1) Configure your program by creating a GameConfig instance.
  (2) Extend GameLoopEvents. Note that you need to override _every_
      method of that class.
  (3) Create a GameLoop object by passing a GameConfig instance and
      an instance of your GameLoopEvents object. Call go() .
  (4) Have fun!
"""

class Colors:
	"""
	A list of predefined colors.
	"""
	LUCID_DARK = [90, 73, 64]
	WHITE = [255, 255, 255]
	BLACK = [0, 0, 0]
	RED = [255, 0, 0]
	GREEN = [0, 255, 0]
	BLUE = [0, 0, 255]
	LIGHT_GRAY = [218, 218, 218]

class GameConfig:
	"""
	Encapsulation of various configurations needed by a GameLoop object.
	
	All conifgurations are stored as public class attributes so you can
	change them when and as you please.
	
	Right now, it only supports three configurations, clock rate, window
	size, and window title. I might add more as I go along.
	
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
		"""
		The main game loop.
		
		This already listens for the click of the close button of
		a window.
		"""
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
	Encapsulates the stuff that happens inside a game loop. Override
	_every_ method in this class.
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
