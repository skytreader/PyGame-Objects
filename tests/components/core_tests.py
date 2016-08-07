from components.core import GameConfig
from components.subscriber_pattern import Subscriber

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
