from components.common_ui import Button
from components.core import Colors, GameConfig, GameModel, GameScreen
from mock import patch

import pygame
import unittest

class ButtonTests(unittest.TestCase):

    @patch("components.common_ui.pygame.draw.rect", autospec=True)
    def test_draw(self, draw_rect):
        config = GameConfig(window_size=(400, 400))
        game_screen = GameScreen(config, GameModel())
        window = pygame.display.set_mode(config.get_config_val("window_size"))
        btn = Button("Test", Colors.NIGHT_BLUE, (100, 100))
        btn.draw(window, game_screen)
        self.assertTrue(draw_rect.called)
