

from components.helpers.grid import QuadraticGrid
from demo.snake.model import Snake
from demo.snake.ai import SimpleRankSpawnManager, SpawnManagerIgnoramus, WindowedCount

import random
import unittest

class WindowedCountTests(unittest.TestCase):
    
    def setUp(self):
        self.windowed_count = WindowedCount()

    def test_incr(self):
        self.assertEqual(self.windowed_count.record_size, 0)
        self.windowed_count.incr("spam")
        self.assertEqual(self.windowed_count.record_size, 1)

        for _ in range(self.windowed_count.window_size * 2):
            self.windowed_count.incr("spam")

        self.assertEqual(self.windowed_count.window_size, self.windowed_count.record_size)

    def test_incr_different_keys(self):
        self.assertEqual(self.windowed_count.record_size, 0)
        
        half = int(self.windowed_count.window_size / 2)

        for _ in range(half):
            self.windowed_count.incr("spam")
            self.windowed_count.incr("eggs")

        self.assertEqual(half * 2, self.windowed_count.record_size)
        self.windowed_count.incr("spam&eggs")
        self.assertEqual(half - 1, self.windowed_count.counts["spam"])
        self.assertEqual(half, self.windowed_count.counts["eggs"])
        self.assertEqual(1, self.windowed_count.counts["spam&eggs"])

class SimpleRankSpawnManagerTests(unittest.TestCase):
    
    def setUp(self):
        self.spawn_manager_rect = SimpleRankSpawnManager(4, 6)
        self.spawn_manager_playtest = SimpleRankSpawnManager(10, 10)

    def test_note_movement(self):
        def make_moves(movement):
            spam = random.randint(1, 4)
            for _ in range(spam):
                self.spawn_manager_rect.note_movement(movement)

        make_moves(QuadraticGrid.Movements.UP)
        make_moves(QuadraticGrid.Movements.DOWN)
        make_moves(QuadraticGrid.Movements.LEFT)
        make_moves(QuadraticGrid.Movements.RIGHT)

        self.assertTrue(self.spawn_manager_rect.global_counts[QuadraticGrid.Movements.UP] > 0)
        self.assertTrue(self.spawn_manager_rect.global_counts[QuadraticGrid.Movements.DOWN] > 0)
        self.assertTrue(self.spawn_manager_rect.global_counts[QuadraticGrid.Movements.LEFT] > 0)
        self.assertTrue(self.spawn_manager_rect.global_counts[QuadraticGrid.Movements.RIGHT] > 0)

    def test_get_spawn(self):
        # Initial case, just test that it will return something acceptable
        # The snake head is irrelevant here.
        food_coords = self.spawn_manager_rect.get_spawn(Snake())
        self.assertTrue(food_coords[0] >= 0)
        self.assertTrue(food_coords[0] < 4)
        self.assertTrue(food_coords[1] >= 0)
        self.assertTrue(food_coords[1] < 6)

        # Construct a snake that loops around itself.
        snake = Snake()
        snake.head = (3, 7)
        snake.joints = [(6, 7), (6, 3), (5, 3), (5, 2), (7, 2), (7, 8), (3, 8)]
        snake_squares = snake.enumerate_snake_squares()

        # Repeat 100 times so that the test may include all branches
        for _ in range(100):
            food_coords = self.spawn_manager_playtest.get_spawn(snake)
            self.assertTrue(food_coords not in snake_squares)

        movements = (QuadraticGrid.Movements.UP, QuadraticGrid.Movements.DOWN,
          QuadraticGrid.Movements.LEFT, QuadraticGrid.Movements.RIGHT)

        for _ in range(100):
            self.spawn_manager_playtest.note_movement(random.choice(movements))

        for _ in range(100):
            food_coords = self.spawn_manager_playtest.get_spawn(snake)
            self.assertTrue(food_coords not in snake_squares)

class SpawnManagerIgnoramusTests(unittest.TestCase):
    
    def setUp(self):
        self.spawn_manager = SpawnManagerIgnoramus(10, 10)

    def test_get_spawn(self):
        snake = Snake()
        snake.head = (3, 7)
        snake.joints = [(6, 7), (6, 3), (5, 3), (5, 2), (7, 2), (7, 8), (3, 8)]
        snake_squares = snake.enumerate_snake_squares()

        for _ in range(100):
            food_coords = self.spawn_manager.get_spawn(snake)
            self.assertTrue(food_coords not in snake_squares)
