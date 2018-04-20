from components.core import DebugQueue, GameConfig, GameModel, GameScreen, GameLoop, GameLoopEvents
from components.drawable import Drawable
from components.subscriber_pattern import Subscriber
from mock import patch
from StringIO import StringIO
from tests import make_mock_clock

import json
import pygame
import unittest

# These are classes used by the tests, not actual tests themselves.

class ConfigSubscriberMock(Subscriber):
    
    def __init__(self):
        super(ConfigSubscriberMock, self).__init__()
        self.notified = False

    def notify(self, observed, arg_bundle):
        has_config_key = arg_bundle.get("config_key") is not None
        has_old_val = arg_bundle["old_val"]
        has_new_val = arg_bundle.get("new_val") is not None
        self.notified = (
          isinstance(observed, GameConfig) and has_config_key and has_new_val
        )

class LoopEventsMock(GameLoopEvents):
    
    def __init__(self, screen):
        super(LoopEventsMock, self).__init__(screen)
        self.times_called = 0
    
    def loop_invariant(self):
        self.times_called += 1
        return self.times_called < 10

class KeyboardHandlingLoopEventsMock(GameLoopEvents):
    """
    Technically this could be merged with LoopEventsMock above but it seemed
    prudent to abide by the single responsibility principle and create a new
    mock subclass for each scenario we want to test. That way, the parts that
    are mocked out do not run into each other.
    """

    def __init__(self, screen):
        super(KeyboardHandlingLoopEventsMock, self).__init__(screen)
        self.key_controls = GameLoopEvents.KeyControls()

    def attach_event_handlers(self):
        super(KeyboardHandlingLoopEventsMock, self).attach_event_handlers()

        keydown_event = pygame.event.Event(pygame.KEYDOWN)
        self.add_event_handler(keydown_event, self.key_controls.handle)

class EventHandlerMock(object):

    def __init__(self):
        self.is_called = False

    def handle_event(self, event):
        self.is_called = True

# Actual tests start below.

class GameConfigTest(unittest.TestCase):
    
    def setUp(self):
        self.game_config = GameConfig()
        self.watcher = ConfigSubscriberMock()
        self.game_config.subscribe(self.watcher)
        self.titled_config = GameConfig(window_title="Your Majesty")

    def test_window_size_setter(self):
        self.assertFalse(self.watcher.notified)
        self.game_config.set_config_val("window_size", (100, 100))
        self.assertTrue(self.watcher.notified)

    def test_clock_rate_setter(self):
        self.assertFalse(self.watcher.notified)
        self.game_config.set_config_val("clock_rate", 100)
        self.assertTrue(self.watcher.notified)

    def test_custom_key_setter(self):
        self.assertFalse(self.watcher.notified)
        self.game_config.set_config_val("quick brown foxkcd", 1)
        self.assertTrue(self.watcher.notified)

    def test_load_from_file_expected(self):
        expected_json_newbies = """{
    "song": "Lost Stars",
    "artist": "Adam Levine",
    "player": "Spotify"
}"""
        preload_title = self.titled_config.get_config_val("window_title")
        self.assertTrue(preload_title is not None)
        self.titled_config.load_from_file(StringIO(expected_json_newbies))
        postload_title = self.titled_config.get_config_val("window_title")
        self.assertEqual(preload_title, postload_title)

        json_confs = json.loads(expected_json_newbies)
        
        for key in json_confs.keys():
            self.assertEqual(self.titled_config.get_config_val(key), json_confs[key])
    
    def test_load_from_file_unwanted(self):
        unwanted_json = """[
    {"song": "Lost Stars"},
    {"artist": "Adam Levine"},
    {"player": "Spotify"}
]"""
        preload_title = self.titled_config.get_config_val("window_title")
        self.assertTrue(preload_title is not None)

        with self.assertRaises(AttributeError):
            self.titled_config.load_from_file(StringIO(unwanted_json))

        postload_title = self.titled_config.get_config_val("window_title")
        self.assertEquals(preload_title, postload_title)
    
    def test_load_from_file_replacing(self):
        replacing_json = '{"window_title": "Your Royal Highness"}'
        preload_title = self.titled_config.get_config_val("window_title")
        self.assertTrue(preload_title is not None)
        self.titled_config.load_from_file(StringIO(replacing_json))
        postload_title = self.titled_config.get_config_val("window_title")
        self.assertEqual(postload_title, "Your Royal Highness")
        self.assertNotEqual(preload_title, postload_title)

