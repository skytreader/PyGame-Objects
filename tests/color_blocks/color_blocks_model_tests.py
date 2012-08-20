#! usr/bin/env python

from color_blocks_model import ColorBlocksModel

import unittest

class color_blocks_model_tests(unittest.TestCase):
	
	def setUp(self):
		self.width = 3
		self.height = 4
		self.color_game = ColorBlocksModel(self.height, self.width)
	
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
				self.color_game.grid[i][j]
	
	def test_game_instance(self):
		game_grid = self.color_game.grid
		self.assertEqual(self.height, len(game_grid))
		self.assertEqual(self.width, len(game_grid[0]))

if __name__ == "__main__":
	tests = unittest.TestLoader().loadTestsFromTestCase(color_blocks_model_tests)
	unittest.TextTestRunner(verbosity=2).run(tests)
