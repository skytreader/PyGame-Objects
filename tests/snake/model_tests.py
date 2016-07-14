import unittest

from demo.snake.model import GameModel

class SnakeModelTests(unittest.TestCase):
    
    def setUp(self):
        self.gm = GameModel(10, 10)
        self.gm.initialize()
    
    def test_constructor_exception(self):
        self.assertRaises(ValueError, GameModel, 0, 0)
        self.assertRaises(ValueError, GameModel, GameModel.DEFAULT_SNAKE_SIZE,
          GameModel.DEFAULT_SNAKE_SIZE)
        less1 = GameModel.DEFAULT_SNAKE_SIZE
        self.assertRaises(ValueError, GameModel, less1, less1)
        self.assertRaises(ValueError, GameModel, -1, -1)

    def test_constructor_happy(self):
        gm = GameModel(4, 4)
        self.assertTrue(gm.snake is not None)

    def test_move_snake_exceptions(self):
        self.assertRaises(ValueError, self.gm.move_snake, "a")

    def test_move_snake(self):
        _snake_head = self.gm.snake_head
        self.gm.move_snake("u")
        self.assertEqual((_snake_head[0]-1, _snake_head[1]), self.gm.snake_head)
        self.assertTrue(_snake_head in self.gm.snake_joints)

        _snake_head = self.gm.snake_head
        self.gm.move_snake("r")
        self.assertEqual((_snake_head[0], _snake_head[1]+1), self.gm.snake_head)

        _snake_head = self.gm.snake_head
        self.gm.move_snake("u")
        self.assertEqual((_snake_head[0]-1, _snake_head[1]), self.gm.snake_head)

        _snake_head = self.gm.snake_head
        self.gm.move_snake("l")
        self.assertEqual((_snake_head[0], _snake_head[1]-1), self.gm.snake_head)

        _snake_head = self.gm.snake_head
        self.gm.move_snake("l")
        self.assertEqual((_snake_head[0], _snake_head[1]-1), self.gm.snake_head)

        _snake_head = self.gm.snake_head
        self.gm.move_snake("d")
        self.assertEqual((_snake_head[0]+1, _snake_head[1]), self.gm.snake_head)
