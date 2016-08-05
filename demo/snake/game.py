from components.core import Colors, GameConfig, GameLoop, GameLoopEvents, GameScreen
from components.helpers.grid import QuadraticGrid
from model import SnakeGameModel

import math
import pygame

class SnakeScreen(GameScreen):
    
    def __init__(self, screen_size, grid_size):
        super(SnakeScreen, self).__init__(screen_size, SnakeGameModel(grid_size[0], grid_size[1]))
        self.game_model = self.model
        self.game_model.initialize()

        self.block_width = int(math.floor(screen_size[0] / grid_size[0]))
        self.block_height = int(math.floor(screen_size[1] / grid_size[1]))

    def draw_screen(self, window):
        snake_squares = self.game_model.snake.enumerate_snake_squares()
        snake_squares = QuadraticGrid.make_rects(snake_squares, self.block_width, self.block_height)

        for snake_pos in snake_squares:
            pygame.draw.rect(window, Colors.BLACK, snake_pos, 0) 

class SnakeGameEvents(GameLoopEvents):
    
    def __init__(self, screen, config):
        super(SnakeGameEvents, self).__init__(screen, config)

    def loop_event(self):
        self.window.fill(Colors.WHITE)
        super(SnakeGameEvents, self).loop_event()

if __name__ == "__main__":
    config = GameConfig()
    config.set_config_val("clock_rate", 60)
    config.set_config_val("window_size", (600, 600))
    config.set_config_val("window_title", "SNAKE!")

    screen = SnakeScreen(config.get_config_val("window_size"), (10, 10))
    loop_events = SnakeGameEvents(config, screen)
    loop = GameLoop(loop_events)
    loop.go()
