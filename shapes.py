#! usr/bin/python2

from core import Colors
from drawable import Drawable

import pygame

"""
Encapsulates closed-figure objects you can draw on screen.

Sample Usage (see also: drawing_shapes_test.py):
  (1) Extend GameLoopEvents (core.py). Create an instance
      of PointShape. Note that the shape is defined by the
      Points you put in this object.
  (2) In the loop_event of your GameLoopEvents extension, call
      the draw method of your PointShape object.
      
      (Note that a GameLoopEvent object can pass self.window for
      the screen argument to draw.)
  (3) Have fun!
"""

class PointShape(Drawable):
	"""
	Defines closed figures as a collection of Points. It is
	possible to define a circle using this class though it
	will be cumbersome.
	
	Specify the Points in the order with which you would like
	them connected. The last point will be automatically
	connected to the first point.
	"""
	
	def __init__(self, point_list = None, color = Colors.BLACK):
		"""
		Create a PointShape with no points.
		"""
		if point_list is None:
			self.__point_list = []
		else:
			self.__point_list = point_list
		self.__color = color
	
	def add_point(self, p):
		"""
		Add a point to the point list. This will change how this
		PointShape is drawn.
		"""
		self.point_list.append(p)
	
	def translate(self, dx, dy):
		"""
		Translates this PointShape by dx pixels on the x axis and by
		dy pixels on the y axis.
		"""
		incr_xs = map(lambda p: Point(p.x + dx, p.y), self.point_list)
		incr_ys = map(lambda p: Point(p.x, p.y + dy), incr_xs)
		self.point_list = incr_ys
	
	@property
	def point_list(self):
		return self.__point_list
	
	@point_list.setter
	def point_list(self, point_list):
		"""
		TODO: Is this a good idea? The whole PointShape may change?
		"""
		self.__point_list = point_list
	
	def draw(self, screen):
		"""
		Shapes with only one point is not a shape and so is
		not drawn.
		
		Shapes with no point do not exist and so are not drawn.
		
		@param screen
			The window to which we draw this PointShape.
		"""
		limit = len(self.point_list) - 1
		i = 0
		
		while i < limit:
			point0 = self.point_list[i]
			point1 = self.point_list[i + 1]
			
			pygame.draw.line(screen, self.__color, point0.get_list(), point1.get_list())
			
			i += 1
		
		if limit > 0:
			# Since we end at limit - 1, limit should now hold the index
			# to the last point in the point list
			pygame.draw.line(screen, self.__color, self.point_list[limit].get_list(), self.point_list[0].get_list())
	
	def __eq__(self, other_shape):
		"""
		Two PointShapes are equal if and only if their point_lists
		are exactly the same.
		"""
		i = 0
		limit = len(other_shape.point_list)
		
		if limit != len(self.point_list):
			return False
		
		while i < limit:
			if not self.point_list[i].__eq__(other_shape.point_list[i]):
				return False
			
			i += 1
		
		return True
		
	def __str__(self):
		stringed = "PointShape: ["
		
		for point in self.point_list:
			stringed += " " + str(point)
		
		return stringed + " ]"
	
	
class Point:
	"""
	Represents a point in 2D-space.
	"""
	
	def __init__(self, x, y):
		self.__x = x
		self.__y = y
	
	@property
	def x(self):
		return self.__x
	
	@property
	def y(self):
		return self.__y
	
	def get_list(self):
		return [self.x, self.y]
	
	def __eq__(self, other_point):
		return self.x == other_point.x and self.y == other_point.y
	
	def __str__(self):
		return "(" + str(self.x) + ", " + str(self.y) + ")"
