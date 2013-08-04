#! usr/bin/env python

from components.core import GameConfig
from components.core import GameLoopEvents
from components.core import GameLoop
from components.core import GameScreen

import pygame
import random

"""
A simple demo of using the framework that randomly draws
gray circles on a white canvas.

@author Chad Estioco
"""

class GrayCircle(GameLoopEvents):
    
    def __init__(self, config):
        super(GrayCircle, self).__init__(config, GameScreen([500,500]))
        self.__limit = 100
        self.__count = 0
    
    def loop_invariant(self):
        parent_invariant = super(GrayCircle, self).loop_invariant()
        return self.__count < self.__limit and parent_invariant
    
    def loop_event(self):
        x = random.randint(0, 500)
        y = random.randint(0, 500)
        pygame.draw.circle(self.window, [218, 218, 218], [x, y], 50, 2)
        self.__count += 1

gconfig = GameConfig()
gconfig.clock_rate = 10
gconfig.window_size = [500, 500]
gconfig.window_title = "Framework test"
gc_object = GrayCircle(gconfig)
game_loop = GameLoop(gc_object)
game_loop.go()
