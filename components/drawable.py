#! usr/bin/env python

class Drawable(object):
    """
    All classes that represent something that can be drawn on a PyGame
    screen canvas should extend this class and implement draw().

    In the context of this framework, instantiate your drawables in your
    GameScreen object and then invoke their draw methods in either `draw_screen`
    or `draw_unchanging`.
    """

    def __init__(self, draw_offset, width_limit=None, height_limit=None):
        """
        draw_offset is a (row, col) tuple.
        """
        self.draw_offset = draw_offset if draw_offset else (0, 0)
        # TODO Make the semantics like so: if width_limit is None, make it scale
        # along the screen's width; if height_limit is None, make it scale along
        # the screen's height.
        self.max_size = (width_limit, height_limit)
    
    def draw(self, window, screen, **kwargs):
        """
        Implement all drawing logic here!
        
        @param window
            The PyGame display to which we draw whatever needs to
            be drawn.
        @param screen
            A GameScreen from components.core
        """
        raise NotImplementedError("Subclasess must implement this!")

    def invariant_scale(self, scale_factor):
        """
        Scale this shape regardless of where the shape is put.
        """
        raise NotImplementedError("Not implemented...yet.")
