#! usr/bin/env python

from components.shapes import PointShape
from components.shapes import Point
from components.shapes import CollisionBox

import unittest

"""
Unit tests for the shapes module.

@author Chad Estioco
"""

class shapes_tests(unittest.TestCase):
    
    def setUp(self):
        self.__four_points = PointShape()
        self.__four_points.add_point(Point(3, 4))
        self.__four_points.add_point(Point(5, 1))
        self.__four_points.add_point(Point(8, 10))
        self.__four_points.add_point(Point(6, 9))
        
        pl = [Point(5, 4), Point(5, 7), Point(3, 9), Point(5, 11), Point(5, 13), Point(1, 13), \
            Point(1, 16), Point(8, 16), Point(10, 14), Point(9, 12), Point(12, 9), Point(9, 6), Point(9,4)]
        self.__shape = PointShape(pl)
    
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
    
    def test_collision_box(self):
        """
        Create a new PointShape object and test whether it, indeed, gets
        the CollisionBox expected.
        """
        expected_box = CollisionBox(Point(1, 4), Point(12, 16))
        self.assertTrue(expected_box.__eq__(self.__shape.collision_box))
        
        new_point = Point(15, 3)
        self.__shape.add_point(new_point)
        expected_box = CollisionBox(Point(1,3), Point(15,16))
        self.assertTrue(expected_box.__eq__(self.__shape.collision_box))
    
    def test_set_scale(self):
        # A triangle confined in a 10x10 screen
        triangle_pl = [Point(5,1), Point(1,7), Point(8,7)]
        triangle = PointShape(triangle_pl)
        triangle_scaled = [Point(5 * 50, 50), Point(50, 50 * 7), Point(50 * 8, 50 * 7)]
        triangle.set_scale(500, 500, 10, 10)
        self.assertTrue(triangle.point_list == triangle_scaled)

    def test_equality(self):
        four_points = PointShape()
        four_points.add_point(Point(3, 4))
        four_points.add_point(Point(5, 1))
        four_points.add_point(Point(8, 10))
        four_points.add_point(Point(6, 9))

        self.assertTrue(four_points == four_points)
        self.assertFalse(four_points == self.__shape)
        self.assertTrue(four_points == self.__four_points)

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
    
    def test___eq__(self):
        b1 = CollisionBox(Point(1, 1), Point(2, 2))
        b2 = CollisionBox(Point(1, 1), Point(2, 2))
        b3 = CollisionBox(Point(1, 1), Point(2, 3))
        b4 = CollisionBox(Point(0, 1), Point(2, 2))
        b5 = CollisionBox(Point(1, 4), Point(1, 5))
        
        self.assertTrue(b1.__eq__(b2))
        self.assertTrue(not b1.__eq__(b3))
        self.assertTrue(not b1.__eq__(b4))
        self.assertTrue(not b1.__eq__(b5))

if __name__ == "__main__":
    tests = unittest.TestLoader().loadTestsFromTestCase(shapes_tests)
    unittest.TextTestRunner(verbosity=2).run(tests)
    
    tests = unittest.TestLoader().loadTestsFromTestCase(collisionbox_tests)
    unittest.TextTestRunner(verbosity=2).run(tests)
