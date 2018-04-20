from components.core import Colors, GameConfig, GameLoop, GameLoopEvents, GameScreen
from components.framework_exceptions import VectorDirectionException
from components.helpers.grid import QuadraticGrid
from components.helpers.scheduler import Scheduler
from model import SnakeGameModel

import logging
import math
import pygame

class SnakeScreen(GameScreen):
    
    GAME_OVER_FONT_SIZE = 28
    GAME_OVER_FONT = pygame.font.Font("fonts/forcedsquare/forcedsquare.ttf", GAME_OVER_FONT_SIZE)
    
    def __init__(self, config, grid_size):
        super(SnakeScreen, self).__init__(config, SnakeGameModel(grid_size[0], grid_size[1]))
        screen_size = config.get_config_val("window_size")
        self.game_model = self.model
        self.game_model.initialize()

        self.block_width = int(math.floor(screen_size[0] / grid_size[0]))
        self.block_height = int(math.floor(screen_size[1] / grid_size[1]))

        self.automove_schedule = Scheduler(config.get_config_val("clock_rate"),
          1, self.__automove_snake)

    def __automove_snake(self):
        current_direction = self.game_model.snake.get_orientation()
        self.game_model.move_snake(current_direction)

    def draw_screen(self, window):
        snake_squares = self.game_model.snake.enumerate_snake_squares()

        for snake_pos in snake_squares:
            color = Colors.DIM_GRAY if snake_pos == self.game_model.snake.head else Colors.EBONY
            snake_pos = QuadraticGrid.make_rect(snake_pos, self.block_width, self.block_height)
            pygame.draw.rect(window, color, snake_pos, 0) 

        if self.game_model.food_point:
            fp_rect = QuadraticGrid.make_rect(self.game_model.food_point, self.block_width, self.block_height)
            pygame.draw.rect(window, Colors.NIGHT_GRAY, fp_rect, 0)

        if self.game_model.is_endgame():
            # Render a "Game Over" sign
            game_over_render = SnakeScreen.GAME_OVER_FONT.render("GAME OVER", True, Colors.HUMAN_RED)
            window.blit(game_over_render, (50, 50))

        self.automove_schedule.event()

    def draw_unchanging(self, window):
        super(SnakeScreen, self).draw_unchanging(window)
        original_dims = self.config.get_config_val("window_size")
        pygame.draw.line(window, Colors.MAX_BLACK, (0, 0), (0, original_dims[1]), 10)
        pygame.draw.line(window, Colors.MAX_BLACK, (0, 0), (original_dims[0], 0), 10)
        pygame.draw.line(window, Colors.MAX_BLACK, (original_dims[0], 0), original_dims, 10)
        pygame.draw.line(window, Colors.MAX_BLACK, (0, original_dims[1]), original_dims, 10)

class SnakeGameEvents(GameLoopEvents):
    
    def __init__(self, screen):
        super(SnakeGameEvents, self).__init__(screen)
        self.key_controls = GameLoopEvents.KeyControls()
        self.key_controls.register_key(
            pygame.K_UP,
            self.__create_move_event_handler(pygame.K_UP)
        )
        self.key_controls.register_key(
            pygame.K_DOWN,
            self.__create_move_event_handler(pygame.K_DOWN)
        )
        self.key_controls.register_key(
            pygame.K_LEFT,
            self.__create_move_event_handler(pygame.K_LEFT)
        )
        self.key_controls.register_key(
            pygame.K_RIGHT,
            self.__create_move_event_handler(pygame.K_RIGHT)
        )

    def loop_event(self):
        self.window.fill(Colors.MAX_WHITE)
        super(SnakeGameEvents, self).loop_event()

    def __create_move_event_handler(self, key):
        def event_handler(event):
            current_direction = self.game_screen.model.snake.get_orientation()
            height = self.game_screen.game_model.height
            width = self.game_screen.game_model.width
            movement = QuadraticGrid.Movements.KEY_TO_DIR[key]
            if current_direction == movement:
                return

            try:
                self.game_screen.model.move_snake(movement, True)
                self.debug_queue.log("snake head now at %s" % str(self.game_screen.model.snake.head))
                self.debug_queue.log(str(self.game_screen.model.snake.enumerate_snake_squares()))
                new_head = self.game_screen.model.snake.head
            except VectorDirectionException:
                self.debug_queue.log("attempted 180 turn", logging.WARNING)
        
        return event_handler

    def attach_event_handlers(self):
        keydown_event = pygame.event.Event(pygame.KEYDOWN)
        self.add_event_handler(keydown_event, self.key_controls.handle)

if __name__ == "__main__":
    config = GameConfig()
    config.set_config_val("clock_rate", 60)
    config.set_config_val("window_size", (600, 600))
    config.set_config_val("window_title", "SNAKE!")
    config.set_config_val("debug_mode", True)
    config.set_config_val("log_to_terminal", True)
    config.set_config_val("difficulty", 1)

    screen = SnakeScreen(config, (10, 10))
    loop_events = SnakeGameEvents(screen)
    loop = GameLoop(loop_events)
    loop.go()
