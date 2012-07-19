#! usr/bin/env python

from ...components.core import Colors
from ...components.core import GameLoopEvents
from ...components.core import GameConfig
from ...components.core import GameLoop
from ...components.core import GameScreen
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

class PVZMainScreen(GameScreen):
	
	def __init__(self, screen_dimensions):
		super(PVZMainScreen, self).__init__(screen_dimensions)
		self.__sprite_group = pygame.sprite.Group()
	
	@property
	def sprite_group(self):
		return self.__sprite_group
	
	@property
	def shooter_sprite(self):
		return self.__shooter_sprite
	
	def setup(self):
		super(PVZMainScreen, self).setup()
		meteormon = Image(os.path.join("PyGame_Objects","sample_sprites","meteormon_clueless.png"))
		bakemon = Image(os.path.join("PyGame_Objects","sample_sprites","bakemon_attack.png"))
		shooter_image = Image(os.path.join("PyGame_Objects","sample_sprites","seahomon_hero.png"))
		shooter_image.flip(True, False)
		
		init_x = super(PVZMainScreen, self).screen_dimensions[GameConfig.WIDTH_INDEX] - \
			meteormon.width
		#off-screen
		bakemon_x = init_x + meteormon.height
		
		meteormon.position = Point(init_x, 0)
		bakemon.position = Point(bakemon_x, meteormon.height)
		shooter_image.position = Point(0, super(PVZMainScreen, self).screen_dimensions[GameConfig.HEIGHT_INDEX] / 2)
		
		meteormon_sprite = Zombie(5, meteormon, 10)
		bakemon_sprite = Zombie(8, bakemon, 10)
		self.__shooter_sprite = Shooter(7, shooter_image, 10)
		self.sprite_group.add(meteormon_sprite)
		self.sprite_group.add(bakemon_sprite)
		self.sprite_group.add(self.shooter_sprite)
	
	def draw_screen(self, window):
		self.sprite_group.draw(window)
		self.sprite_group.update()

class PVZEvents(GameLoopEvents):
	
	def __init__(self, config, game_screen):
		super(PVZEvents, self).__init__(config, game_screen)
		self.__meteormon = None
	
	def loop_event(self):
		self.window.fill(Colors.WHITE)
		super(PVZEvents, self).loop_event()
	
	def move_shooter(self, event):
		
		if event.key == KeyCodes.UP:
			is_up = True
		elif event.key == KeyCodes.DOWN:
			is_up = False
		
		super(PVZEvents, self).game_screen.shooter_sprite.is_going_up = is_up
		super(PVZEvents, self).game_screen.shooter_sprite.move()
		
	def loop_setup(self):
		super(PVZEvents, self).loop_setup()

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
			raise TypeError("PVZLoop expects an instance of PVZEvents")
	
	def attach_event_handlers(self):
		self.add_event_handler(pygame.event.Event(pygame.KEYDOWN), self.loop_events.move_shooter)

config = GameConfig()
config.window_size = [500, 500]
config.clock_rate = 12
config.window_title = "PvZ Clone Demo"

screen = PVZMainScreen(config.window_size)

image_gle = PVZEvents(config, screen)
gl = PVZLoop(image_gle)
gl.go()
