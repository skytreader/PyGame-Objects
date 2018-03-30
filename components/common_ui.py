from __future__ import division
from __future__ import print_function

from components.core import Colors
from drawable import Drawable

import pygame
import sys

class Button(Drawable):

    DEFAULT_FONT = pygame.font.Font(None, 24)
    VPADDING = 18
    HPADDING = 18

    def __init__(self, label, color, position, label_font=None):
        """
        Draws a rectangular button.

        position is the position of the upper-left corner of the button.
        """
        self.label = label
        self.color = color
        self.position = position
        self.__action = lambda event: event
        # TODO Handle labels that are too long.
        if pygame.font.get_init():
            size = Button.DEFAULT_FONT.size(label)
        else:
            size = (0, 0)
            print("pygame.font not initialized for Button construction.", file=sys.stderr)

        super(Button, self).__init__(
            position, size[0] + Button.HPADDING, size[1] + Button.VPADDING
        )

    @property
    def action(self):
        return self.__action

    @action.setter
    def action(self, handler):
        self.__action = handler

    def draw(self, window, screen, **kwargs):
        pygame.draw.rect(window, self.color, (self.position[1], self.position[0], self.max_size[0], self.max_size[1]))
        if pygame.font.get_init():
            button_label = Button.DEFAULT_FONT.render(self.label, True, Colors.MAX_BLACK)
            window.blit(button_label, (self.position[1] + int(Button.HPADDING / 2), self.position[0] + int(Button.VPADDING / 2)))
        else:
            print("pygame.font not initialized for Button draw.", file=sys.stderr)
