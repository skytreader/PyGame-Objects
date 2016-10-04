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

class SpawnManagerTests(unittest.TestCase):
    
    def setUp(self):
        self.spawn_manager = SpawnManager()
