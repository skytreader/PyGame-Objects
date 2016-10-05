from __future__ import division

from demo.snake.ai import SpawnManager, WindowedCount

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
