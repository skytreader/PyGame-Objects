from components.helpers.grid import QuadraticGrid

import time

class WindowedCount(object):
    
    def __init__(self, window=8):
        self.window_counts = {}
        self.timestamps = {}

    def incr(self, count_key):
        count = self.window_counts.get(count_key)
        
        if count:
            self.window_counts[count_key] += 1
        else:
            self.window_counts[count_key] = 1

        self.timestamps[count_key] = int(time.time() * 1000)

class SpawnManager(object):
    
    def __init__(self, window=8):
        self.global_counts = {}
        self.window_counts = WindowedCount()
