from components.helpers.grid import QuadraticGrid

class Snake(object):
    
    def __init__(self, size):
        self.size = size

class GameModel(object):
    
    DEFAULT_SNAKE_SIZE = 3
    
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

        At any given time, the length of this list cannot be greater than the
        size of the snake.
        """
        self.snake_joints = []
        # The location of the snake's head.
        self.snake_head = None

    def initialize(self):
        # Relies on Python 2.x division behavior.
        row = len(self.grid_size[0]) / 2
        col = len(self.grid_size[1]) / 2
        self.snake_head = (row, col)
        self.snake_joints.append((row, col - self.snake.size))

    def move_snake(self, direction):
        movector = QuadraticGrid.Movements.MOVEMAP.get(direction)
        if movector is None:
            raise ValueError("Invalid direction input %s." % direction)

        current_direction = QuadraticGrid.Movements.compute_direction(
          self.snake_joints[0], self.snake_head
        )
        inverse_direction = QuadraticGrid.Movements.INVERSE_DIRECTION[current_direction]

        if movector == inverse_direction:
            return

        self.snake_joints.insert(0, self.snake_head)
        self.snake_head = (self.snake_head[0] + movector[0], self.snake_head[1] + movector[1])

        snake_tail_vector = QuadraticGrid.Movements.compute_direction(
          self.snake_joints[-1], self.snake_joints[-2]
        )

        self.snake_joints[-1] = (self.snake_joints[-1][0] + snake_tail_vector[0],
          self.snake_joints[-1][1] + snake_tail_vector[1])
