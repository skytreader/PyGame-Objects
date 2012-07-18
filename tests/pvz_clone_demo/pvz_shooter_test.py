#! usr/bin/env python

from ...components.core import Colors
from ...components.core import GameLoopEvents
from ...components.core import GameConfig
from ...components.core import GameLoop
from ...components.core import KeyCodes

from ...components.framework_exceptions import InstanceException

from ...components.image import Image

from ...components.subscriber_pattern import Observer

from ...components.shapes import Point

import os

import pygame

"""
A shooting game inspired by Plants vs Zombies.

Branch-off from image_test.py
"""

class PVZSprite(pygame.sprite.Sprite, Observer):
	"""
	A zombie is a sprite that moves from the right side of the
	screen to the left side. Zombies typically start off-screen
	and march to the right side. When a zombie reaches the left
	side, the player losses.
	"""
	
	def __init__(self, move_speed, img, hit_points):
		"""
		@param move_speed
		  The speed at which the zombie marches, specified in pixels.
		@param img
		  An instance of Image, which is the Zombie's character
		  representation. Not to be confused with Sprite's self.image .
		  This constructor automatically loads self.image with the surface
		  contained in img .
		  
		  TODO: Give PointShape a Surface property so that it can be drawn
		  as a sprite.
		  
		@param hit_points
		  The number of hits it takes for the Zombie to go down. That is,
		  this zombie's maximum HP.
		
		@param pos
		  A Point object specifying this Zombie's position.
		"""
		
		super(PVZSprite, self).__init__()
		
		self.__speed = move_speed
		self.__screen_draw = img
		self.__screen_draw.subscribe(self)
		self.__max_hp = hit_points
		self.__hp = hit_points
		
		#Set sprite attributes
		self.image = img.img
		self.rect = self.image.get_rect()
		self.rect.y = img.position.y
		self.rect.x = img.position.x
	
	@property
	def speed(self):
		return self.__speed
	
	@speed.setter
	def speed(self, s):
		self.__speed = s
	
	@property
	def screen_draw(self):
		"""
		Returns the Image object of this sprite.
		"""
		return self.__screen_draw
	
	@screen_draw.setter
	def screen_draw(self, i):
		"""
		Sets the Image object of this sprite.
		"""
		self.__screen_draw = i
		self.image = self.screen_draw.img
	
	@property
	def max_hp(self):
		return self.__max_hp
	
	@property
	def hp(self):
		"""
		Returns the _current_ HP of this Zombie
		"""
		return self.__hp
	
	@hp.setter
	def hp(self, new_hp):
		"""
		Throws an exception when new_hp is greater than
		self.max_hp
		
		@param new_hp
		  The new HP of this Zombie.
		"""
		if new_hp > self.max_hp:
			raise HPException("Gave a zombie more HP than it's worth!")
		else:
			self.__hp = new_hp
	
	def notify(self, observed, arg_bundle = None):
		self.image = self.screen_draw.img
		self.rect.x = self.screen_draw.position.x
		self.rect.y = self.screen_draw.position.y
	
class Zombie(PVZSprite):
	
	def __init__(self, move_speed, img, hit_points):
		super(Zombie, self).__init__(move_speed, img, hit_points)
	
	def update(self):
		new_pos = Point(self.screen_draw.position.x - self.speed, \
			self.screen_draw.position.y)
		self.screen_draw.position = new_pos

class Shooter(PVZSprite):
	"""
	A shooter is the controllable character in a PVZ game.
	"""
	
	def __init__(self, move_speed, img, hit_points):
		super(Shooter, self).__init__(move_speed, img, hit_points)
		self.__is_going_up = False
	
	@property
	def is_going_up(self):
		return self.__is_going_up
	
	@is_going_up.setter
	def is_going_up(self, go_up):
		self.__is_going_up = go_up
	
	def move(self):
		if self.is_going_up:
			move_delta = -self.speed
		else:
			move_delta = self.speed
		
		new_pos = Point(0, self.screen_draw.position.y + move_delta)
		self.screen_draw.position = new_pos

class HPException(Exception):
	"""
	Thrown when a zombie/plant is given an HP greater than it's
	max HP.
	
	Example taken from:
	http://docs.python.org/tutorial/errors.html#user-defined-exceptions
	"""
	
	def __init__(self, value):
		self.value = value
	
	def __str__(self):
		return repr(self.value)

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
