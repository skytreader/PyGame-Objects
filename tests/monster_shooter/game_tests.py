from components.core import GameConfig, GameLoop
from demo.monster_shooter_demo.monster_shooter_test import PVZMainScreen, PVZEvents
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
        config.set_config_val("window_size", [500, 500])
        config.set_config_val("clock_rate", 60)
        config.set_config_val("window_title", "PvZ Clone Demo")
        
        screen = PVZMainScreen(config)
        
        image_gle = PVZEvents(config, screen)
        gl = GameLoop(image_gle, is_test=True)
        gl.go()

        self.assertTrue(pygame_init.called)
        self.assertTrue(clock_tick.called)
        self.assertTrue(flip.called)
        self.assertTrue(quit.called)
