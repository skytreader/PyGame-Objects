from test_subscriber_pattern import SubscriberMock
from components.core import GameConfig

import unittest

class GameConfigTest(unittest.TestCase):
    
    def setUp(self):
        self.game_config = GameConfig()
        self.watcher = SubscriberMock()
        self.game_config.subscribe(self.watcher)

    def test_window_size_setter(self):
        self.assertFalse(self.watcher.notified)
        self.game_config.window_size = (100, 100)
        self.assertTrue(self.watcher.notified)

    def test_clock_rate_setter(self):
        self.assertFalse(self.watcher.notified)
        self.game_config.clock_rate = 100
        self.assertTrue(self.watcher.notified)
