#! usr/bin/env python3

from components.core import Colors, GameConfig, GameLoop, GameLoopEvents, GameModel, GameScreen
from components.shapes import Point, PointShape

import math

"""
Renders a scene full of fractal trees.

@author Chad Estioco
"""

class TreeScreen(GameScreen):
    
    def __init__(self, config):
        super(TreeScreen, self).__init__(config, GameModel())
        self.__line_stack = []
    
    @property
    def line_stack(self):
        return self.__line_stack
    
    def draw_screen(self, window):
        super(TreeScreen, self).draw_screen(window)
        line_pointshape = self.line_stack.pop()
        line_pointshape.draw(window)

class TreeLoopEvents(GameLoopEvents):
    
    # The angle at which branches branch off, in radians
    BRANCH_ANGLE = 0.523598776
    
    # FIXME I think initial_length should be a config value
    def __init__(self, screen, initial_length):
        super(TreeLoopEvents, self).__init__(screen)
        self.__wood_length = initial_length
        self.configurable_setup()
    
    @property
    def wood_length(self):
        return self.__wood_length
    
    @wood_length.setter
    def wood_length(self, l):
        self.__wood_length = l
    
    def loop_invariant(self):
        parent_invariant = super(TreeLoopEvents, self).loop_invariant()
        return len(self.game_screen.line_stack) and parent_invariant
    
    def loop_setup(self):
        center_x = self.config.get_config_val("window_size")[GameConfig.WIDTH_INDEX] / 2
        bottom_y = self.config.get_config_val("window_size")[GameConfig.WIDTH_INDEX]
        endpoint_y = bottom_y - self.wood_length
        line_pointshape = PointShape([Point(center_x, bottom_y), Point(center_x, endpoint_y)])
        self.game_screen.line_stack.append(line_pointshape)
    
    def loop_event(self):
        line_stack_length = len(self.game_screen.line_stack)
        current_line = self.game_screen.line_stack[line_stack_length - 1]
        
        super(TreeLoopEvents, self).loop_event()
        
        # Grow the new branches 1/3 and 2/3 of the way on the current branch
        # These define the starting points. y-coordinates first, then x
        point_list = current_line.point_list
        y_length = math.fabs(point_list[0].y - point_list[1].y + 1)
        y_branch1 = math.floor(0.33 * y_length)
        y_branch2 = math.floor(0.66 * y_length)
        
        x_length = math.fabs(point_list[0].x - point_list[1].x + 1)
        x_branch1 = math.floor(0.33 * x_length)
        x_branch2 = math.floor(0.66 * y_length)
        
        
if __name__ == "__main__":
    config = GameConfig()
    config.set_config_val("clock_rate", 60)
    config.set_config_val("window_size", (600, 600))
    config.set_config_val("window_title", "Trees")

    screen = TreeScreen(config)
    loop_events = TreeLoopEvents(screen, 300)
    loop = GameLoop(loop_events)
    loop.go()
