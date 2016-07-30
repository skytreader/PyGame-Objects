#! usr/bin/env python
from __future__ import division

from components.core import Colors
from components.core import GameConfig
from components.core import GameLoop
from components.core import GameLoopEvents
from components.core import GameScreen
from components.shapes import Point
from components.shapes import PointShape

from components.helpers.grid import QuadraticGrid

from color_blocks_model import ColorBlocksModel

import math
import pygame

HEIGHT_OFFSET = 100

class ColorBlocksScreen(GameScreen):
    
    COLOR_MAPPING = (Colors.LUCID_DARK, Colors.RED, Colors.GREEN, Colors.BLUE, Colors.LIGHT_GRAY)
    
    def __init__(self, screen_size, grid_size):
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
        super(ColorBlocksScreen, self).__init__(screen_size, ColorBlocksModel(grid_size[0], grid_size[1], 2))
        self.game_model = self.model
        # Instantiate an underlying grid model
        self.block_width = int(math.floor(screen_size[0] / grid_size[0]))
        self.block_height = int(math.floor((screen_size[1] - HEIGHT_OFFSET) / grid_size[1]))
        self.grid_model = QuadraticGrid(grid_size[0], grid_size[1])
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
          height_offset=HEIGHT_OFFSET
        )
    
    def draw_screen(self, window):
        """
        Right now, the _whole_ screen is allocated for the color blocks
        grid. Later, we'll add a some margins for scores and shiz.
        
        And the color blocks won't be demarcated with lines. Not yet. Yes,
        messy, I know.
        """
        limit = len(self.color_list)
        
        for i in range(limit):
            pygame.draw.rect(window, self.color_list[i], self.rect_list[i], 0)
        
        score_font = pygame.font.Font(None, 25)
        score = score_font.render("Score: " + str(self.game_model.score), True, Colors.RED)
        window.blit(score, [10, 10])

class ColorBlocksEvents(GameLoopEvents):
    
    def __init__(self, screen, config):
        super(ColorBlocksEvents, self).__init__(screen, config)
    
    # Wow. Amusing that this works. Where'd they get the screen?
    def __mouse_click(self, event):
        pos = pygame.mouse.get_pos()
        row_index = int(math.floor((pos[1] - HEIGHT_OFFSET) / screen.block_height))
        col_index = int(math.floor(pos[0] / screen.block_width))
        screen.game_model.score += screen.game_model.toggle(row_index, col_index)
        screen.game_model.falldown()
        screen.game_model.collapse()
        screen.represent_tiles()
    
    def __trigger_new_game(self, event):
        self.game_screen.game_model.new_game()
        self.game_screen.represent_tiles()
    
    def attach_event_handlers(self):
        button_down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN)
        self.add_event_handler(button_down_event, self.__mouse_click)
        
        new_game_dict = {}
        new_game_dict[GameLoopEvents.KEYCODE] = pygame.K_F2
        new_game_dict[GameLoopEvents.HANDLER] = self.__trigger_new_game
        self.add_event_handler(pygame.event.Event(pygame.KEYDOWN), new_game_dict)
    
    def loop_event(self):
        self.window.fill(Colors.WHITE)
        super(ColorBlocksEvents, self).loop_event()

if __name__ == "__main__":
    config = GameConfig()
    config.clock_rate = 12
    config.window_size = [500, 500 + HEIGHT_OFFSET]
    config.window_title = "Color Blocks Game"
    
    screen = ColorBlocksScreen(config.window_size, [10, 10])
    loop_events = ColorBlocksEvents(config, screen)
    loop = GameLoop(loop_events)
    loop.go()
