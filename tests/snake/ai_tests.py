from __future__ import division

from components.helpers.grid import QuadraticGrid
from demo.snake.ai import SpawnManager, WindowedCount

import random
import unittest

class WindowedCountTests(unittest.TestCase):
    
    def setUp(self):
        self.windowed_count = WindowedCount()

    def test_incr(self):
        self.assertEquals(self.windowed_count.record_size, 0)
        self.windowed_count.incr("spam")
        self.assertEquals(self.windowed_count.record_size, 1)

        for _ in range(self.windowed_count.window_size * 2):
            self.windowed_count.incr("spam")

        self.assertEquals(self.windowed_count.window_size, self.windowed_count.record_size)

    def test_incr_different_keys(self):
        self.assertEquals(self.windowed_count.record_size, 0)
        
        half = int(self.windowed_count.window_size / 2)

        for _ in range(half):
            self.windowed_count.incr("spam")
            self.windowed_count.incr("eggs")

        self.assertEquals(half * 2, self.windowed_count.record_size)
        self.windowed_count.incr("spam&eggs")
        self.assertEquals(half - 1, self.windowed_count.counts["spam"])
        self.assertEquals(half, self.windowed_count.counts["eggs"])
        self.assertEquals(1, self.windowed_count.counts["spam&eggs"])

class SpawnManagerTests(unittest.TestCase):
    
    def setUp(self):
        self.spawn_manager = SpawnManager()

    def test_note_movement(self):
        def make_moves(movement):
            spam = random.randint(1, 4)
            for _ in range(spam):
                self.spawn_manager.note_movement(movement)

        make_moves(QuadraticGrid.Movements.UP)
        make_moves(QuadraticGrid.Movements.DOWN)
        make_moves(QuadraticGrid.Movements.LEFT)
        make_moves(QuadraticGrid.Movements.RIGHT)

        self.assertTrue(self.spawn_manager.global_counts[QuadraticGrid.Movements.UP] > 0)
        self.assertTrue(self.spawn_manager.global_counts[QuadraticGrid.Movements.DOWN] > 0)
        self.assertTrue(self.spawn_manager.global_counts[QuadraticGrid.Movements.LEFT] > 0)
        self.assertTrue(self.spawn_manager.global_counts[QuadraticGrid.Movements.RIGHT] > 0)
