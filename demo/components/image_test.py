#! usr/bin/env python

from components.core import GameLoopEvents
from components.core import GameConfig
from components.core import GameLoop
from components.core import GameScreen
from components.core import Colors

from components.image import Image

from components.shapes import Point

import os

import pygame

class ImageLoader(GameLoopEvents):
    
    def __init__(self, config, game_screen):
        super(ImageLoader, self).__init__(config, game_screen)
    
    def loop_event(self):
        super(ImageLoader, self).loop_event()
        new_x = self.game_screen.meteormon.position.x - 10
        
        self.game_screen.meteormon.position = Point(new_x, 0);
        
    def loop_setup(self):
        super(ImageLoader, self).loop_setup()
        init_x = super(ImageLoader, self).config.window_size[GameConfig.WIDTH_INDEX] - \
            self.game_screen.meteormon.width
        
        self.game_screen.meteormon.position = Point(init_x, 0)

class ImageScreen(GameScreen):
    
    @property
    def meteormon(self):
        return self.__meteormon
    
    def setup(self):
        super(ImageScreen, self).setup()
        self.__meteormon = Image(os.path.join("sample_sprites","meteormon_clueless.png"))
    
    def draw_screen(self, window):
        super(ImageScreen, self).draw_screen(window)
        window.fill(Colors.WHITE)
        self.meteormon.draw(window)

config = GameConfig()
config.window_size = [500, 500]
config.clock_rate = 12
config.window_title = "Image Class Test"
screen = ImageScreen(config.window_size)
image_gle = ImageLoader(config, screen)
gl = GameLoop(image_gle)
gl.go()
