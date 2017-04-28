from components.core import GameConfig, GameLoop
from demo.snake.game import SnakeScreen, SnakeGameEvents
from mock import patch
from tests import make_mock_clock

import unittest

class GameTests(unittest.TestCase):
    from components import core

    @patch("components.core.pygame.quit", autospec=True)
    @patch("components.core.pygame.display.flip", autospec=True)
    @patch("components.core.pygame.time.Clock", new_callable=make_mock_clock)
    @patch("components.core.pygame.init", autospec=True)
    def test_dry_run(self, pygame_init, clock_tick, flip, quit):
        config = GameConfig()
        config.set_config_val("clock_rate", 60)
        config.set_config_val("window_size", (600, 600))
        config.set_config_val("window_title", "SNAKE!")
        config.set_config_val("debug_mode", True)
        config.set_config_val("log_to_terminal", True)
        config.set_config_val("difficulty", 1)
        screen = SnakeScreen(config, (10, 10))
        loop_events = SnakeGameEvents(config, screen)
        loop = GameLoop(loop_events)
        loop.go()

        self.assertTrue(pygame_init.called)
        self.assertTrue(clock_tick.called)
        self.assertTrue(flip.called)
        self.assertTrue(quit.called)
