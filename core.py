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

class Colors(object):
	"""
	A list of predefined colors.
	"""
	LUCID_DARK = (90, 73, 64)
	WHITE = (255, 255, 255)
	BLACK = (0, 0, 0)
	RED = (255, 0, 0)
	GREEN = (0, 255, 0)
	BLUE = (0, 0, 255)
	LIGHT_GRAY = (218, 218, 218)

class KeyCodes(object):
	"""
	A list of the key codes used in detecting key presses. Will add more as
	we go along. Will be deprecated when we find the PyGame equivalent.
	"""
	
	"""
	Up key
	"""
	UP_KEY = 273
	
	"""
	Down key
	"""
	DOWN_KEY = 274

class GameConfig(object):
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
		frame_rate = 12
	"""
	
	# Following constants for window_size
	WIDTH_INDEX = 0
	HEIGHT_INDEX = 1
	
	def __init__(self):
		self.clock_rate = 0
		self.window_size = [0, 0]
		self.window_title = ""

class GameLoop(object):
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
	
	def add_event_handler(self, event, handler_function):
		"""
		@param event
		  The event trigger. Get this from pygame.event.get() .
		@param handler_function
		  The function to be executed when event_code is trigerred. This
		  function will be triggered without any arguments passed.
		"""
		event_code = event.type
		self.__handlers[event_code] = handler_function
	
	def __handle_event(self, event_code):
		if event_code in self.__handlers:
			#TODO: Passing arguments?
			self.__handlers[event_code]()
	
	def attach_event_handlers(self):
		"""
		Write all calls to add_event_handler here. This method is called after
		GameLoopEvents.loop_setup but before the main loop starts rolling.
		
		(So far, this is the only event in GameLoop which you need to
		implement, and that's depending on your requirements.)
		"""
		pass
	
	def go(self):
		"""
		The main game loop.
		
		This already listens for the click of the close button of a window
		You can listen for other events by adding event handlers through
		add_event_handler .
		
		The initializations GameLoop performs by default are the following:
		  (1) Initialization of PyGame (pygame.init())
		  (2) Window invokation (GameLoopEvents.invoke_window()); background
		      color set-up and caption set-up
		  (3) PyGame clock (pygame.time.Clock())
		"""
		pygame.init()
		window = self.__loop_events.invoke_window(self.__window_size)
		window.fill(Colors.WHITE)
		pygame.display.set_caption(self.__window_title)
		clock = pygame.time.Clock()
		loop_control = True
		
		self.__loop_events.loop_setup()
		self.attach_event_handlers()
		
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
	
	def loop_setup(self):
		"""
		This code is executed after the GameLoop default set-up
		but before GameLoop enters the loop.
		"""
		pass
