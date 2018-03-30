from components.common_ui import Button
from components.core import Colors, GameConfig, GameModel, GameScreen
from mock import patch

import pygame
import unittest

class ButtonTests(unittest.TestCase):

    @patch("components.common_ui.pygame.draw.rect", autospec=True)
    def test_draw(self, draw_rect):
        print "we are in test_draw"
        config = GameConfig(window_size=(400, 400))
        game_screen = GameScreen(config, GameModel())
        window = pygame.display.set_mode(config.get_config_val("window_size"))
        btn = Button("Test", Colors.NIGHT_BLUE, (100, 88))
        btn.draw(window, game_screen)
        draw_rect.assert_any_call(
            window, btn.color, (
                btn.position[1], btn.position[0], btn.max_size[0],
                btn.max_size[1]
            )
        )
