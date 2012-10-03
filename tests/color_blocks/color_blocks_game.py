#! usr/bin/env python

from ...components.core import Colors
from ...components.core import GameConfig
from ...components.core import GameLoop
from ...components.core import GameLoopEvents
from ...components.core import GameScreen
from ...components.shapes import Point
from ...components.shapes import PointShape

from ...helpers.grid import QuadraticGrid

from color_blocks_model import ColorBlocksModel

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
		super(ColorBlocksScreen, self).__init__(screen_size)
		self.__game_model = ColorBlocksModel(grid_size[0], grid_size[1], 2)
		# Instantiate an underlying grid model
		# Python 2 automatically floors division. Beware when this code
		# is run on Python 3!
		self.__block_width = screen_size[0] / grid_size[0]
		self.__block_height = (screen_size[1] - HEIGHT_OFFSET) / grid_size[1]
		self.__grid_model = QuadraticGrid(screen_size[0] / self.block_width, (screen_size[1] - HEIGHT_OFFSET) / self.block_height)
	
	@property
	def game_model(self):
		return self.__game_model
	
	@property
	def grid_model(self):
		return self.__grid_model
	
	@property
	def block_width(self):
		return self.__block_width
	
	@property
	def block_height(self):
		return self.__block_height
	
	@property
	def rect_list(self):
		return self.__rect_list
	
	@property
	def color_list(self):
		return self.__color_list
	
	def setup(self):
		self.represent_tiles()
	
	def represent_tiles(self):
		"""
		Scans the game model and then lists their assigned colors.
		"""
		# rect_list and color_list are associative arrays.
		# for the rect described in rect_list, its color is
		# in color_list.
		self.__rect_list = []
		self.__color_list = []
		raw_grid = self.game_model.grid
		rowlen = len(raw_grid)
		collen = len(raw_grid[0])
		
		for i in range(rowlen):
			for j in range(collen):
				upper_left_x = j * self.block_width
				upper_left_y = i * self.block_height + HEIGHT_OFFSET
				rect = (upper_left_x, upper_left_y, self.block_width, self.block_height)
				self.rect_list.append(rect)
				
				if raw_grid[i][j] == ColorBlocksModel.UNTAKEN:
					self.color_list.append(Colors.WHITE)
				else:
					color_index = int(raw_grid[i][j])
					self.color_list.append(ColorBlocksScreen.COLOR_MAPPING[color_index])
	
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
		row_index = (pos[1] - HEIGHT_OFFSET) / screen.block_height
		col_index = pos[0] / screen.block_width
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
