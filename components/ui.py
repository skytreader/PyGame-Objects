from drawable import Drawable

class Button(Drawable):

    DEFAULT_FONT = pygame.font.Font(None, 24)

    def __init__(self, label, color, position, draw_offset, label_font=None):
        self.label = label
        self.color = color
        self.position = position
        self.__action = lambda event: pass

    @property
    def action(self):
        return self.__action

    @action.setter
    def action(self, handler):
        self.__action = handler

    def draw(self, window, screen, **kwargs):
        pass
