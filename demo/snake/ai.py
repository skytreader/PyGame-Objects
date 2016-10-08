from components.framework_exceptions import VectorDirectionException
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
    
    QUADRATIC_DIRECTIONS = set((QuadraticGrid.Movements.UP,
      QuadraticGrid.Movements.DOWN, QuadraticGrid.Movements.LEFT,
      QuadraticGrid.Movements.RIGHT))
    
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

    def __is_snake_limited(self, snake, proposed_food_pos):
        if proposed_food_pos == QuadraticGrid.Movements.UP:
            return snake.head[0] == 0
        elif proposed_food_pos == QuadraticGrid.Movements.DOWN:
            return snake.head[0] == (self.grid_height - 1)
        elif proposed_food_pos == QuadraticGrid.Movements.LEFT:
            return snake.head[1] == 0
        elif proposed_food_pos == QuadraticGrid.Movements.RIGHT:
            return snake.head[1] == (self.grid_width - 1)
        else:
            raise VectorDirectionException("Proposed food position is not a cardinal direction.")

    def get_spawn(self, snake):
        """
        Even for power players, this method will not be called "too fast" for
        computers.

        The only caveat here is that the counts may update while we are doing
        statistics on them.
        """
        ranker = []
        snake_squares = snake.enumerate_snake_squares()

        for k in self.global_counts.keys():
            heapq.heappush(ranker, (self.global_counts[k], k))

        if len(ranker) < 2:
            return (random.randint(0, self.grid_width - 1), random.randint(0, self.grid_height - 1))

        top1 = heapq.heappop(ranker)
        top2 = heapq.heappop(ranker)
        unchosen = set(top1, top2)
        bottom = SpawnManager.QUADRATIC_DIRECTIONS - unchosen
        chosen = random.choice(bottom)
        
        if self.__is_snake_limited(snake, chosen):
            unchosen.add(chosen)
            # This must be a singleton
            last = SpawnManager.QUADRATIC_DIRECTIONS - unchosen
            chosen = last.pop()

        food = snake.head

        while food in snake_squares:
            food = (food[0] + chosen[0], food[1] + chosen[1])

        return food
