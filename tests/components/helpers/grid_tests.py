import unittest

from components.framework_exceptions import VectorDirectionException
from components.helpers.grid import QuadraticGrid

import random
import unittest

class QuadraticGridTests(unittest.TestCase):
    
    def test_movements(self):
        left_vector = {"tail": (0, 1), "head": (0, 0)}
        self.assertEquals(QuadraticGrid.Movements.compute_direction(**left_vector),
          QuadraticGrid.Movements.LEFT)

        right_vector = {"tail": (0, 0), "head": (0, 1)}
        self.assertEquals(QuadraticGrid.Movements.compute_direction(**right_vector),
          QuadraticGrid.Movements.RIGHT)

        stay_vector = {"tail": (0, 0), "head": (0, 0)}
        self.assertEquals(QuadraticGrid.Movements.compute_direction(**stay_vector),
          QuadraticGrid.Movements.STAY)

        up_vector = {"tail": (1, 0), "head": (0, 0)}
        self.assertEquals(QuadraticGrid.Movements.compute_direction(**up_vector),
          QuadraticGrid.Movements.UP)

        down_vector = {"tail": (0, 0), "head": (1, 0)}
        self.assertEquals(QuadraticGrid.Movements.compute_direction(**down_vector),
          QuadraticGrid.Movements.DOWN)

        self.assertRaises(VectorDirectionException,
          QuadraticGrid.Movements.compute_direction, (1, 1), (2, 2))
    
    def test_adjacent_list(self):
        one_row = QuadraticGrid(5, 1)
        adj = one_row.get_adjacent(0, 0)
        self.assertEqual(set(adj), set([(0, 1)]))
        adj = one_row.get_adjacent(0, 3)
        self.assertEqual(set(adj), set([(0, 2), (0, 4)]))
        adj = one_row.get_adjacent(0, 4)
        self.assertEqual(set(adj), set([(0, 3)]))
        
        one_col = QuadraticGrid(1, 5)
        adj = one_col.get_adjacent(0, 0)
        self.assertEqual(set(adj), set([(1, 0)]));
        adj = one_col.get_adjacent(3, 0)
        self.assertEqual(set(adj), set([(2, 0), (4, 0)]))
        adj = one_col.get_adjacent(4, 0)
        self.assertEqual(set(adj), set([(3, 0)]))
        
        matrix = QuadraticGrid(3, 4)
        adj = matrix.get_adjacent(0, 0)
        self.assertEqual(set(adj), set([(0, 1), (1, 0), (1, 1)]))
        adj = matrix.get_adjacent(0, 2)
        self.assertEqual(set(adj), set([(0, 1), (1, 1), (1, 2)]))
        adj = matrix.get_adjacent(3, 0)
        self.assertEqual(set(adj), set([(2, 0), (2, 1), (3, 1)]))
        adj = matrix.get_adjacent(3, 2)
        self.assertEqual(set(adj), set([(3, 1), (2, 1), (2, 2)]))
        adj = matrix.get_adjacent(2, 1)
        self.assertEqual(set(adj), set([(2, 0), (2, 2), (1, 0), (1, 1), (1, 2), (3, 0), (3, 1), (3, 2)]))
        
        self.assertRaises(IndexError, matrix.get_adjacent, 10, 10)
        self.assertRaises(TypeError, matrix.get_adjacent, 0.0, "zero")
