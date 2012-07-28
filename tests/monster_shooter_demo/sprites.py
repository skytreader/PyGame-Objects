#! usr/bin/env python

from ...components.image import Image

from ...components.subscriber_pattern import Observer

from ...components.shapes import Point

import os

import pygame

import thread

class PVZSprite(pygame.sprite.Sprite, Observer):
	"""
	General behavior of a PVZ Game Sprite
	
	@author Chad Estioco
	"""
	
	def __init__(self, move_speed, img, hit_points):
		"""
		@param move_speed
		  The speed at which this sprite moves, specified in pixels.
		@param img
		  An instance of Image, which is the sprite's character
		  representation. Not to be confused with Sprite's self.image .
		  This constructor automatically loads self.image with the surface
		  contained in img .
		  
		@param hit_points
		  The number of hits it takes for this sprite to go down. That is,
		  this sprite's maximum HP.
		
		@param pos
		  A Point object specifying this sprite's position.
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
	"""
	A zombie is a sprite that moves from the right side of the
	screen to the left side. Zombies typically start off-screen
	and march to the right side. When a zombie reaches the left
	side, the player losses.
	
	@author Chad Estioco
	"""
	
	def __init__(self, move_speed, img, hit_points):
		super(Zombie, self).__init__(move_speed, img, hit_points)
	
	def update(self):
		new_pos = Point(self.screen_draw.position.x - self.speed, \
			self.screen_draw.position.y)
		self.screen_draw.position = new_pos

class Shooter(PVZSprite):
	"""
	A shooter is the controllable character in a PVZ game.
	
	@author Chad Estioco
	"""
	
	def __init__(self, move_speed, img, hit_points, max_bullet_pos):
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
	
class Bullet(pygame.sprite.Sprite):
	"""
	A Bullet is only put on screen when the Shooter wants to
	shoot some monsters.
	
	@author Chad Estioco
	"""
	
	def __init__(self, xpos, ypos):
		super(Bullet, self).__init__()
		
		bullet_image = Image(os.path.join("PyGame_Objects", "sample_sprites", "bullet.png"))
		bullet_image.position.x = xpos
		bullet_image.position.y = ypos
		
		self.image = bullet_image.img
		self.rect = bullet_image.img.get_rect()
		self.rect.x = bullet_image.position.x
		self.rect.y = bullet_image.position.y
	
	def update(self):
		self.rect.x += 10
		

class HPException(Exception):
	"""
	Thrown when a zombie/plant is given an HP greater than it's
	max HP.
	
	Example taken from:
	http://docs.python.org/tutorial/errors.html#user-defined-exceptions
	
	@author Chad Estioco
	"""
	
	def __init__(self, value):
		self.value = value
	
	def __str__(self):
		return repr(self.value)
