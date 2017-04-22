from subscriber_pattern import Subscriber as Observer

import pygame

"""
Convenience class to make PyGame Sprites fit into the
scheme of the framework.

@author Chad Estioco
"""

class PyRoSprite(pygame.sprite.Sprite, Observer):
    
    def __init__(self, img):
        """
        @param img
          An instance of components.image.Image, which is the sprite's character
          representation. Not to be confused with Sprite's self.image .
          This constructor automatically loads self.image with the surface
          contained in img .
        """
        super(PyRoSprite, self).__init__()
        
        self.screen_draw = img
        self.screen_draw.subscribe(self)
        
        self.image = img.img
        self.rect = self.image.get_rect()
        self.rect.y = img.position.y
        self.rect.x = img.position.x
    
    def notify(self, observed, arg_bundle = None):
        self.image = self.screen_draw.img
        self.rect.x = self.screen_draw.position.x
        self.rect.y = self.screen_draw.position.y
