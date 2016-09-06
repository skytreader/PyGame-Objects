from __future__ import division

from framework_exceptions import InvalidConfigStateException
from subscriber_pattern import Publisher
from subscriber_pattern import Subscriber

import logging
import math
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

pygame.font.init()

class Colors(object):
    """
    A list of predefined colors.
    """
    MAX_WHITE = (255, 255, 255)
    MAX_BLACK = (0, 0, 0)
    MAX_RED = (255, 0, 0)
    MAX_GREEN = (0, 255, 0)
    MAX_BLUE = (0, 0, 255)

    LUCID_DARK = (90, 73, 64)
    HUMAN_GREEN = (61, 153, 112) # olive
    HUMAN_BLUE = (0, int("74", 16), int("d9", 16))
    HUMAN_RED = (255, int("41", 16), int("36", 16))
    LIGHT_GRAY = (218, 218, 218)

    YELLOW = (255, int("dc", 16), 0)
    GOLD = (230, 220, 50)

class GameConfig(Publisher):
    """
    Object to hold config values for games. Other components can subscribe to
    their GameConfig to adapt as the GameConfig changes value. They will be
    notified of the following in the arg_bundle:
        
        - config_key - of what changed.
        - old_val - of the config key.
        - new_val - of the config key.
    
    Defaults:
        clock_rate = 0
        window_size = (0, 0)
        window_title = ""
        debug_mode = False
    
    @author Chad Estioco
    """
    
    # Following constants for window_size
    WIDTH_INDEX = 0
    HEIGHT_INDEX = 1
    
    def __init__(self, clock_rate=0, window_size=None, window_title=None, debug_mode=False):
        super(GameConfig, self).__init__()
        self.__values = {}
        self.__values["window_size"] = window_size if window_size else (0, 0)
        self.__values["window_title"] = window_title if window_title else ""
        self.__values["clock_rate"] = clock_rate
        self.__values["debug_mode"] = debug_mode

    def set_config_val(self, config_key, val):
        arg_bundle = {}
        arg_bundle["config_key"] = config_key
        arg_bundle["old_val"] = self.__values[config_key]
        arg_bundle["new_val"] = val
        self.__values[config_key] = val
        self.notify_subscribers(**arg_bundle)

    def get_config_val(self, config_key):
        return self.__values.get(config_key)

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
        
        The initializations GameLoop performs by default are the following:
          (1) Initialization of PyGame (pygame.init())
          (2) Window invocation (GameLoopEvents.invoke_window()); background
              color set-up and caption set-up
        """
        pygame.init()
        clock = pygame.time.Clock()
        loop_control = True
        
        self.loop_events.loop_setup()
        
        while loop_control and self.__loop_events.loop_invariant():
            clock.tick(self.__loop_events.config.get_config_val("clock_rate"))
            for event in pygame.event.get():
                self.__handle_event(event)
            
            self.__loop_events.loop_event()
            pygame.display.flip()
        
        pygame.quit()

class GameScreen(Subscriber):
    """
    The view.
    
    A GameScreen must be PyGame executable by itself. Without a GameLoopEvents,
    it won't respond to any user-triggerred event.
    
    GameScreen classes should provide properties with which a GameLoopEvents can
    change what's happening on screen.
    
    @author Chad Estioco
    """

    DEBUG_SPACE_PROVISIONS = 300
    
    def __init__(self, game_config, model):
        """
        Creates an instance of GameScreen. DO NOT instantiate images/surfaces here.
        Put instantiation code in setup() method.
        
        @param screen_dimensions
          An iterable with at least two elements. See GameConfig.
        """
        screen_dimensions = game_config.get_config_val("window_size")
        self.config = game_config
        if game_config.get_config_val("debug_mode"):
            screen_dimensions = (screen_dimensions[0], screen_dimensions[1] + GameScreen.DEBUG_SPACE_PROVISIONS)

        self.__screen_dimensions = screen_dimensions
        self.model = model
        self.model.subscribe(self)
    
    @property
    def screen_size(self):
        return self.__screen_dimensions
    
    def setup(self):
        """
        Put all image/surface instantiation code here.
        """
        pass
    
    def draw_screen(self, window):
        """
        Insert all drawing logic here. Draw them on window.
        
        @param window
          A Surface instance to draw on.
        """
        pass

    def draw_unchanging(self, window):
        """
        Draw the unchanging aspects of your game screen, like the background.

        This method is only provided for the sake of code organization. There
        is nothing stopping you from drawing _everything_ in `draw_screen`.
        However, you may want to focus that method for the possibly-changing
        aspects of your display.
        """
        pass

class DebugQueue(Subscriber):
    """
    Handles on-screen display of logging.
    """

    DISPLAY_PADDING = 4
    LINE_DISTANCE = 2
    FONT_SIZE = 18
    FONT = pygame.font.Font(None, FONT_SIZE)
    LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
    
    def __init__(self, game_screen):
        self.q = []
        self.game_screen = game_screen
        self.game_screen.config.subscribe(self)
        self.fps_rate = self.game_screen.config.get_config_val("frame_rate")
        self.original_dims = self.game_screen.config.get_config_val("window_size")
        self.max_q_size = self.__get_max_log_display()

        log_formatter = logging.Formatter(DebugQueue.LOG_FORMAT)
        file_handler = logging.FileHandler("pygame-objects.log")
        file_handler.setFormatter(log_formatter)

        self.logger = logging.getLogger("pygame-objects-%s" % self.game_screen.config.get_config_val("window_title"))
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(file_handler)

    def log(self, log):
        if self.game_screen.config.get_config_val("debug_mode"):
            self.logger.info(log)
            if len(self.q) == self.max_q_size:
                self.q.pop(0)
            self.q.append(log)

    def __yposgen(self, x):
        return (DebugQueue.LINE_DISTANCE * (x - 1)) + (DebugQueue.FONT_SIZE * x) + self.original_dims[1] + DebugQueue.DISPLAY_PADDING

    def __get_max_log_display(self):
        """
        Get the maximum number of lines displayable.
        """
        constants = self.original_dims[1] + DebugQueue.DISPLAY_PADDING - DebugQueue.LINE_DISTANCE
        variabled = DebugQueue.LINE_DISTANCE + DebugQueue.FONT_SIZE
        available_space = self.original_dims[1] + GameScreen.DEBUG_SPACE_PROVISIONS
        return int(math.floor((available_space - constants) / variabled))
            
    def display_logs(self):
        if self.window and self.q:
            for idx, val in enumerate(self.q):
                mul = idx + 1
                log_render = DebugQueue.FONT.render(val, True, Colors.HUMAN_BLUE)
                self.window.blit(log_render, (DebugQueue.DISPLAY_PADDING, self.__yposgen(mul)))
    
class GameLoopEvents(Subscriber):
    """
    The controller.
    
    Encapsulates the stuff that happens inside a game loop.
    
    @author Chad Estioco
    """

    class KeyboardHandlerMapping(object):
        
        def __init__(self, keycode, handler):
            self.keycode = keycode
            self.handler = handler
    
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

        if config.get_config_val("debug_mode"):
            self.debug_queue = DebugQueue(game_screen)
        else:
            self.debug_queue = None
        
        self.__config.subscribe(self)
        self.__event_handlers = {}
        self.__key_handlers = {}
        
        self.__loop_control = True
        
        self.event_handlers[pygame.QUIT] = self.stop_loop
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
    
    def stop_loop(self, event):
        """
        You can override the default behavior of a game when responding to a
        pygame.QUIT event; like, for instance, if you want to ask the user
        if he really wants to quit. However, doing so may cause your game
        _not_ to quit at all! Use this method, in conjunction with
        GameLoopEvents.loop_invariant, to kill a game session.
        """
        self.__loop_control = False
    
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
          If event.type == pygame.KEYDOWN, this must be an instance of
          GameLoopEvents.KeyboardHandlerMapping.
          
          Otherwise, this is simply the function to be executed when
          event_code is trigerred. All handler functions must accept one
          argument, the event.
        """
        event_code = event.type
        
        if event_code == pygame.KEYDOWN:
            self.key_handlers[handler.keycode] = handler.handler
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
        
        The return value of this method is affected by the default behavior
        defined for event pygame.QUIT . It is recommended that direct subclasses
        of GameLoopEvents AND the return of this loop_invariant to their own
        loop invariants.
        """
        return self.__loop_control
    
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
        self.game_screen.draw_unchanging(self.window)
        self.game_screen.draw_screen(self.window)
        if self.debug_queue:
            self.debug_queue.display_logs()
    
    def configurable_setup(self):
        """
        Holds the set-up code affected by GameConfig.
        """
        pygame.display.set_caption(self.config.get_config_val("window_title"))
        window = self.invoke_window(self.game_screen.screen_size)
        window.fill(Colors.MAX_WHITE)

        if self.config.get_config_val("debug_mode"):
            self.debug_queue.window = window
    
    def notify(self, observed, arg_bundle = None):
        self.__configurable_setup()
    
    def loop_setup(self):
        """
        This code is executed after the GameLoop default set-up but before
        GameLoop enters the loop. It is important that extensions of
        GameLoopEvents call this method. This method already calls the setup()
        method of the GameScreen attribute.
        """
        self.configurable_setup()
        self.game_screen.setup()
        self.attach_event_handlers()

class GameModel(Publisher):
    
    def __init__(self):
        super(GameModel, self).__init__()
    
    def render(self, **kwargs):
        """
        Helps GameScreens represent and render relevant parts of this model.
        Return an object which your GameScreen knows how to render.
        """
        raise NotImplementedError("No rendering shall occur.")
