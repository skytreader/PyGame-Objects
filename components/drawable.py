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
    
    def draw(self, screen):
        """
        Implement all drawing logic here!
        
        @param screen
          The PyGame display to which we draw whatever needs to
          be drawn.
        """
        pass
    
    def set_scale(self, new_width, new_height, old_width, old_height):
        """
        Set the scale of this drawable object. Can be used to adjust
        to screen size.
        
        @param new_width
          The width to which we adjust to (e.g., the width of the new window).
        @param new_heigth
          The height to which we adjust to (e.g., the height of the new window).
        @param old_width
        @param old_height
        """
        pass
