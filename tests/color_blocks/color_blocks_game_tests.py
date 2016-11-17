from components.core import GameLoop
from demo.color_blocks.color_blocks_game import main

import pygame
import sched
import time
import unittest

class ColorBlocksGameTests(unittest.TestCase):

    def setUp(self):
        self.scheduler = sched.scheduler(time.time, time.sleep)

    def test_main(self):
        loop_events = main()
        self.scheduler.enter(1, 1, loop_events.stop_main, (pygame.QUIT,))
        self.scheduler.run()
        GameLoop(loop_events).go()
