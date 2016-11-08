#! usr/bin/env python

class Drawable(object):
    """
    All classes that represent something that can be drawn on a PyGame
    screen canvas should extend this class and implement draw().
    
    This class is akin to a Java interface so it is not necessary for classes
    directly extending this class to call super methods. Don't call them
    if it will cause conflicts with other parent classes that may have
    logic involved (case in point, constructor).
    
    @author Chad Estioco
    """

    def __init__(self, draw_offset):
        self.draw_offset = draw_offset
    
    def draw(self, screen):
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
