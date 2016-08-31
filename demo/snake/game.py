from components.core import Colors, GameConfig, GameLoop, GameLoopEvents, GameScreen
from components.helpers.grid import QuadraticGrid
from model import SnakeGameModel

import math
import pygame

class SnakeScreen(GameScreen):
    
    def __init__(self, config, grid_size):
        super(SnakeScreen, self).__init__(config, SnakeGameModel(grid_size[0], grid_size[1]))
        screen_size = config.get_config_val("window_size")
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
    
    PYGAME_TO_MOVE = {
      pygame.K_UP: 'u', pygame.K_DOWN: 'd', pygame.K_RIGHT: 'r',
      pygame.K_LEFT: 'l' 
    }
    
    def __init__(self, screen, config):
        super(SnakeGameEvents, self).__init__(screen, config)

    def loop_event(self):
        self.window.fill(Colors.WHITE)
        super(SnakeGameEvents, self).loop_event()

    def __create_move_event_handler(self, key):
        def event_handler(event):
            height = self.game_screen.game_model.height
            movement = SnakeGameEvents.PYGAME_TO_MOVE[key]
            self.debug_queue.log(movement)
            self.debug_queue.log("grid height is %s" % height)
            self.game_screen.model.move_snake(movement)
            self.debug_queue.log("snake head now at %s" % str(self.game_screen.model.snake.head))
        
        return event_handler

    def attach_event_handlers(self):
        keydown_event = pygame.event.Event(pygame.KEYDOWN)
        self.add_event_handler(keydown_event, GameLoopEvents.KeyboardHandlerMapping(
            keycode=pygame.K_UP,
            handler=self.__create_move_event_handler(pygame.K_UP)
        ))
        self.add_event_handler(keydown_event, GameLoopEvents.KeyboardHandlerMapping(
            keycode=pygame.K_DOWN,
            handler=self.__create_move_event_handler(pygame.K_DOWN)
        ))
        self.add_event_handler(keydown_event, GameLoopEvents.KeyboardHandlerMapping(
            keycode=pygame.K_LEFT,
            handler=self.__create_move_event_handler(pygame.K_LEFT)
        ))
        self.add_event_handler(keydown_event, GameLoopEvents.KeyboardHandlerMapping(
            keycode=pygame.K_RIGHT,
            handler=self.__create_move_event_handler(pygame.K_RIGHT)
        ))

    def configurable_setup(self):
        super(SnakeGameEvents, self).configurable_setup()
        original_dims = self.config.get_config_val("window_size")
        pygame.draw.line(self.window, Colors.BLACK, (10, 10), (0, original_dims[1]), 10)
        pygame.draw.line(self.window, Colors.BLACK, (original_dims[0], 0), original_dims, 10)
        pygame.display.update()

if __name__ == "__main__":
    config = GameConfig()
    config.set_config_val("clock_rate", 60)
    config.set_config_val("window_size", (600, 600))
    config.set_config_val("window_title", "SNAKE!")
    config.set_config_val("debug_mode", True)

    screen = SnakeScreen(config, (10, 10))
    loop_events = SnakeGameEvents(config, screen)
    loop = GameLoop(loop_events)
    loop.go()
