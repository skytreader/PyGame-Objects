#! usr/bin/env python

from ..components.core import GameLoopEvents
from ..components.core import GameConfig
from ..components.core import GameLoop
from ..components.core import Colors

from ..components.image import Image

from ..components.shapes import Point

import os

import pygame

class ImageLoader(GameLoopEvents):
	
	def __init__(self, config):
		super(ImageLoader, self).__init__(config)
		self.__meteormon = None
	
	def loop_event(self):
		self.window.fill(Colors.WHITE)
		self.__meteormon.draw(self.window)
		new_x = self.__meteormon.position.x - 10
		
		self.__meteormon.position = Point(new_x, 0);
		
	def loop_setup(self):
		super(ImageLoader, self).loop_setup()
		self.__meteormon = Image(os.path.join("PyGame_Objects","sample_sprites","meteormon_clueless.png"))
		init_x = super(ImageLoader, self).config.window_size[GameConfig.WIDTH_INDEX] - \
			self.__meteormon.width
		
		self.__meteormon.position = Point(init_x, 0)

config = GameConfig()
config.window_size = [500, 500]
config.clock_rate = 12
config.window_title = "Image Class Test"
image_gle = ImageLoader(config)
gl = GameLoop(image_gle)
gl.go()
