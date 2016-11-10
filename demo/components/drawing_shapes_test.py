#! usr/bin/env python

from components.core import Colors
from components.core import GameConfig
from components.core import GameLoop
from components.core import GameLoopEvents
from components.core import GameModel
from components.core import GameScreen

from components.shapes import PointShape
from components.shapes import Point

from components.helpers.scheduler import Scheduler

import pygame

"""
Shows a four-sided figure gliding across the screen.

@author Chad Estioco
"""

class RandomDrawing(GameLoopEvents):
    """
    Wanted to draw a rectangle but oh, what the hey...ended up with
    an arrow-like object! :))
    """
    
    def __init__(self, config, gamescreen):
        super(RandomDrawing, self).__init__(config, gamescreen)
        self.__game_screen = gamescreen
        self.s = Scheduler(config.get_config_val("clock_rate"), 1, self.__translate)
    
    def loop_event(self):
        super(RandomDrawing, self).loop_event()
        self.s.event()

    def __translate(self):
        self.game_screen.ps.translate(10, 10)

class RandomDrawingScreen(GameScreen):
    
    def __init__(self, config):
        super(RandomDrawingScreen, self).__init__(config, GameModel())
        self.__ps = PointShape()
        self.__ps.add_point(Point(3, 5))
        self.__ps.add_point(Point(15, 25))
        self.__ps.add_point(Point(10, 40))
        self.__ps.add_point(Point(30, 28))
    
    @property
    def ps(self):
        return self.__ps
    
    def draw_screen(self, window):
        window.fill(Colors.MAX_WHITE)
        self.ps.draw(window)

if __name__ == "__main__":
    config = GameConfig()
    config.set_config_val("window_size", (600, 600))
    config.set_config_val("clock_rate", 12)
    
    gamescreen = RandomDrawingScreen(config)
    
    loopevents = RandomDrawing(config, gamescreen)
    gl = GameLoop(loopevents)
    gl.go()
