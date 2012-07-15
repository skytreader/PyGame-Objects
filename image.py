#! usr/bin/env python

from drawable import Drawable
from shapes import Point

import pygame

class Image(Drawable):
	
	def __init__(self, filename):
		"""
		TODO: What happens if the file described by the filename does not
		exist? What happens if the file is deleted while we are using it?
		Do I need to close this resource?
		
		@param filename
		  The filename of the image, relative to the code listing.
		"""
		super(Image, self).__init__()
		self.__img = pygame.image.load(filename).convert()
		self.__position = Point(0,0)
	
	@property
	def img(self):
		return self.__img
	
	@img.setter
	def img(self, i):
		self.__img = i
	
	@property
	def position(self):
		return self.__position
	
	@position.setter
	def position(self, position):
		"""
		Sets where this image will be drawn on screen.
		
		@param position
		  A Point describing where this image gets drawn on screen.
		"""
		self.__position = position
	
	@property
	def height(self):
		return self.img.get_height()
	
	@property
	def width(self):
		return self.img.get_width()
	
	def draw(self, screen):
		"""
		Draws the image on the screen. To set where this image gets drawn
		on screen, use the position setter. Otherwise, this image gets drawn
		at point (0, 0) by default.
		"""
		super(Image, self).draw(screen)
		screen.blit(self.img, self.position.get_list())
