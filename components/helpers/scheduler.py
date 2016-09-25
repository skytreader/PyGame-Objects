"""
A scheduler will tell you if an event is due to happen in the current clock
tick.

Assumes that the game's frame rate is constant, which may not always be the
case. For future iterations, look into
[pygame.time.Clock.get_fps](http://www.pygame.org/docs/ref/time.html#pygame.time.Clock.get_fps).
"""

class Scheduler(object):
    
    def __init__(self, frame_rate, event_frequency, event):
        """
        frame_rate - as configured
        event_frequency - expressed per second
        event - a Python callable
        """
        self.frame_rate = frame_rate
        self.event_frequency = event_frequency
        self.__event = event
        self.time = 0
        self.event_count = 0

    def event(self):
        """
        Just keep calling this on every iteration of your game loop. This will
        guarantee that the `event` given to this object will be called at most
        `event_frequency` times in one second.
        """
        if (self.time % self.frame_rate) == 0:
            self.event_count = 0

        if self.event_count < self.event_frequency:
            self.__event()
