from drawable import Drawable

import pygame

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
        size = Button.DEFAULT_FONT.size(label)
        super(Button, self).__init__(
            position, size[1] + Button.VPADDING, size[0] + Button.HPADDING
        )

    @property
    def action(self):
        return self.__action

    @action.setter
    def action(self, handler):
        self.__action = handler

    def draw(self, window, screen, **kwargs):
        pygame.draw.rect(window, self.color, (self.position[1], self.position[0], self.max_size[0], self.max_size[1]))
