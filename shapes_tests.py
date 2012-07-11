#! usr/bin/python2

from shapes import PointShape
from shapes import Point
from shapes import CollisionBox
import unittest

class shapes_tests(unittest.TestCase):
	
	def setUp(self):
		self.__four_points = PointShape() #PointShape([Point(3,4), Point(5,1), Point(8,10), Point(6,9)])
		#self.__four_points.point_list = []
		self.__four_points.add_point(Point(3, 4))
		self.__four_points.add_point(Point(5, 1))
		self.__four_points.add_point(Point(8, 10))
		self.__four_points.add_point(Point(6, 9))
	
	def test_translate(self):
		self.__four_points.translate(1, 1)
		translated = PointShape()
		translated.point_list = [Point(4, 5), Point(6, 2), Point(9, 11), Point(7, 10)]
		self.assertTrue(self.__four_points.__eq__(translated))
	
	def test___str__(self):
		stringed = "PointShape: [ (3, 4) (5, 1) (8, 10) (6, 9) ]"
		self.assertEqual(self.__four_points.__str__(), stringed)
	
	def test_set(self):
		lazy_pointshape = PointShape()
		pl = [Point(1, 2), Point(2,3), Point(4,5)]
		lazy_pointshape.point_list = pl
		self.assertTrue(pl == lazy_pointshape.point_list)

class collisionbox_tests(unittest.TestCase):
	
	def setUp(self):
		pass
	
	def test_has_collided(self):
		mario = CollisionBox(Point(0, 50), Point(10, 0))
		bowser = CollisionBox(Point(100, 40), Point(150, 0))
		self.assertTrue(not mario.has_collided(bowser))
		self.assertTrue(not bowser.has_collided(mario))
		
		bowser_colliding = CollisionBox(Point(9, 40), Point(141, 0))
		self.assertTrue(mario.has_collided(bowser_colliding))
		self.assertTrue(bowser_colliding.has_collided(mario))

if __name__ == "__main__":
	tests = unittest.TestLoader().loadTestsFromTestCase(shapes_tests)
	unittest.TextTestRunner(verbosity=2).run(tests)
	
	tests = unittest.TestLoader().loadTestsFromTestCase(collisionbox_tests)
	unittest.TextTestRunner(verbosity=2).run(tests)
