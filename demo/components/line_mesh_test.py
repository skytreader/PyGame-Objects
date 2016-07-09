#! usr/bin/env python

from components.core import GameLoop, GameLoopEvents, GameConfig, GameScreen, Colors
from components.shapes import Point, PointShape

import random

"""
Demo stuff for PointShape.

@author Chad Estioco
"""

class LineMeshScreen(GameScreen):
    
    def __init__(self, screen_size):
        super(LineMeshScreen, self).__init__(screen_size)
    
    @property
    def triangle(self):
        return self.__triangle
    
    def setup(self):
        self.__triangle = PointShape([Point(250, 50), Point(50, 350), Point(400, 250)])
    
    def draw_screen(self, window):
        self.triangle.draw(window)

class LineMesh(GameLoopEvents):
    """
    Creates a line mesh with a triangle for its initial shape.
    
    You can change the number of mutations the triangle undergoes
    by setting self.__limit.
    
    I want a 500x500 window!
    """
    
    def __init__(self, config, game_screen):
        super(LineMesh, self).__init__(config, game_screen)
        self.__limit = 200
        self.__count = 0
        
    
    def loop_invariant(self):
        parent_invariant = super(LineMesh, self).loop_invariant()
        return self.__count < self.__limit and parent_invariant
    
    def loop_event(self):
        self.window.fill(Colors.WHITE)
        self.game_screen.triangle.draw(self.window)
        self.game_screen.triangle.add_point(Point(random.randint(0, 500), random.randint(0, 500)))
        
        self.__count += 1

config = GameConfig()
config.window_size = [500, 500]
config.clock_rate = 10
config.window_title = "Line Mesh"

game_screen = LineMeshScreen(config.window_size)

ms = LineMesh(config, game_screen)
game_loop = GameLoop(ms)
game_loop.go()
