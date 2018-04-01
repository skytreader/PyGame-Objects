from __future__ import division
from __future__ import print_function

from components.core import Colors
from drawable import Drawable

import pygame
import sys

class UnsupportedEventException(Exception):

    def __init__(self, event):
        message = "%s is not supported by this CommonUI object." % event
        super(UnsupportedEventException, self).__init__(message)

class CommonUI(Drawable):
    """
    CommonUI objects are Drawables that come with a declaration of intent: this
    Drawable _interacts_ with the user by default, through a set of
    _pre-determined_ events. However, a limitation is that a CommonUI object can
    only specify one event handler for any event it mightbe listening to.
    """

    def __init__(self, draw_offset, width_limit=None, height_limit=None):
        super(CommonUI, self).__init__(draw_offset, width_limit, height_limit)
        # Mapping of events to handler functions. Subclasses should prefill this
        # dictionary with the events they expect to handle, maybe using
        # `dummy_event_handler` as a placeholder. NOTE: Do **not** use `None` as
        # a placeholder for events you expect to handle.
        self._event_handlers = {}

    # TODO Make this a staticmethod instead.
    def dummy_event_handler(self, event):
        """
        Note that this makes it so that a CommonUI instance "unlistens" to an
        event it is supposed to be listening to (largely because, if it responds
        to said event with this handler, the user will not see anything happen.
        """
        pass

    def set_event_handler(self, event, handler):
        """
        Classes that use CommonUI objects should use this method to specify
        event handlers for whatever events are supported by this object. This
        method throws an UnsupportedEventException in case an event which is not
        handled is specified.
        """
        _handler = self._event_handlers.get(event.type)
        if _handler:
            self._event_handlers[event.type] = handler
        else:
            raise UnsupportedEventException(event)

class Button(CommonUI):

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
        # TODO Handle labels that are too long.
        if pygame.font.get_init():
            size = Button.DEFAULT_FONT.size(label)
        else:
            size = (0, 0)
            print("pygame.font not initialized for Button construction.", file=sys.stderr)

        super(Button, self).__init__(
            position, size[0] + Button.HPADDING, size[1] + Button.VPADDING
        )

        mouseclick_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN)
        self._event_handlers[mouseclick_event.type] = self.dummy_event_handler

    def draw(self, window, screen, **kwargs):
        pygame.draw.rect(window, self.color, (self.position[1], self.position[0], self.max_size[0], self.max_size[1]))
        if pygame.font.get_init():
            button_label = Button.DEFAULT_FONT.render(self.label, True, Colors.MAX_BLACK)
            window.blit(button_label, (self.position[1] + int(Button.HPADDING / 2), self.position[0] + int(Button.VPADDING / 2)))
        else:
            print("pygame.font not initialized for Button draw.", file=sys.stderr)
