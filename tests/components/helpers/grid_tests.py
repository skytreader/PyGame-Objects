import unittest

from components.core import GameConfig, GameModel, GameScreen
from components.framework_exceptions import VectorDirectionException
from components.helpers.grid import BorderProperties, QuadraticGrid
from mock import patch

import pygame
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

    @patch("components.helpers.grid.pygame.draw.line", autospec=True)
    @patch("components.helpers.grid.pygame.draw.rect", autospec=True)
    def test_draw(self, draw_rect, draw_line):
        game_screen = GameScreen(GameConfig(), GameModel())
        window = pygame.display.set_mode((1, 1))
        quadratic_grid = QuadraticGrid(4, 4)
        quadratic_grid.draw(window, game_screen)
        self.assertTrue(draw_rect.called)
        self.assertFalse(draw_line.called)

    @patch("components.helpers.grid.pygame.draw.line", autospec=True)
    @patch("components.helpers.grid.pygame.draw.rect", autospec=True)
    def test_draw_borders(self, draw_rect, draw_line):
        game_screen = GameScreen(GameConfig(), GameModel())
        window = pygame.display.set_mode((1, 1))
        qg = QuadraticGrid(4, 4, border_properties=BorderProperties())
        qg.draw(window, game_screen)
        self.assertTrue(draw_rect.called)
        self.assertTrue(draw_line.called)

    def test_get_clicked_cell_squarefull(self):
        square_config = GameConfig(window_size=(80, 80))
        square_screen = GameScreen(square_config, GameModel())
        square_grid = QuadraticGrid(8, 8)
        self.assertEqual((7, 3), square_grid.get_clicked_cell(square_screen, (36, 74)))

    def test_get_clicked_algorithmspkg(self):
        algrid_config = GameConfig(window_size=(600, 600), debug_mode=True)
        algrid_screen = GameScreen(algrid_config, GameModel())
        algrid_qg = QuadraticGrid(
            10, 10, diag_neighbors=False, border_properties=BorderProperties()
        )
        self.assertEqual((4, 7), algrid_qg.get_clicked_cell(algrid_screen, (424, 294)))

    def test_get_clicked_height_limited(self):
        grid_config = GameConfig(window_size=(400, 600))
        screen = GameScreen(grid_config, GameModel())
        qg = QuadraticGrid(10, 10, 400, 400)
        self.assertEqual((8, 3), qg.get_clicked_cell(screen, (121, 323)))
