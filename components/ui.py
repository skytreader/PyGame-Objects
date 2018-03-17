from drawable import Drawable

class Button(Drawable):

    def __init__(self, label, color, position):
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
