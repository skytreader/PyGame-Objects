#! usr/bin/env python

from ...helpers.grid import QuadraticGrid

import random

class ColorBlocksModel(object):
	"""
	A Color Blocks game will be represented by an n x m grid. Each cell
	will be represented by a character in ColorBlocksModel.BLOCKS . Since,
	when collapsing blocks, it will happen that the overall grid becomes
	less than the original, removed blocks will be represented by
	ColorBlocksModel.UNTAKEN .
	"""
	
	BLOCKS = "01234"
	UNTAKEN = "."
	
	def __init__(self, grid_width, grid_height, min_score = 1):
		"""
		Initializes a Color Blocks game with the given parameters
		
		@param grid_width
		@param grid_height
		@param min_score
		  The minimum number of blocks required to make a score.
		"""
		untaken = ColorBlocksModel.UNTAKEN
		self.__quadratic_grid = QuadraticGrid(grid_width, grid_height, True, False)
		self.__populate()
		self.__min_score = min_score
		self.__score = 0
	
	@property
	def grid(self):
		return self.__quadratic_grid.grid
	
	@property
	def quadratic_grid(self):
		return self.__quadratic_grid
	
	@property
	def min_score(self):
		return self.__min_score
	
	@min_score.setter
	def min_score(self, min_score):
		self.__min_score = min_score
	
	@property
	def score(self):
		return self.__score
	
	@score.setter
	def score(self, score):
		self.__score = score
	
	def __populate(self):
		height = len(self.grid)
		width = len(self.grid[0])
		block_index_max = len(ColorBlocksModel.BLOCKS) - 1
		
		for i in range(height):
			for j in range(width):
				block = ColorBlocksModel.BLOCKS[random.randint(0, block_index_max)]
				self.grid[i][j] = block
	
	def toggle(self, row, col):
		"""
		Removes the block at position (row, col) and all adjacent blocks of
		the same color.
		
		Returns the number of blocks removed from the grid.
		
		@param row
		  The row index of the block to be toggled.
		@param col
		  The column index of the block to be toggled.
		@return The number of blocks removed from the grid or false if the block
		indicated is untaken.
		"""
		points = 0
		original = self.grid[row][col]
		
		if original == ColorBlocksModel.UNTAKEN:
			return False
		
		adjacent_stack = [(row, col)]
		adj_same_color = []
		inspected = []
		
		while len(adjacent_stack):
			cur_block = adjacent_stack.pop()
			inspected.append(cur_block)
			adj_same_color.append(cur_block)
			adjacent_blocks = self.quadratic_grid.get_adjacent(cur_block[0], cur_block[1])
			adj_count = len(adjacent_blocks)
			
			for i in range(adj_count):
				block = adjacent_blocks[i]
				if self.grid[block[0]][block[1]] == original and \
				  block not in adjacent_stack and block not in inspected:
					adjacent_stack.append(adjacent_blocks[i])
		
		if len(adj_same_color) >= self.min_score:
			for cur_block in adj_same_color:
				self.grid[cur_block[0]][cur_block[1]] = ColorBlocksModel.UNTAKEN
				points += 1
		
		return points
	
	def __find_empty_column(self):
		"""
		Looks for empty columns in the grid. Returns the index of an
		empty column. If there are multiple empty columns, only the
		first one is returned. If there are no empty columns in the
		grid, the value -1 is returned.
		"""
		col_limit = len(self.grid[0])
		row_limit = len(self.grid)
		
		for col in range(col_limit):
			if self.__is_empty_col(col):
				return col
		
		return -1
	
	def __is_empty_col(self, col_index):
		"""
		Checks whether the column described by col_index is empty.
		"""
		for row in self.grid:
			if row[col_index] != ColorBlocksModel.UNTAKEN:
				return False
		
		return True
	
	def __find_empty_column_block(self, start_index):
		"""
		Returns a tuple indicating the start and end of an empty column
		block. start_index is the index in which we start searching.
		
		Assume start_index is an empty column already (for sure!)
		
		Yes, if there is only one empty column, the return tuple will
		be (start_index, start_index)
		"""
		empty_range = [start_index, None]
		limit = len(self.grid[0])
		col_index = start_index + 1
		
		while col_index < limit:
			if not self.__is_empty_col(col_index):
				break
			
			col_index += 1
		
		empty_range[1] = col_index - 1
		
		return tuple(empty_range)
	
	def __translate_empty_block(self, col_index, block_length):
		"""
		Performs the actual collapsing of an empty column block.
		
		@param col_index
		  The upper bound of the range of empty columns which we are
		  collapsing.
		@param block_length
		  The length of the empty column block.
		"""
		limit = len(self.grid[0])
		
		for row in self.grid:
			non_empty = col_index + 1
			
			while non_empty < limit:
				row[non_empty - block_length] = row[non_empty]
				non_empty += 1
	
	def __untake_last_block(self, block_length):
		limit = len(self.grid[0])
		last_block_start = limit - block_length
		
		for row in self.grid:
			cell_index = last_block_start
			
			while cell_index < limit:
				row[cell_index] = ColorBlocksModel.UNTAKEN
				cell_index += 1
	
	def collapse(self):
		"""
		Removes empty columns by "collapsing" the space left.
		"""
		empty_col = self.__find_empty_column()
		
		empty_block = self.__find_empty_column_block(empty_col)
		block_length = empty_block[1] - empty_block[0] + 1
		self.__translate_empty_block(empty_block[1], block_length)
		self.__untake_last_block(block_length)
	
	def falldown(self):
		"""
		Scans each column of the grid and looks for unsupported (i.e.,
		UNTAKEN cells below) blocks and makes them "fall down".
		"""
		col_limit = len(self.grid[0])
		row_limit = len(self.grid)
		
		for col in range(col_limit):
			row = row_limit - 1
			
			while i >= 0:
				if not self.__is_empty_col(col) and self.grid[row][col] == ColorBlocksModel.UNTAKEN:
					self.__fall_col(col)
					row_runner = row - 1
					
					while row_runner >= 0:
						if self.grid[row_runner][col] != ColorBlocksModel.UNTAKEN:
							# Move everything!
							skip = row - row_runner
							fall = row_runnerd
							
							while fall >= 0 and self.grid[fall][col] != ColorBlocksModel.UNTAKEN:
								self.grid[fall + 3][col] = self.grid[fall][col]
								self.grid[fall][col] = ColorBlocksModel.UNTAKEN
							
							break
						else:
							row_runner -= 1
				
				i -= 1
	
	def __str__(self):
		board = ""
		height = len(self.grid)
		
		for i in range(height):
			board += str(self.grid[i]) + "\n"
		
		return board
