import unittest

from components.framework_exceptions import VectorDirectionException
from components.helpers.grid import QuadraticGrid

class QudraticGrid(unittest.TestCase):
    
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
