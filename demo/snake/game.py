from components.core import GameConfig
from components.core import GameScreen
from components.helpers.grid import QuadraticGrid
from model import GameModel

import pygame

class SnakeScreen(GameScreen):
    
    def __init__(self, screen_size, grid_size):
        super(SnakeScreen, self).__init__(screen_size)
        self.game_model = GameModel(grid_size[0], grid_size[1])
