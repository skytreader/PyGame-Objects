import random

class Snake(object):
    
    def __init__(self, size):
        self.size = size

class GameModel(object):
    
    DEFAULT_SNAKE_SIZE = 3
    SNAKE_MOVEMENTS = set(("u", "d", "l", "r"))
    
    def __init__(self, width, height):
        if width < (GameModel.DEFAULT_SNAKE_SIZE + 1) or height < (GameModel.DEFAULT_SNAKE_SIZE):
            raise ValueError("Please give enough room for the snake to move")

        self.grid_size = [[False for _ in range(width)] for __ in range(height)]
        self.snake = Snake(GameModel.DEFAULT_SNAKE_SIZE)
        """
        Sorted (row, col) tuples of the snake joints. Notice that joints can
        only be made from the snake's head and can only disappear from the
        snake's tail. The current location of the head is not considered a joint
        but the tail is.
        """
        self.snake_joints = []
        # The location of the snake's head.
        self.snake_head = None

    def initialize(self):
        # Relies on Python 2.x division behavior.
        row = len(self.grid_size[0]) / 2
        col = len(self.grid_size[1]) / 2
        self.snake_head = (row, col)
        self.snake_joints.append((row, col + self.snake.size))

    def move_snake(self, direction):
        if direction not in GameModel.SNAKE_MOVEMENTS:
            raise ValueError("Please see GameModel.SNAKE_MOVEMENTS for possible values")

        new_vector_head = self.snake_head
        self.snake_joints.insert(0, self.snake_head)
