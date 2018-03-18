#! usr/bin/env python

class Drawable(object):
    """
    All classes that represent something that can be drawn on a PyGame
    screen canvas should extend this class and implement draw().

    In the context of this framework, instantiate your drawables in your
    GameScreen object and then invoke their draw methods in either `draw_screen`
    or `draw_unchanging`.
    """

    def __init__(self, draw_offset, height_limit=None, width_limit=None):
        """
        draw_offset is a (width, height) tuple.
        """
        self.draw_offset = draw_offset if draw_offset else (0, 0)
        self.max_size = (width_limit, height_limit) if width_limit and height_limit else None
    
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
