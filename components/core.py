#! usr/bin/env python

from subscriber_pattern import Observable
from subscriber_pattern import Observer

import pygame

"""
Classes in core encapsulate what happens in a game loop. It contains
the classes used to implement an MVC pattern.

Usage
  (1) Set the configuration of your game by creating a GameConfig
      instance.
  (2) Create a GameScreen instance.
  (3) Create a GameLoopEvents object by passing your GameConfig
      instance and GameScreen instance.
  (4) Create a GameLoop object by passing your GameLoopEvents object.
      Call go() .
  (5) Have fun!
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

class GameConfig(Observable):
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
	
	@author Chad Estioco
	"""
	
	# Following constants for window_size
	WIDTH_INDEX = 0
	HEIGHT_INDEX = 1
	
	def __init__(self):
		super(GameConfig, self).__init__()
		self.__clock_rate = 0
		self.__window_size = [0, 0]
		self.__window_title = ""
	
	@property
	def clock_rate(self):
		return self.__clock_rate
	
	@clock_rate.setter
	def clock_rate(self, rate):
		self.__clock_rate = rate
		self.notify_subscribers()
	
	@property
	def window_size(self):
		return self.__window_size
	
	@window_size.setter
	def window_size(self, ws):
		self.__window_size = ws
		self.notify_subscribers()
	
	@property
	def window_title(self):
		return self.__window_title
	
	@window_title.setter
	def window_title(self, title):
		self.__window_title = title
		self.notify_subscribers()

class GameLoop(object):
	"""
	A basic PyGame Game Loop.
	
	@author Chad Estioco
	"""
	
	def __init__(self, loop_events):
		"""
		Initializes a GameLoop.
		
		@param loop_events
		  An instance of GameLoopEvents.
		"""
		self.__loop_events = loop_events
		self.__game_configurations = loop_events.config
		
	@property
	def loop_events(self):
		return self.__loop_events
	
	@property
	def game_configurations(self):
		return self.__game_configurations
	
	def __handle_event(self, event):
		event_code = event.type
		if event_code in self.loop_events.event_handlers:
			#TODO: Passing arguments?
			self.loop_events.event_handlers[event_code](event)
	
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
		"""
		pygame.init()
		clock = pygame.time.Clock()
		loop_control = True
		
		self.loop_events.loop_setup()
		
		while loop_control and self.__loop_events.loop_invariant():
			clock.tick(self.__loop_events.config.clock_rate)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					loop_control = False
				else:
					self.__handle_event(event)
			
			self.__loop_events.loop_event()
			pygame.display.flip()
		
		pygame.quit()

class GameScreen(object):
	"""
	The view.
	
	A GameScreen must be PyGame executable by itself. Without a GameLoopEvents,
	it won't respond to any user-triggerred event.
	
	GameScreen classes should provide properties with which a GameLoopEvents can
	change what's happening on screen.
	
	@author Chad Estioco
	"""
	
	def __init__(self, screen_dimensions):
		"""
		Creates an instance of GameScreen. DO NOT instantiate images/surfaces here.
		Put instantiation code in setup() method.
		
		TODO: Take in a Model (for MVC).
		
		@param screen_dimensions
		  An iterable with at least two elements. See GameConfig.
		"""
		self.__screen_dimensions = screen_dimensions
		pass
	
	@property
	def screen_size(self):
		return self.__screen_dimensions
	
	def setup(self):
		"""
		Put all image/surface instatiation code here.
		"""
		pass
	
	def draw_screen(self, window):
		"""
		Insert all drawing logic here. Draw them on window.
		
		@param window
		  A Surface instance to draw on.
		"""
		pass
	
class GameLoopEvents(Observer):
	"""
	The controller.
	
	Encapsulates the stuff that happens inside a game loop.
	
	@author Chad Estioco
	"""
	
	# Constants used by the dictionary for key handlers
	KEYCODE = "keycode"
	HANDLER = "handler"
	
	def __init__(self, config, game_screen):
		"""
		Initializes a GameLoopEvents object. It is important that subclasses
		still initialize GameLoopEvents superclass for the properties config
		and game_screen.
		
		@param config
		  A GameConfig instance.
		@param game_screen
		  A GameScreen instance.
		"""
		self.__config = config
		self.__game_screen = game_screen
		
		self.__config.subscribe(self)
		self.__event_handlers = {}
		self.__key_handlers = {}
		
		self.event_handlers[pygame.KEYDOWN] = self.__handle_key
	
	@property
	def config(self):
		return self.__config
	
	@property
	def game_screen(self):
		return self.__game_screen
	
	@property
	def event_handlers(self):
		return self.__event_handlers
	
	@property
	def key_handlers(self):
		return self.__key_handlers
	
	def __handle_key(self, event):
		if event.key in self.key_handlers:
			self.key_handlers[event.key](event)
	
	def add_event_handler(self, event, handler):
		"""
		Maps a given event to the function handler. pygame.KEYDOWN events
		are handled slightly differently, though. See argument documentation
		below.
		
		@param event
		  The event trigger. Get this from pygame.event.get() .
		@param handler
		  If event.type == pygame.KEYDOWN, this must be a dictionary
		  containing at least two keys: GameLoopEvents.KEYCODE and GameLoopEvents.HANDLER.
		  GameLoopEvents.KEY should map to the key code of the button we wish
		  to catch while GameLoopEvents.HANDLER should map to the function we will
		  execute when the said key is triggered.
		  
		  Otherwise, this is simply the function to be executed when
		  event_code is trigerred. All handler functions must accept one
		  argument, the event.
		"""
		event_code = event.type
		
		if event_code == pygame.KEYDOWN:
			self.key_handlers[handler[GameLoopEvents.KEYCODE]] = handler[GameLoopEvents.HANDLER]
		else:
			self.event_handlers[event_code] = handler
	
	def attach_event_handlers(self):
		"""
		Write all calls to add_event_handler here. This method is called inside
		GameLoopEvents.loop_setup.
		"""
		pass
	
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
		Call this only after calling invoke_window
		"""
		return self.__window
	
	def loop_event(self):
		"""
		Holds the code that will be repeatedly executed.
		
		By default, this already draws the GameScreen object.
		"""
		self.game_screen.draw_screen(self.window)
	
	def configurable_setup(self):
		"""
		Holds the set-up code affected by GameConfig.
		"""
		pygame.display.set_caption(self.config.window_title)
		window = self.invoke_window(self.config.window_size)
		window.fill(Colors.WHITE)
	
	def notify(self, observed, arg_bundle = None):
		self.__configurable_setup()
	
	def loop_setup(self):
		"""
		This code is executed after the GameLoop default set-up but before
		GameLoop enters the loop. It is important that extensions of GameLoopEvents
		call this method. This method already calls the setup() method of the
		GameScreen attribute.
		"""
		self.configurable_setup()
		self.game_screen.setup()
		self.attach_event_handlers()
