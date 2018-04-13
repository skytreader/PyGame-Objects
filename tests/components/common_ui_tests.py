from components.common_ui import Button, UnsupportedEventException
from components.core import Colors, GameConfig, GameLoop, GameLoopEvents, GameModel, GameScreen
from mock import patch
from tests.components.core_tests import EventHandlerMock

import pygame
import unittest

class SampleGameScreenUI(GameScreen):

    def setup(self):
        self.btn = Button("test", Colors.MAX_BLACK, (0, 0))
        self.evh = EventHandlerMock()
        self.btn.set_event_handler(
            pygame.event.Event(pygame.MOUSEBUTTONDOWN), self.evh.handle_event
        )
        self.ui_elements.add(self.btn)

class ButtonTests(unittest.TestCase):

    @patch("components.common_ui.pygame.draw.rect", autospec=True)
    def test_draw(self, draw_rect):
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

    def test_default_event_handling(self):
        screen = SampleGameScreenUI(GameConfig(), GameModel())
        loop_events = GameLoopEvents(screen)
        loop_events.loop_setup()
        loop = GameLoop(loop_events)
        # Python sorcery!
        loop._GameLoop__handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN))
        self.assertTrue(screen.evh.is_called)

    def test_unsupported_event(self):
        btn = Button("test", Colors.NIGHT_BLUE, (100, 88))
        self.assertRaises(
            UnsupportedEventException,
            btn.set_event_handler, pygame.event.Event(pygame.KEYUP),
            btn.dummy_event_handler
        )
