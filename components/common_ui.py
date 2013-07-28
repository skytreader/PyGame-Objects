from common_shapes import Rectangle

from core import Colors

from drawable import Drawable

from shapes import Point
from shapes import PointShape

"""
This module manages some common-UI functionalities like buttons
and menus.

TODO: Maybe, integrate this with common_shapes ?
TODO: If we are to use common shapes with this, we must have a facility
to flood fill PointShapes.
"""

class Button(Drawable):
	"""
	A button has three states: untouched, hover, and pushed.
	"""
	
	def __init__(self, upper_left, lower_right, btn_color = Colors.LUCID_DARK, text, text_color = Colors.WHITE):
		self.__button_area = Rectangle(upper_left, lower_right)
		self.__button_text = text
		self.__text_color = text_color
	
	@property
	def button_area(self):
		return self.__button_area
	
	@property
	def button_text(self):
		return self.__button_text
	
	@button_text.setter
	def button_text(self, new_text):
		self.__button_text = new_text
	
	@property
	def text_color(self):
		return self.__text_color
