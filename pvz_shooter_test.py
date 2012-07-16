#! usr/bin/env python

from core import GameLoopEvents
from core import GameConfig
from core import GameLoop
from core import Colors

from image import Image

from shapes import Point

import pygame

"""
A shooting game inspired by Plants vs Zombies.

Branch-off from image_test.py
"""

class Zombie(pygame.sprite.Sprite):
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
		
		super(Zombie, self).__init__()
		
		self.__speed = move_speed
		self.__screen_draw = img
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
	
	def update(self):
		self.rect.x -= self.speed

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

class ImageLoader(GameLoopEvents):
	
	def __init__(self, config):
		super(ImageLoader, self).__init__(config)
		self.__meteormon = None
	
	def loop_event(self):
		self.window.fill(Colors.WHITE)
		self.__sprite_group.draw(self.window)
		self.__sprite_group.update()
		
	def loop_setup(self):
		super(ImageLoader, self).loop_setup()
		meteormon = Image("sample_sprites/meteormon_clueless.png")
		init_x = super(ImageLoader, self).config.window_size[GameConfig.WIDTH_INDEX] - \
			meteormon.width
		
		meteormon.position = Point(init_x, 0)
		
		self.__sprite_group = pygame.sprite.Group()
		meteormon_sprite = Zombie(5, meteormon, 10)
		self.__sprite_group.add(meteormon_sprite)

config = GameConfig()
config.window_size = [500, 500]
config.clock_rate = 12
config.window_title = "Image Class Test"
image_gle = ImageLoader(config)
gl = GameLoop(image_gle)
gl.go()
