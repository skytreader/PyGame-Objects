#! usr/bin/env python

class Drawable(object):
    """
    All classes that represent something that can be drawn on a PyGame
    screen canvas should extend this class and implement draw().
    """

    def __init__(self, draw_offset, height_limit=None, width_limit=None):
        """
        draw_offset is a (width, height) tuple.
        """
        self.draw_offset = draw_offset
    
    def draw(self, screen, **kwargs):
        """
        Implement all drawing logic here!
        
        @param screen
          The PyGame display to which we draw whatever needs to
          be drawn.
        """
        pass

    def invariant_scale(self, scale_factor):
        """
        Scale this shape regardless of where the shape is put.
        """
        pass
