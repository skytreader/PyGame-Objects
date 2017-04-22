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

    def __init__(self, world_objects, initial_view, draw_offset=None):
        """
        An explorable world is one where not all objects is in view at once.

        v0.1.0: Actually draw everything in memory, just hidden from view.

        world_objects - A collection of StaticWorldObjects.
        initial_view - The upper-left coordinates of what is initially visible.
        draw_offset - As required by Drawable.
        """
        draw_offset = draw_offset if draw_offset else None
        super(Explorable, self).__init__(draw_offset)
        self.world_objects = world_objects
        self.initial_view = initial_view

    def draw(self, window, screen, **kwargs):
        window_size = window.get_surface().get_size()
