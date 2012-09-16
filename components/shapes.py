#! usr/bin/env python

from core import Colors
from drawable import Drawable
from collidable import Collidable

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
	
	@author Chad Estioco
	"""
	
	def __init__(self, point_list = None, color = Colors.BLACK):
		"""
		Create a PointShape with no points.
		"""
		#Wonder what will happen if I call the super constructor
		#being that the super class got no constructor?
		super(PointShape, self).__init__()
		
		# This box does not exist anywhere in the visible screen
		self.__collision_box = CollisionBox(Point(-1,-1), Point(-1,-1))
		
		if point_list is None or point_list == []:
			self.__point_list = []
		else:
			self.__point_list = point_list
			self.__set_box()
			
		self.__color = color
	
	def add_point(self, p, index = None):
		"""
		Add a point to the point list. This will change how this
		PointShape is drawn. Also adjusts collision_box when necessary.
		
		TODO: Check if index can get len(self.point_list)
		"""
		if index == None:
			index = len(self.point_list)
		
		self.point_list.insert(index, p)
		
		max_x = self.collision_box.lower_right.x
		max_y = self.collision_box.lower_right.y
		min_x = self.collision_box.upper_left.x
		min_y = self.collision_box.upper_left.y
		
		if p.x > max_x:
			self.collision_box.lower_right.x = p.x
		elif p.x < min_x:
			self.collision_box.upper_left.x = p.x
		
		if p.y > max_y:
			self.collision_box.lower_right.y = p.y
		elif p.y < min_y:
			self.collision_box.upper_left.y = p.y
	
	def __set_box(self):
		"""
		Sets the collision_box property of this object.
		
		Call this after everytime __point_list is set (through constructor,
		point_list setter, etc.) or modified (through add_point, etc.)
		"""
		x_list = map(lambda point: point.x, self.point_list)
		y_list = map(lambda point: point.y, self.point_list)
		
		min_x = min(x_list)
		min_y = min(y_list)
		max_x = max(x_list)
		max_y = max(y_list)
		
		box_upper_left = Point(min_x, min_y)
		box_lower_right = Point(max_x, max_y)
		
		self.__collision_box = CollisionBox(box_upper_left, box_lower_right)
	
	@property
	def collision_box(self):
		return self.__collision_box
	
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
		self.__set_box()
	
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
	
	def __x_set(self, point, scale_trans):
		point.x = scale_trans
		return point
	
	def __y_set(self, point, scale_trans):
		point.y = scale_trans
		return point
	
	def set_scale(self, new_width, new_height, old_width, old_height):
		# TODO: Recall that Python 2.x does _integer division_
		width_scale = float(new_width) / old_width
		height_scale = float(new_height) / old_height
		
		# Scale the x
		self.point_list = map(lambda point: self.__x_set(point, point.x * width_scale), self.point_list)
		# Scale the y
		self.point_list = map(lambda point: self.__y_set(point, point.y * height_scale), self.point_list)
	
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

class CollisionBox(Collidable):
	"""
	A CollisionBox defines an area for collision for PointShapes.
	CollisionBoxes implement naive collision detection [VALDEZ, PyCon
	Ph 2012]
	
	A CollisionBox is defined by its upper left and lower right points.
	
	@author Chad Estioco
	"""
	
	def __init__(self, upper_left = None, lower_right = None):
		super(CollisionBox, self).__init__()
		self.__upper_left = upper_left
		self.__lower_right = lower_right
	
	@property
	def upper_left(self):
		return self.__upper_left
	
	@property
	def lower_right(self):
		return self.__lower_right
	
	@upper_left.setter
	def upper_left(self, point):
		self.__upper_left = point
	
	@lower_right.setter
	def lower_right(self, point):
		self.__lower_right = point
	
	@property
	def width(self):
		return self.lower_right.x - self.upper_left.x
	
	@property
	def height(self):
		return self.upper_left.y - self.lower_right.y
	
	def has_collided(self, another_box):
		"""
		Simple test is two boxes (in the rectangular sense of the word)
		intersect.
		"""
		return self.upper_left.x + self.width > another_box.upper_left.x and \
			self.upper_left.x < another_box.upper_left.x + another_box.width and \
			self.upper_left.y + self.height > another_box.upper_left.y and \
			self.upper_left.y < another_box.upper_left.y + another_box.height
	
	def __eq__(self, another_box):
		"""
		Two collision boxes are equal if and only if their upper left
		and lower right points are equal.
		"""
		return self.upper_left.__eq__(another_box.upper_left) and \
			self.lower_right.__eq__(another_box.lower_right)
	
class Point:
	"""
	Represents a point in 2D-space.
	
	@author Chad Estioco
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
	
	@x.setter
	def x(self, new_x):
		self.__x = new_x
	
	@y.setter
	def y(self, new_y):
		self.__y = new_y
	
	def get_list(self):
		return [self.x, self.y]
	
	def distance(self, another_point):
		dx = self.x - another_point.x
		dy = self.y - another_point.y
		square_sum = (dx ** 2) + (dy ** 2)
		
		return math.sqrt(square_sum)
	
	def __eq__(self, other_point):
		return self.x == other_point.x and self.y == other_point.y
	
	def __str__(self):
		return "(" + str(self.x) + ", " + str(self.y) + ")"
