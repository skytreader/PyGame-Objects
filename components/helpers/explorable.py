from __future__ import division

from components.core import GameLoopEvents
from components.drawable import Drawable
from components.sprite import PyRoSprite

from components.helpers.grid import QuadraticGrid

import pygame

class ForegroundSprite(PyRoSprite):

    def __init__(self, filename):
        super(ForegroundSprite, self).__init__(filename)

    def update(self, *args):
        pass

class Explorable(Drawable):

    def __init__(self, world_objects, initial_view, draw_offset=None):
        """
        An explorable world is one where not all objects is in view at once.

        v0.1.0: Actually draw everything in memory, just hidden from view.

        world_objects - A pygame.sprite.Group.
        initial_view - The upper-left coordinates of what is initially visible.
        draw_offset - As required by Drawable.
        """
        draw_offset = draw_offset if draw_offset else None
        super(Explorable, self).__init__(draw_offset)
        self.world_objects = world_objects
        self.initial_view = initial_view

    def draw(self, window, screen, **kwargs):
        self.world_objects.draw(window)
        self.world_objects.update()

    def move_camera(self, direction):
        """
        direction - QuadraticGrid.Movements
        """
        tile_translation = QuadraticGrid.Movements.INVERSE_MOVEMAP[direction]
        world_sprites = self.world_objects.sprites()
        for sprite in world_sprites:
            position = Point(
                sprite.screen_draw.position.x + direction[0],
                sprite.screen_draw.position.y + direction[1]
            )
            sprite.screen_draw.position = position

class ExplorableMovements(GameLoopEvents):

    def __init__(self, config, game_screen, explorable):
        super(ExplorableMovements, self).__init__(config, game_screen)
        self.explorable = explorable

    def move_camera(self, event):
        self.explorable.move_camera(self, QuadraticGrid.EVENT_TO_DIR[event])

    def attach_event_handlers(self):
        keydown_event = pygame.event.Event(pygame.KEYDOWN)
