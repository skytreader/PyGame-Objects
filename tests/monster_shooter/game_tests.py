from components.core import GameConfig, GameLoop
from demo.monster_shooter_demo.monster_shooter_test import PVZMainScreen, PVZEvents, PVZLoop
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
