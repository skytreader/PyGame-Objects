#! usr/bin/env python

import pygame

"""
Classes in core encapsulate what happens in a game loop.

Usage
  (1) Configure your program by creating a GameConfig instance.
  (2) Extend GameLoopEvents. Note what methods you need to override
      from that class.
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
	
	def __init__(self, loop_events):
		self.__loop_events = loop_events
		game_configurations = loop_events.config
		self.__clock_rate = game_configurations.clock_rate
		self.__window_size = game_configurations.window_size
		self.__window_title = game_configurations.window_title
		self.__handlers = {}
	
	def add_event_handler(self, event_code, handler_function):
		"""
		@param event_code
		  A PyGame event code (typically ints). These come from pygame.event.get()
		@param handler_function
		  The function to be executed when event_code is trigerred. This
		  function will be triggered without any arguments passed.
		"""
		self.__handlers[event_code] = handler_function
	
	def __handle_event(self, event_code):
		if event_code in self.__handlers:
			#TODO: Passing arguments?
			self.__handlers[event_code]()
	
	def go(self):
		"""
		The main game loop.
		
		This already listens for the click of the close button of a window
		You can listen for other events by adding event handlers through
		add_event_handler .
		"""
		pygame.init()
		window = self.__loop_events.invoke_window(self.__window_size)
		window.fill(Colors.WHITE)
		pygame.display.set_caption(self.__window_title)
		clock = pygame.time.Clock()
		loop_control = True
		
		while loop_control and self.__loop_events.loop_invariant():
			clock.tick(self.__clock_rate)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					loop_control = False
				else:
					self.__handle_event(event.type)
			
			self.__loop_events.loop_event()
			pygame.display.flip()
		
		pygame.quit()
	
class GameLoopEvents(object):
	"""
	Encapsulates the stuff that happens inside a game loop.
	"""
	
	def __init__(self, config):
		self.__config = config
	
	@property
	def config(self):
		return self.__config
	
	def loop_invariant(self):
		"""
		Condition to check that keeps the game loop going.
		
		By default this returns True.
		"""
		return True
	
	def invoke_window(self, window_size):
		"""
		Create a PyGame window and return it so that the GameLoop
		can access it too.
		
		The basic code for creating and returning a window is already
		written. Override this only when you need extra set-up. Extensions
		of this class can access the created window via the accessor, window.
		"""
		self.__window = pygame.display.set_mode(window_size)
		return self.__window
	
	@property
	def window(self):
		"""
		RED ALERT! Call this only after calling invoke_window
		"""
		return self.__window
	
	def loop_event(self):
		"""
		Holds the code that will be repeatedly executed.
		"""
		pass