class GameScreenTest(unittest.TestCase):
    
    def test_debug_provisions(self):
        config_debug = GameConfig(debug_mode=True)
        screen_debug = GameScreen(config_debug, GameModel())
        window_size_debug = config_debug.get_config_val("window_size")
        self.assertEqual(
            (window_size_debug[0], window_size_debug[1] + GameScreen.DEBUG_SPACE_PROVISIONS),
            screen_debug.screen_size
        )

    def test_is_drawable_clicked_happy(self):
        sample_drawable = Drawable((0, 0), 100, 88)
        cfg = GameConfig(window_size=(200, 160))
        screen = GameScreen(cfg, GameModel())
        self.assertTrue(screen._is_drawable_clicked(sample_drawable, (90, 44)))

class DebugQueueTest(unittest.TestCase):
    
    def test_log_q_growth(self):
        config = GameConfig(debug_mode=True)
        screen = GameScreen(config, GameModel())
        debug_q = DebugQueue(screen)
        # Python sorcery!
        max_display = debug_q._DebugQueue__get_max_log_display()

        for i in range(max_display):
            self.assertTrue(len(debug_q.q) == i)
            debug_q.log("log %s" % i)

        self.assertTrue(len(debug_q.q) == max_display)
        debug_q.log("more")
        self.assertTrue(len(debug_q.q) == max_display)
        self.assertTrue(debug_q.q[0].log == "log 1")

class EventHandlerTests(unittest.TestCase):

    def setUp(self):
        self.btn_down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN)
        self.press_up_key_event = pygame.event.Event(
            pygame.KEYDOWN, key=pygame.K_UP
        )

    def test_event_handling_basic(self):
        """
        Test basic event handling of non-keyboard-based events.
        """
        screen = GameScreen(GameConfig(), GameModel())
        loop_events = GameLoopEvents(screen)
        evh1 = EventHandlerMock()
        loop_events.add_event_handler(self.btn_down_event, evh1.handle_event)
        loop = GameLoop(loop_events)
        # More Python sorcery!
        loop._GameLoop__handle_event(self.btn_down_event)
        self.assertTrue(evh1.is_called)

    def test_event_handling_kbd_basic(self):
        """
        Test basic event handling of keyboard-based events.
        """
        screen = GameScreen(GameConfig(), GameModel())
        loop_events = KeyboardHandlingLoopEventsMock(screen)
        evh1 = EventHandlerMock()
        loop_events.key_controls.register_key(pygame.K_UP, evh1.handle_event)
        loop_events.attach_event_handlers()
        loop = GameLoop(loop_events)
        # More Python sorcery!
        loop._GameLoop__handle_event(self.press_up_key_event)
        self.assertTrue(evh1.is_called)

    def test_event_handling_multiple(self):
       """
       Test that multiple event handlers can listen on the same non-keyboard-based
       event.
       """
       screen = GameScreen(GameConfig(), GameModel())
       loop_events = GameLoopEvents(screen)
       evh1 = EventHandlerMock()
       evh2 = EventHandlerMock()
       loop_events.add_event_handler(self.btn_down_event, evh1.handle_event)
       loop_events.add_event_handler(self.btn_down_event, evh2.handle_event)
       loop = GameLoop(loop_events)
       # More Python sorcery!
       loop._GameLoop__handle_event(self.btn_down_event)
       self.assertTrue(evh1.is_called)
       self.assertTrue(evh2.is_called)

class DryRunTest(unittest.TestCase):

    @patch("components.core.pygame.quit", autospec=True)
    @patch("components.core.pygame.display.flip", autospec=True)
    @patch("components.core.pygame.time.Clock", new_callable=make_mock_clock)
    @patch("components.core.pygame.init", autospec=True)
    def test_dry_run(self, pygame_init, clock_tick, flip, quit):
        config = GameConfig()
        model = GameModel()
        screen = GameScreen(config, model)
        loop_events = LoopEventsMock(screen)
        loop = GameLoop(loop_events)
        loop.go()

        self.assertTrue(pygame_init.called)
        self.assertTrue(clock_tick.called)
        self.assertTrue(flip.called)
        self.assertTrue(quit.called)
