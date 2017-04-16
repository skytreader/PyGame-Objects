from __future__ import division

from components.drawable import Drawable

class StaticWorldObject(Drawable):

    def __init__(self, location, sprite):
        """
        @param location
            A component.shapes.Point object.
        @param sprite
            A component.sprite.PyRoSprite object.
        """
        self.__location = location
        self.__sprite = sprite

class Explorable(Drawable):

    def __init__(self, world_objects, initial_view, draw_offset=0):
        """
        An explorable world is one where not all objects is in view at once.
        """
        super(Explorable, self).__init__(draw_offset)
        self.world_objects = world_objects
        self.initial_view = initial_view
