import unittest

from components.framework_exceptions import VectorDirectionException
from components.helpers.grid import QuadraticGrid

from demo.snake.model import SnakeGameModel, Snake

class SnakeModelTests(unittest.TestCase):
    
    def setUp(self):
        self.gm = SnakeGameModel(10, 10)
        self.gm.initialize()

    def test_init(self):
        snake_head = self.gm.snake_head
        self.assertEqual(1, len(self.gm.snake_joints))
        tail = self.gm.snake_joints[0]
        self.assertEqual(tail[0], snake_head[0])
        self.assertNotEqual(tail[1], snake_head[1])
        self.assertTrue(self.gm.snake_head is not None)
    
    def test_constructor_exception(self):
        self.assertRaises(ValueError, SnakeGameModel, 0, 0)
        self.assertRaises(ValueError, SnakeGameModel, SnakeGameModel.DEFAULT_SNAKE_SIZE,
          SnakeGameModel.DEFAULT_SNAKE_SIZE)
        less1 = SnakeGameModel.DEFAULT_SNAKE_SIZE - 1
        self.assertRaises(ValueError, SnakeGameModel, less1, less1)
        self.assertRaises(ValueError, SnakeGameModel, -1, -1)

    def test_constructor_happy(self):
        gm = SnakeGameModel(4, 4)
        self.assertTrue(gm.snake is not None)

    def test_move_snake(self):
        _snake_head = self.gm.snake_head
        self.gm.move_snake(QuadraticGrid.Movements.UP)
        self.assertEqual((_snake_head[0]-1, _snake_head[1]), self.gm.snake_head)
        self.assertTrue(_snake_head in self.gm.snake_joints)

        _snake_head = self.gm.snake_head
        self.gm.move_snake(QuadraticGrid.Movements.RIGHT)
        self.assertEqual((_snake_head[0], _snake_head[1]+1), self.gm.snake_head)

        _snake_head = self.gm.snake_head
        self.gm.move_snake(QuadraticGrid.Movements.UP)
        self.assertEqual((_snake_head[0]-1, _snake_head[1]), self.gm.snake_head)

        _snake_head = self.gm.snake_head
        self.gm.move_snake(QuadraticGrid.Movements.LEFT)
        self.assertEqual((_snake_head[0], _snake_head[1]-1), self.gm.snake_head)

        _snake_head = self.gm.snake_head
        self.gm.move_snake(QuadraticGrid.Movements.LEFT)
        self.assertEqual((_snake_head[0], _snake_head[1]-1), self.gm.snake_head)

        _snake_head = self.gm.snake_head
        self.gm.move_snake(QuadraticGrid.Movements.DOWN)
        self.assertEqual((_snake_head[0]+1, _snake_head[1]), self.gm.snake_head)

    def test_keep_moving_right(self):
        tail = self.gm.snake_joints[-1]
        self.gm.move_snake(QuadraticGrid.Movements.RIGHT)
        self.assertEqual(self.gm.snake_joints[-1], (tail[0], tail[1] + 1))

        tail = self.gm.snake_joints[-1]
        self.gm.move_snake(QuadraticGrid.Movements.RIGHT)
        self.assertEqual(self.gm.snake_joints[-1], (tail[0], tail[1] + 1))

    def test_no_180_turn(self):
        """
        The snake is initially oriented facing rightwards. Test that, from that
        position, it can't suddenly go leftwards.
        """
        head = self.gm.snake_head
        self.assertRaises(VectorDirectionException, self.gm.move_snake, QuadraticGrid.Movements.LEFT)
        self.assertEqual(head, self.gm.snake_head)

    def test_reversible(self):
        original_head = self.gm.snake_head
        original_joints = self.gm.snake_joints
        original_squares = self.gm.snake.enumerate_snake_squares()
        self.gm.move_snake(QuadraticGrid.Movements.RIGHT, True)
        self.gm.move_snake(QuadraticGrid.Movements.LEFT)
        self.assertEqual(original_head, self.gm.snake_head)
        self.assertEqual(original_joints, self.gm.snake_joints)
        self.assertEqual(original_squares, self.gm.snake.enumerate_snake_squares())

    def test_bending(self):
        snake_head = self.gm.snake_head
        max_len = SnakeGameModel.DEFAULT_SNAKE_SIZE
        old_len = len(self.gm.snake_joints)
        old_tail = self.gm.snake_joints[-1]
        self.assertTrue(max_len >= old_len)
        self.gm.move_snake(QuadraticGrid.Movements.UP)
        self.assertTrue(len(self.gm.snake_joints) > old_len)
        self.assertTrue(max_len >= len(self.gm.snake_joints))
        self.assertEqual(self.gm.snake_joints[-1], (old_tail[0], old_tail[1] + 1))

    def test_enumerate_snake_squares(self):
        snake = Snake()
        snake.head = (6, 7)
        snake.joints = [(6, 4), (3, 4), (3, 3), (8, 3), (8, 0), (0, 0)]
        expected_squares = set()
        expected_squares.add((6, 7))

        for r in range(8):
            expected_squares.add((r, 0))

        for c in range(3):
            expected_squares.add((8, c))

        for r in range(3, 9):
            expected_squares.add((r, 3))

        for r in range(3, 7):
            expected_squares.add((r, 4))

        for c in range(4, 7):
            expected_squares.add((6, c))

        self.assertEquals(expected_squares, snake.enumerate_snake_squares())
