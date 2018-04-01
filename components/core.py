from __future__ import division

from config import JsonConfigParser
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
    DIM_GRAY = (108, 108, 108)
    EBONY = (83, 93, 80)

    LUCID_DARK = (90, 73, 64)
    HUMAN_GREEN = (61, 153, 112) # olive
    HUMAN_BLUE = (0, int("74", 16), int("d9", 16))
    HUMAN_RED = (255, int("41", 16), int("36", 16))
    LIGHT_GRAY = (218, 218, 218)

    ADVENTURE_DARK = (4, 3, 3)
    ADVENTURE_RED = (203, 27, 23)
    ADVENTURE_GREEN = (88, 187, 30)
    ADVENTURE_BLUE = (15, 98, 209)

    NIGHT_DARK = (8, 2, 0)
    NIGHT_RED = (228, 68, 41)
    NIGHT_GREEN = (0, 174, 101)
    NIGHT_BLUE = (0, 176, 233)
    NIGHT_YELLOW = (254, 237, 0)
    NIGHT_GRAY = (180, 177, 177)

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

    The defaults are listed [in the wiki](https://github.com/skytreader/PyGame-Objects/wiki/Framework-Walkthrough#gameconfig).
    
    @author Chad Estioco
    """
    
    # Following constants for window_size
    WIDTH_INDEX = 0
    HEIGHT_INDEX = 1
    
    def __init__(self, clock_rate=0, window_size=None, window_title=None,
      debug_mode=False, log_to_terminal=False):
        super(GameConfig, self).__init__()
        self.__values = {}
        self.__values["window_size"] = window_size if window_size else (0, 0)
        self.__values["window_title"] = window_title if window_title else ""
        self.__values["clock_rate"] = clock_rate
        self.__values["debug_mode"] = debug_mode
        self.__values["log_to_terminal"] = log_to_terminal

    def set_config_val(self, config_key, val):
        arg_bundle = {}
        arg_bundle["config_key"] = config_key
        arg_bundle["old_val"] = self.__values.get(config_key)
        arg_bundle["new_val"] = val
        self.__values[config_key] = val
        self.notify_subscribers(**arg_bundle)

    def get_config_val(self, config_key):
        return self.__values.get(config_key)

    def load_from_file(self, f):
        """
        This will only overwrite the config values present in the file. So if
        the current config object has the key value "spam" but the file does not,
        after invoking this method, the key "spam" should still have its original
        value.
        """
        json_parser = JsonConfigParser()
        json_parser.parse_config(f)
        for config in json_parser.config_vals.keys():
            self.set_config_val(config, json_parser.config_vals[config])

class GameLoop(object):
    """
    A basic PyGame Game Loop.
    
    @author Chad Estioco
    """
    
    def __init__(self, loop_events, is_test=False):
        """
        Initializes a GameLoop.
        
        @param loop_events
          An instance of GameLoopEvents.
        """
        self.loop_events = loop_events
        self.game_configurations = loop_events.config
        self.__is_test = is_test
    
    def __handle_event(self, event):
        event_code = event.type
        if event_code in self.loop_events.event_handlers:
            #TODO: Passing arguments?
            for evh in self.loop_events.event_handlers[event_code]:
                evh(event)
    
    def go(self):
        """
        The main game loop.
        
        The initializations GameLoop performs by default are the following:
          (1) Initialization of PyGame (pygame.init())
          (2) Window invocation (GameLoopEvents.invoke_window()); background
              color set-up and caption set-up
        """
        try:
            print "pygame init"
            pygame.init()
            pygame.font.init()
            clock = pygame.time.Clock()
            
            self.loop_events.loop_setup()
            i = 0
            
            while self.loop_events.loop_invariant():
                clock.tick(self.loop_events.config.get_config_val("clock_rate"))
                for event in pygame.event.get():
                    self.__handle_event(event)
                
                self.loop_events.loop_event()
                pygame.display.flip()

                if self.__is_test:
                    i += 1
                    if i > 4: # FIXME: Magic number!
                        break
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            import traceback
            traceback.print_exc()
        finally:
            pygame.quit()
            pygame.font.quit()

class GameScreen(Subscriber):
    """
    The view. GameScreen contains the information needed to render the game's
    current scene.
    
    A GameScreen must be PyGame executable by itself. Without a GameLoopEvents,
    it won't respond to any user-triggerred event.
    
    GameScreen classes should provide properties with which a GameLoopEvents can
    change what's happening on screen.
    """

    DEBUG_SPACE_PROVISIONS = 300
    
    def __init__(self, game_config, model):
        """
        Creates an instance of GameScreen. DO NOT instantiate images/surfaces here.
        Put instantiation code in setup() method.
        """
        screen_dimensions = game_config.get_config_val("window_size")
        self.config = game_config
        if game_config.get_config_val("debug_mode"):
            screen_dimensions = (screen_dimensions[0], screen_dimensions[1] + GameScreen.DEBUG_SPACE_PROVISIONS)

        self.screen_dimensions = screen_dimensions
        self.model = model
        self.model.subscribe(self)
        self.ui_elements = set()
    
    @property
    def screen_size(self):
        """
        This property is provided merely for the sake of backwards compatibility.
        New code should refer straight to the `screen_dimensions` field.
        """
        return self.screen_dimensions

    # TODO Is this appropriate for a decorator?
    def _is_drawable_clicked(self, drawable, pos):
        width_limit = drawable.draw_offset[1] + drawable.max_size[0]
        height_limit = drawable.draw_offset[0] + drawable.max_size[1]
        in_width = drawable.draw_offset[1] <= pos[0] <= width_limit
        in_height = drawable.draw_offset[0] <= pos[1] <= height_limit

        return in_width and in_height
    
    def setup(self):
        """
        Put all image/surface/Drawable instantiation code here.
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

    class LogLine(object):
        
        def __init__(self, log, level):
            self.log = log
            self.level = level

    DISPLAY_PADDING = 4
    LINE_DISTANCE = 2
    FONT_SIZE = 18
    # TODO Handle case where font is not available.
    try:
        FONT = pygame.font.Font("/usr/local/pygame-fonts/Inconsolata-Regular.ttf", FONT_SIZE)
    except IOError:
        FONT = pygame.font.Font(None, FONT_SIZE)
    LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"

    LOG_COLORS = {
        logging.CRITICAL: Colors.MAX_RED,
        logging.ERROR: Colors.NIGHT_RED,
        logging.WARNING: Colors.GOLD,
        logging.INFO: Colors.HUMAN_BLUE,
        logging.DEBUG: Colors.HUMAN_BLUE
    }
    
    def __init__(self, game_screen):
        self.q = []
        self.game_screen = game_screen
        self.game_screen.config.subscribe(self)
        self.fps_rate = self.game_screen.config.get_config_val("frame_rate")
        self.original_dims = self.game_screen.config.get_config_val("window_size")
        self.max_q_size = self.__get_max_log_display()

        # This will be properly set in GameLoopEvents.configurable_setup
        self.window = None

        log_formatter = logging.Formatter(DebugQueue.LOG_FORMAT)
        if self.game_screen.config.get_config_val("log_to_terminal"):
            logging.basicConfig(format=DebugQueue.LOG_FORMAT)

        file_handler = logging.FileHandler("pygame-objects.log")
        file_handler.setFormatter(log_formatter)

        self.logger = logging.getLogger("pygame-objects-%s" % self.game_screen.config.get_config_val("window_title"))
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(file_handler)

    def log(self, log, level=logging.INFO):
        if self.game_screen.config.get_config_val("debug_mode"):
            self.logger.log(level, log)
            if len(self.q) == self.max_q_size:
                self.q.pop(0)
            self.q.append(DebugQueue.LogLine(log, level))

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
                color = DebugQueue.LOG_COLORS[val.level]
                log_render = DebugQueue.FONT.render(val.log, True, color)
                self.window.blit(log_render, (DebugQueue.DISPLAY_PADDING, self.__yposgen(mul)))
    
class GameLoopEvents(Subscriber):
    """
    The controller.
    
    Encapsulates the stuff that happens inside a game loop.
    """

    class KeyControls(object):
        """
        Defines the whole keyboard control scheme for your game. The advantage
        of this is that you can have multiple control schemes (e.g., the
        superior WASD vs arrow keys for movement) which can be swapped
        programmatically/at runtime.
        """
        
        def __init__(self):
            self.controls = {}

        def register_key(self, keycode, handler):
            self.controls[keycode] = handler

        def handle(self, event):
            handler = self.controls.get(event.key)
            if handler:
                handler(event)
    
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

        self.debug_queue = DebugQueue(game_screen)
        
        self.__config.subscribe(self)
        self.__event_handlers = {}
        self.__key_handlers = {}
        
        self.__loop_control = True
        
        # TODO Maybe use add_event_handler for this to prevent future fuck-ups?
        self.event_handlers[pygame.QUIT] = [self.stop_main]
    
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
    
    def stop_main(self, event):
        """
        This is supposed to kill the _whole_ app.
        """
        self.__loop_control = False
    
    def add_event_handler(self, event, handler):
        """
        Maps a given event to the function handler. pygame.KEYDOWN events
        are handled slightly differently, though. See argument documentation
        below.
        
        @param event
          The event trigger. Get this from pygame.event.get() .
        @param handler
          If event.type == pygame.KEYDOWN, this must be the `handle` method of
          an instance of GameLoopEvents.KeyControls.
          
          Otherwise, this is simply the function to be executed when
          event_code is trigerred. All handler functions must accept one
          argument, the event.
        """
        event_code = event.type
        existing_handler = self.event_handlers.get(event_code)

        if existing_handler:
            self.event_handlers[event_code].append(handler)
        else:
            self.event_handlers[event_code] = [handler]

    
    def attach_event_handlers(self):
        """
        Write all calls to add_event_handler here. This method is called inside
        GameLoopEvents.loop_setup.
        """
        for common_ui in self.game_screen.ui_elements:
            for ev_code, ev_handler in common_ui._event_handlers.iteritems():
                self.add_event_handler(pygame.event.Event(ev_code), ev_handler)
    
    def loop_invariant(self):
        """
        Condition to check that keeps the game loop going.
        
        The return value of this method is affected by the default behavior
        defined for event pygame.QUIT . It is recommended that direct subclasses
        of GameLoopEvents `AND` the return of this loop_invariant to their own
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

        TODO Why should this still be a property?
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
        window = self.invoke_window(self.game_screen.screen_dimensions)
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
        self.endgame = False
    
    def render(self, **kwargs):
        """
        Helps GameScreens represent and render relevant parts of this model.
        Return an object which your GameScreen knows how to render.
        """
        pass
