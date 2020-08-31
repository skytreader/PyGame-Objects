from components.helpers.scheduler import Scheduler
from mock import MagicMock, Mock, patch

import unittest

class Event(object):
    
    def __init__(self):
        self.times_called = 0

    def happen(self):
        self.times_called += 1

class SchedulerTests(unittest.TestCase):
    
    MOCK_FRAME_RATE = 18
    MOCK_EVENT_FREQUENCY = 3
    
    def setUp(self):
        self.event = Event()
        self.scheduler = Scheduler(SchedulerTests.MOCK_FRAME_RATE,
          SchedulerTests.MOCK_EVENT_FREQUENCY, self.event.happen)

    def test_event(self):
        for _ in range(SchedulerTests.MOCK_FRAME_RATE):
            self.scheduler.event()

        self.assertEqual(SchedulerTests.MOCK_EVENT_FREQUENCY, self.event.times_called)

        for _ in range(SchedulerTests.MOCK_FRAME_RATE):
            self.scheduler.event()

        self.assertEqual(SchedulerTests.MOCK_EVENT_FREQUENCY * 2,
          self.event.times_called)
