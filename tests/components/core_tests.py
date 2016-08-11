from components.core import GameConfig, GameModel, GameScreen, GameLoop, GameLoopEvents
from components.subscriber_pattern import Subscriber
from mock import patch

import unittest

class ConfigSubscriberMock(Subscriber):
    
    def __init__(self):
        super(ConfigSubscriberMock, self).__init__()
        self.notified = False

    def notify(self, observed, arg_bundle):
        has_config_key = arg_bundle.get("config_key") is not None
        has_old_val = arg_bundle.get("old_val") is not None
        has_new_val = arg_bundle.get("new_val") is not None
        self.notified = (
          isinstance(observed, GameConfig) and has_config_key and has_old_val
          and has_new_val
        )

class LoopEventsMock(GameLoopEvents):
    
    def __init__(self, config, screen):
        super(LoopEventsMock, self).__init__(config, screen)
        self.times_called = 0
    
    def loop_invariant(self):
        self.times_called += 1
        return self.times_called < 10

class GameConfigTest(unittest.TestCase):
    
    def setUp(self):
        self.game_config = GameConfig()
        self.watcher = ConfigSubscriberMock()
        self.game_config.subscribe(self.watcher)

    def test_window_size_setter(self):
        self.assertFalse(self.watcher.notified)
        self.game_config.set_config_val("window_size", (100, 100))
        self.assertTrue(self.watcher.notified)

    def test_clock_rate_setter(self):
        self.assertFalse(self.watcher.notified)
        self.game_config.set_config_val("clock_rate", 100)
        self.assertTrue(self.watcher.notified)

class DryRunTest(unittest.TestCase):

    @patch("components.core.pygame.time.Clock", autospec=True)
    @patch("components.core.pygame.init", autospec=True)
    def test_dry_run(self, pygame_init, clock):
        config = GameConfig()
        model = GameModel()
        screen = GameScreen(config.get_config_val("window_size"), model)
        loop_events = LoopEventsMock(config, screen)
        loop = GameLoop(loop_events)
        loop.go()
        self.assertTrue(pygame_init.called)
        self.assertTrue(clock.tick.called)
