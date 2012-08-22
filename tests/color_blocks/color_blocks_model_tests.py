#! usr/bin/env python

from color_blocks_model import ColorBlocksModel

import unittest

class color_blocks_model_tests(unittest.TestCase):
	
	def setUp(self):
		"""
		Note that this results to a random configuration for every test!
		"""
		self.width = 8
		self.height = 8
		self.color_game = ColorBlocksModel(self.width, self.height)
	
	def __modify_model_grid(self, grid):
		"""
		Changes the grid contained in the model self.color_game. The
		only constraint is that the new grid should be the same
		size as the old grid.
		"""
		height = len(grid)
		width = len(grid[0])
		
		for i in range(height):
			for j in range(width):
				self.color_game.grid[i][j] = grid[i][j]
	
	def test_game_instance(self):
		game_grid = self.color_game.grid
		self.assertEqual(self.height, len(game_grid))
		self.assertEqual(self.width, len(game_grid[0]))
	
	def test_modify_model_grid(self):
		game_grid = [[1 for i in range(self.width)] for j in range(self.height)]
		game_grid[1][1:3] = [0,0]
		game_grid[2][1:3] = [0,0]
		self.__modify_model_grid(game_grid)
		
		self.assertEqual(self.color_game.grid, game_grid)
	
	def test_toggle(self):
		game_grid = [[1 for i in range(self.width)] for j in range(self.height)]
		game_grid[1][1:3] = [0,0]
		game_grid[2][1:3] = [0,0]
		self.__modify_model_grid(game_grid)
		#game.grid = game_grid
		points = self.color_game.toggle(1, 1)
		game_grid[1][1:3] = ColorBlocksModel.UNTAKEN * 2
		game_grid[2][1:3] = ColorBlocksModel.UNTAKEN * 2
		
		self.assertEqual(points, 4)
		self.assertEqual(self.color_game.grid, game_grid)
	
	def test_collapse(self):
		test_game = [[1 for i in range(self.width)] for i in range(self.height)]
		self.__modify_model_grid(test_game)
		row_limit = len(self.color_game.grid)
		col_limit = len(self.color_game.grid[0])
		
		for i in range(row_limit):
			self.color_game.grid[i][3] = ColorBlocksModel.UNTAKEN
		
		self.color_game.collapse()
		
		for i in range(row_limit):
			test_game[i][col_limit - 1] = ColorBlocksModel.UNTAKEN
		
		self.assertEqual(self.color_game.grid, test_game)

if __name__ == "__main__":
	tests = unittest.TestLoader().loadTestsFromTestCase(color_blocks_model_tests)
	unittest.TextTestRunner(verbosity=2).run(tests)
