#! usr/bin/env python


from components.core import Colors
from components.core import GameConfig
from components.core import GameLoop
from components.core import GameLoopEvents
from components.core import GameScreen
from components.shapes import Point
from components.shapes import PointShape

from components.helpers.grid import BorderProperties, QuadraticGrid

from .color_blocks_model import ColorBlocksModel

import math
import pygame


class ColorBlocksScreen(GameScreen):
    
    COLOR_MAPPING = (Colors.LUCID_DARK, Colors.HUMAN_RED, Colors.HUMAN_GREEN,
      Colors.HUMAN_BLUE, Colors.LIGHT_GRAY)
    GRID_OFFSET = (100, 0)
    
    def __init__(self, config, grid_size):
        """
        Instantiates a ColorBlocksScreen instance.
        
        @param screen_size
          The dimensions of the screen. An iterable whose first element
          is taken for the width while the second one is taken for the
          height.
        @param grid_size
          The size of the grid, in squares per dimension. First element
          is taken for the width while the second one is taken for the
          height.
        """
        super(ColorBlocksScreen, self).__init__(config, ColorBlocksModel(grid_size[0], grid_size[1], 2))
        screen_size = config.get_config_val("window_size")
        self.game_model = self.model
        # Instantiate an underlying grid model
        self.block_width = int(math.floor((screen_size[0] - ColorBlocksScreen.GRID_OFFSET[1]) / grid_size[0]))
        self.block_height = int(math.floor((screen_size[1] - ColorBlocksScreen.GRID_OFFSET[0]) / grid_size[1]))
        self.grid_model = QuadraticGrid(
            grid_size[0], grid_size[1],
            draw_offset=ColorBlocksScreen.GRID_OFFSET,
            border_properties=BorderProperties()
        )
        self.rect_list = []
        self.color_list = []
    
    def setup(self):
        self.represent_tiles()
    
    def represent_tiles(self):
        """
        Scans the game model and then lists their assigned colors.
        """
        # rect_list and color_list are associative arrays.
        # for the rect described in rect_list, its color is
        # in color_list.
        self.rect_list, self.color_list = QuadraticGrid.cons_rect_list(
          self.grid_model, self.model, self.block_width, self.block_height,
          offset=ColorBlocksScreen.GRID_OFFSET
        )
    
    def draw_screen(self, window):
        self.grid_model.draw(window, self)
        score_font = pygame.font.Font(None, 25)
        score = score_font.render("Score: " + str(self.game_model.score), True, Colors.HUMAN_RED)
        window.blit(score, [10, 10])

class ColorBlocksEvents(GameLoopEvents):
    
    def __init__(self, screen):
        super(ColorBlocksEvents, self).__init__(screen)
        self.key_control = GameLoopEvents.KeyControls()
        self.key_control.register_key(pygame.K_F2, self.__trigger_new_game)
    
    def __mouse_click(self, event):
        pos = pygame.mouse.get_pos()
        row_index, col_index = self.game_screen.grid_model.get_clicked_cell(
            self.game_screen, pos
        )
        self.game_screen.game_model.score += self.game_screen.game_model.toggle(row_index, col_index)
        self.game_screen.game_model.falldown()
        self.game_screen.game_model.collapse()
        self.game_screen.represent_tiles()
    
    def __trigger_new_game(self):
        self.game_screen.game_model.new_game()
        self.game_screen.represent_tiles()
    
    def attach_event_handlers(self):
        button_down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN)
        self.add_event_handler(button_down_event, self.__mouse_click)
        
        self.add_event_handler(pygame.event.Event(pygame.KEYDOWN), self.key_control.handle)
    
    def loop_event(self):
        self.window.fill(Colors.MAX_WHITE)
        super(ColorBlocksEvents, self).loop_event()

def main():
    config = GameConfig()
    config.set_config_val("clock_rate", 12)
    config.set_config_val("window_size", [500, 500 + ColorBlocksScreen.GRID_OFFSET[0]])
    config.set_config_val("window_title", "Color Blocks Game")
    
    screen = ColorBlocksScreen(config, [10, 10])
    loop_events = ColorBlocksEvents(screen)
    return loop_events

if __name__ == "__main__":
    loop_events = main()
    GameLoop(loop_events).go()
