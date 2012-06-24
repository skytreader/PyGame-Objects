#! usr/bin/python2

class PointShape:
	"""
	Defines closed figures as a collection of Points. It is
	possible to define a circle using this class though it
	will be cumbersome.
	
	Specify the Points in the order with which you would like
	them connected. The last point will be automatically
	connected to the first point.
	"""
	
	def __init__(self):
		self.__point_list = []
	
	def add_point(self, p):
		self.__point_list.append(p)
	
	def translate(self, dx, dy):
		incr_xs = map(lambda p: Point(p.get_x() + dx, p.get_y()), self.__point_list)
		incr_ys = map(lambda p: Point(p.get_x(), p.get_y() + dy), incr_xs)
		self.__point_list = incr_ys
	
	def get_point_list(self):
		return self.__point_list
	
	def set_point_list(self, point_list):
		self.__point_list = point_list
		
	def __eq__(self, other_shape):
		"""
		Two PointShapes are equal if and only if their point_lists
		are exactly the same.
		"""
		i = 0
		limit = len(other_shape.__point_list)
		
		if limit != len(self.__point_list):
			return False
		
		while i < limit:
			if not self.__point_list[i].__eq__(other_shape.__point_list[i]):
				print str(self.__point_list[i])
				print str(other_shape.__point_list[i])
				return False
			
			i += 1
		
		return True
		
	def __str__(self):
		stringed = "PointShape: ["
		
		for point in self.__point_list:
			stringed += " " + str(point)
		
		return stringed + " ]"
	
	
class Point:
	"""
	Represents a point in 2D-space.
	"""
	
	def __init__(self, x, y):
		self.__x = x
		self.__y = y
	
	def get_x(self):
		return self.__x
	
	def get_y(self):
		return self.__y
	
	def __eq__(self, other_point):
		return self.__x == other_point.__x and self.__y == other_point.__y
	
	def __str__(self):
		return "(" + str(self.__x) + ", " + str(self.__y) + ")"
