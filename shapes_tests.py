#! usr/bin/python2

from shapes import PointShape
from shapes import Point
import unittest

class shapes_tests(unittest.TestCase):
	
	def setUp(self):
		self.__four_points = PointShape([Point(3,4), Point(5,1), Point(8,10), Point(6,9)])
		#self.__four_points.point_list = []
		#self.__four_points.add_point(Point(3, 4))
		#self.__four_points.add_point(Point(5, 1))
		#self.__four_points.add_point(Point(8, 10))
		#self.__four_points.add_point(Point(6, 9))
	
	def test_translate(self):
		print ""
		print self.__four_points.__str__()
		self.__four_points.translate(1, 1)
		translated = PointShape()
		print "Fresh translated:"
		print translated.__str__()
		translated.point_list = [Point(4, 5), Point(6, 2), Point(9, 11), Point(7, 10)]
		print self.__four_points.__str__()
		print translated.__str__()
		self.assertTrue(self.__four_points.__eq__(translated))
	
	def test___str__(self):
		stringed = "PointShape: [ (3, 4) (5, 1) (8, 10) (6, 9) ]"
		self.assertEqual(self.__four_points.__str__(), stringed)
	
	def test_set(self):
		lazy_pointshape = PointShape()
		pl = [Point(1, 2), Point(2,3), Point(4,5)]
		lazy_pointshape.point_list = pl
		#print "set lazy_pointshape"
		#print lazy_pointshape.__str__()
		self.assertTrue(pl == lazy_pointshape.point_list)

if __name__ == "__main__":
	tests = unittest.TestLoader().loadTestsFromTestCase(shapes_tests)
	unittest.TextTestRunner(verbosity=2).run(tests)
