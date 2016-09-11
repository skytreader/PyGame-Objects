from __future__ import division

from components.core import GameModel
from components.framework_exceptions import VectorDirectionException
from components.helpers.grid import QuadraticGrid

import random

class Snake(object):
    
    def __init__(self):
        self.head = None
        """
        Sorted (row, col) tuples of the snake joints. Notice that joints can
        only be made from the snake's head and can only disappear from the
        snake's tail. The current location of the head is not considered a joint
        but the tail is.

        At any given time, the length of this list cannot be greater than the
        size of the snake.

        By convention, the first element of this list is the joint closest to
        the head of the snake.
        """
        self.joints = []

    def enumerate_snake_squares(self):
        """
        Returns a set of tuples indicating the squares the snake is occupying.
        This does not take into account the grid in which the snake is moving.
        """
        snake_squares = set()
        c_origin = self.head
        snake_squares.add(self.head)

        for c_end in self.joints:
            c_direction = QuadraticGrid.Movements.compute_direction(c_origin, c_end)
            square = (c_origin[0] + c_direction[0], c_origin[1] + c_direction[1])
            snake_squares.add(square)

            while square != c_end:
                square = (square[0] + c_direction[0], square[1] + c_direction[1])
                snake_squares.add(square)

            c_origin = c_end

        return snake_squares

    def grow(self):
        current_tail = None
        if len(self.joints) == 1:
            current_tail = (self.head, self.joints[0])
        else:
            current_tail = (self.joints[-2], self.joints[-1])

        direction = QuadraticGrid.Movements.compute_direction(current_tail[0], current_tail[1])
        new_tail_location = (self.joints[-1][0] + direction[0],
          self.joints[-1][1] + direction[1])
        self.joints[-1] = new_tail_location

class SnakeGameModel(GameModel):
    
    DEFAULT_SNAKE_SIZE = 3
    
    def __init__(self, width, height):
        super(SnakeGameModel, self).__init__()
        if width < (SnakeGameModel.DEFAULT_SNAKE_SIZE + 1) or height < (SnakeGameModel.DEFAULT_SNAKE_SIZE):
            raise ValueError("Please give enough room for the snake to move")

        self.width = width
        self.height = height
        self.snake = Snake()
        self.food_point = None
        self.last_move_reversible = False
        self.last_tail = None
        self.endgame = False

    def is_endgame(self):
        return self.endgame

    @property
    def snake_joints(self):
        return self.snake.joints

    @property
    def snake_head(self):
        return self.snake.head

    def initialize(self):
        row = self.height / 2
        col = self.width / 2
        self.snake.head = (row, col)
        self.snake_joints.append((row, col - SnakeGameModel.DEFAULT_SNAKE_SIZE))
        self.__generate_food_point()

    def __generate_food_point(self):
        self.food_point = (random.randint(0, self.height - 1), random.randint(0, self.width - 1))

    def move_snake(self, direction, reversible=False):
        movector = direction
        if movector is None:
            raise ValueError("Invalid direction input %s." % direction)

        current_direction = QuadraticGrid.Movements.compute_direction(
          self.snake_joints[0], self.snake_head
        )
        inverse_direction = None
        try:
            inverse_direction = QuadraticGrid.Movements.INVERSE_DIRECTION[current_direction]
        except KeyError:
            self.endgame = True

        if movector == inverse_direction and not self.last_move_reversible:
            raise VectorDirectionException("Impossible to reverse last movement.")

        if movector == inverse_direction and self.last_move_reversible:
            self.snake.joints.append(self.last_tail)

        if movector != inverse_direction:
            self.snake_joints.insert(0, self.snake_head)

        self.snake.head = (self.snake_head[0] + movector[0], self.snake_head[1] + movector[1])

        if self.snake.head == self.food_point:
            self.snake.grow()
            self.__generate_food_point()

        self.last_tail = self.snake_joints[-1]

        if movector != inverse_direction:
            snake_tail_vector = QuadraticGrid.Movements.compute_direction(
              self.snake_joints[-1], self.snake_joints[-2]
            )

            self.snake_joints[-1] = (self.snake_joints[-1][0] + snake_tail_vector[0],
              self.snake_joints[-1][1] + snake_tail_vector[1])

        if self.snake_joints[-1] == self.snake_joints[-2]:
            self.snake_joints.pop()

        self.last_move_reversible = reversible
    
    def collides_with_self(self):
        return self.snake_head in self.snake.enumerate_snake_squares()

    def render(self, **kwargs):
        pass
