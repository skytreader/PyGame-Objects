#! usr/bin/env python

from core import GameLoopEvents
from core import GameConfig
from core import GameLoop
from core import Colors

from image import Image

import pygame

class ImageLoader(GameLoopEvents):
	
	def __init__(self, config):
		super(ImageLoader, self).__init__(config)
		self.__meteormon = Image("sample_sprites/meteormon_clueless.png")
	
	def loop_event(self):
		self.__meteormon.draw(self.window)

config = GameConfig()
config.window_size = [500, 500]
config.clock_rate = 10
config.window_title = "Image Class Test"
image_gle = ImageLoader(config)
gl = GameLoop(image_gle)
gl.go()
