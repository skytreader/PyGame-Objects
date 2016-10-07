from components.helpers.grid import QuadraticGrid

import heapq
import random
import time

class WindowedCount(object):
    
    def __init__(self, window=8):
        self.window_size = window
        self.counts = {}
        self.record_size = 0
        self.timeheap = []

    def incr(self, count_key):
        assert self.record_size <= self.window_size
        if self.record_size == self.window_size:
            oldest_entry = heapq.heappop(self.timeheap)[1]
            self.counts[oldest_entry] -= 1
            self.record_size -= 1

        count = self.counts.get(count_key)
        
        if count: self.counts[count_key] += 1
        else:
            self.counts[count_key] = 1

        self.record_size += 1

        heapq.heappush(self.timeheap, (time.time(), count_key))

class SpawnManager(object):
    
    QUADRATIC_DIRECTIONS = set(QuadraticGrid.Movements.UP,
      QuadraticGrid.Movements.DOWN, QuadraticGrid.Movements.LEFT,
      QuadraticGrid.Movements.RIGHT)
    
    def __init__(self, grid_width, grid_height, window=8):
        self.global_counts = {}
        self.window_counts = WindowedCount()
        self.grid_width = grid_width
        self.grid_height = grid_height

    def note_movement(self, movement):
        self.window_counts.incr(movement)

        count = self.global_counts.get(movement)

        if count:
            self.global_counts[movement] += 1
        else:
            self.global_counts[movement] = 1

    def get_spawn(self, snake_squares):
        """
        Even for power players, this method will not be called "too fast" for
        computers.

        The only caveat here is that the counts may update while we are doing
        statistics on them.
        """
        ranker = []

        for k in self.global_counts.keys():
            heapq.heappush(ranker, (self.global_counts[k], k))

        if len(ranker) < 2:
            return (random.randint(0, self.grid_width), random.randint(0, self.grid_height))

        top1 = heapq.heappop(ranker)
        top2 = heapq.heappop(ranker)
        tops = set(top1, top2)
        bottom = SpawnManager.QUADRATIC_DIRECTIONS - tops
        lucky_bottom = random.choice(bottom)
