#! usr/bin/env python

from ...components.core import Colors
from ...components.core import GameLoopEvents
from ...components.core import GameConfig
from ...components.core import GameLoop
from ...components.core import KeyCodes

from ...components.framework_exceptions import InstanceException

from ...components.image import Image

from ...components.shapes import Point

from sprites import Zombie, Shooter

import os

import pygame

"""
A shooting game inspired by Plants vs Zombies.
"""

class PVZEvents(GameLoopEvents):
	
	def __init__(self, config):
		super(PVZEvents, self).__init__(config)
		self.__meteormon = None
	
	def loop_event(self):
		self.window.fill(Colors.WHITE)
		self.__sprite_group.draw(self.window)
		self.__sprite_group.update()
	
	def move_shooter(self, event):
		
		if event.key == KeyCodes.UP:
			is_up = True
		elif event.key == KeyCodes.DOWN:
			is_up = False
		
		self.__shooter_sprite.is_going_up = is_up
		self.__shooter_sprite.move()
		
	def loop_setup(self):
		super(PVZEvents, self).loop_setup()
		meteormon = Image(os.path.join("PyGame_Objects","sample_sprites","meteormon_clueless.png"))
		bakemon = Image(os.path.join("PyGame_Objects","sample_sprites","bakemon_attack.png"))
		shooter_image = Image(os.path.join("PyGame_Objects","sample_sprites","seahomon_hero.png"))
		shooter_image.flip(True, False)
		
		init_x = super(PVZEvents, self).config.window_size[GameConfig.WIDTH_INDEX] - \
			meteormon.width
		#off-screen
		bakemon_x = init_x + meteormon.height
		
		meteormon.position = Point(init_x, 0)
		bakemon.position = Point(bakemon_x, meteormon.height)
		shooter_image.position = Point(0, self.config.window_size[GameConfig.HEIGHT_INDEX] / 2)
		
		self.__sprite_group = pygame.sprite.Group()
		meteormon_sprite = Zombie(5, meteormon, 10)
		bakemon_sprite = Zombie(8, bakemon, 10)
		self.__shooter_sprite = Shooter(7, shooter_image, 10)
		self.__sprite_group.add(meteormon_sprite)
		self.__sprite_group.add(bakemon_sprite)
		self.__sprite_group.add(self.__shooter_sprite)

class PVZLoop(GameLoop):
	
	def __init__(self, events):
		"""
		FIXME: Is this Pythonic enough?
		
		@param events
		  Must be an instance of PVZEvents.
		"""
		if isinstance(events, PVZEvents):
			super(PVZLoop, self).__init__(events)
		else:
			raise InstanceException("PVZLoop expects an instance of PVZEvents")
	
	def attach_event_handlers(self):
		self.add_event_handler(pygame.event.Event(pygame.KEYDOWN), self.loop_events.move_shooter)

config = GameConfig()
config.window_size = [500, 500]
config.clock_rate = 12
config.window_title = "Image Class Test"
image_gle = PVZEvents(config)
gl = PVZLoop(image_gle)
gl.go()
