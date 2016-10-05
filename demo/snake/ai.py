from components.helpers.grid import QuadraticGrid

import heapq
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
        
        if count:
            self.counts[count_key] += 1
        else:
            self.counts[count_key] = 1

        self.record_size += 1

        heapq.heappush(self.timeheap, (time.time(), count_key))

class SpawnManager(object):
    
    def __init__(self, window=8):
        self.global_counts = {}
        self.window_counts = WindowedCount()

    def note_movement(self, movement):
        self.window_counts.incr(movement)

        count = self.global_counts.get(movement)

        if count:
            self.global_counts[count_key] += 1
        else:
            self.global_counts[count_key] = 1

    def get_spawn(self):
        pass
