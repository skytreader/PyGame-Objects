#! usr/bin/env python

from color_blocks_model import ColorBlocksModel

import unittest

class color_blocks_model_tests(unittest.TestCase):
	
	def setUp(self):
		"""
		Note that this results to a random configuration for every test!
		"""
		self.width = 9
		self.height = 9
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
	
	def __collapse(self, untake_ranges):
		"""
		Auto script for collapse unit tests that will actually collapse.
		
		Specify the (continuous) columns to untake as ranges (i.e., untake_ranges
		is a list-of-lists).
		"""
		for r in untake_ranges:
			self.__range_col_untake(r)
		
		test_game = [list(self.color_game.grid[row]) for row in range(self.height)]
		
		# "Collapse" board out-of-place
		collapsed = [[] for row in self.color_game.grid]
		
		self.color_game.collapse()
		self.assertNotEqual(test_game, self.color_game.grid)
		
		for col_index in range(self.width):
			if not self.__is_untaken(test_game, col_index):
				row_counter = 0
				
				for row in collapsed:
					row.append(test_game[row_counter][col_index])
					row_counter += 1
		
		# Pad collapsed with untaken cols
		for row in collapsed:
			row.extend([ColorBlocksModel.UNTAKEN for i in range(self.width - len(row))])
		
		# Collapse color_game
		self.assertEqual(collapsed, self.color_game.grid)
	
	def __is_untaken(self, board, col_index):
		for row in board:
			if row[col_index] != ColorBlocksModel.UNTAKEN:
				return False
		
		return True
	
	def __range_col_untake(self, untake_range):
		"""
		Untakes whole columns. The columns should be consecutive and specified
		as an inclusive range.
		
		untake_range is an iterable with at least two items. The first item is the
		low bound of the range while the second one is the high bound of the range.
		"""
		col = untake_range[0]
		
		while col <= untake_range[1]:
			for row in self.color_game.grid:
				row[col] = ColorBlocksModel.UNTAKEN
			
			col += 1
	
	def test_collapse(self):
		self.__collapse([(3, 3)])
		self.setUp()
		self.__collapse([(3, 4)])
	
	def __col_untake(self, col, row):
		"""
		Untakes the cells in index col, for every row as specified in
		iterable row.
		"""
		for r in row:
			self.color_game.grid[r][col] = ColorBlocksModel.UNTAKEN
	
	def test_falldown(self):
		limit = len(self.color_game.grid)
		rlimit = range(limit)
		test_board = [list(self.color_game.grid[i]) for i in rlimit]
		
		untake_list = [6, 7, 8]
		untake_col = 3
		
		self.__col_untake(untake_col, untake_list)
		self.color_game.falldown()
		
		trans_block = range(6)
		trans_block.reverse()
		
		for block in trans_block:
			test_board[block + 3][untake_col] = test_board[block][untake_col]
		
		for untake_row in range(len(untake_list)):
			test_board[untake_row][untake_col] = ColorBlocksModel.UNTAKEN
		
		self.assertEqual(self.color_game.grid, test_board)
		
		self.setUp()
		
		test_board = [list(self.color_game.grid[i]) for i in rlimit]
		untake_list = [6, 7, 8, 0, 1, 2]
		self.__col_untake(untake_col, untake_list)
		self.color_game.falldown()
		
		for block in [5, 4, 3]:
			test_board[block + 3][untake_col] = test_board[block][untake_col]
		
		for untake_row in range(len(untake_list)):
			test_board[untake_row][untake_col] = ColorBlocksModel.UNTAKEN
		
		self.assertEqual(test_board, self.color_game.grid)

if __name__ == "__main__":
	tests = unittest.TestLoader().loadTestsFromTestCase(color_blocks_model_tests)
	unittest.TextTestRunner(verbosity=2).run(tests)
