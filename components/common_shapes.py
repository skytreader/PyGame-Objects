from core import Colors

from shapes import Point
from shapes import PointShape

"""
This module contains some common shapes you may want
to draw on your games. A (sort of) alternative to using
pygame.draw.* .
"""

class Rectangle(PointShape):
	
	def __init__(self, upper_left, lower_right, line_color):
		self.__upper_left = upper_left
		self.__lower_right = lower_right
		upper_right = Point(lower_right.x, upper_left.y)
		lower_left = Point(upper_left.x, lower_right.y)
		super(Rectangle, self).__init__([upper_left, upper_right, lower_right, lower_left], line_color)
	
	@property
	def upper_left(self):
		return self.__upper_left
	
	@property
	def lower_right(self):
		return self.__lower_right
