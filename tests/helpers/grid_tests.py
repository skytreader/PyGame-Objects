#! usr/bin/env python

from ...helpers.grid import QuadraticGrid

import random
import unittest

class QuadraticGrid_Tests(unittest.TestCase):
	
	def __all_in(self, l1, l2):
		"""
		Tests if l1 and l2 represent equal sets, regardless of
		the order of items.
		"""
		
		if len(l1) != len(l2):
			return False
		
		while len(l1):
			item = l1.pop()
			
			if item not in l2:
				return False
			
			l2.remove(item)
		
		return len(l1) == len(l2) == 0
	
	def test_adjacent_list(self):
		one_row = QuadraticGrid(5, 1)
		adj = one_row.get_adjacent(0, 0)
		self.assertTrue(self.__all_in(adj, [(0, 1)]))
		adj = one_row.get_adjacent(0, 3)
		self.assertTrue(self.__all_in(adj, [(0, 2), (0, 4)]))
		adj = one_row.get_adjacent(0, 4)
		self.assertTrue(self.__all_in(adj, [(0, 3)]))
		
		one_col = QuadraticGrid(1, 5)
		adj = one_col.get_adjacent(0, 0)
		self.assertTrue(self.__all_in(adj, [(1, 0)]));
		adj = one_col.get_adjacent(3, 0)
		self.assertTrue(self.__all_in(adj, [(2, 0), (4, 0)]))
		adj = one_col.get_adjacent(4, 0)
		self.assertTrue(self.__all_in(adj, [(3, 0)]))
		
		matrix = QuadraticGrid(3, 4)
		adj = matrix.get_adjacent(0, 0)
		self.assertTrue(self.__all_in(adj, [(0, 1), (1, 0), (1, 1)]))
		adj = matrix.get_adjacent(0, 2)
		self.assertTrue(self.__all_in(adj, [(0, 1), (1, 1), (1, 2)]))
		adj = matrix.get_adjacent(3, 0)
		self.assertTrue(self.__all_in(adj, [(2, 0), (2, 1), (3, 1)]))
		adj = matrix.get_adjacent(3, 2)
		self.assertTrue(self.__all_in(adj, [(3, 1), (2, 1), (2, 2)]))
		adj = matrix.get_adjacent(2, 1)
		self.assertTrue(self.__all_in(adj, [(2, 0), (2, 2), (1, 0), (1, 1), (1, 2), (3, 0), (3, 1), (3, 2)]))
		
		self.assertRaises(IndexError, matrix.get_adjacent, 10, 10)
		self.assertRaises(TypeError, matrix.get_adjacent, 0.0, "zero")
	
	def test_all_in(self):
		l1 = [1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7, 9, 3, 2, 3, 8, 4, 6, 2, 6, 4, 3, 3, 8, 3, 2, 7, 9, 5, 0, 2, 8, 8, 1, 1, 9, 7, 1, 6, 9]
		l2 = [l1[i] for i in range(len(l1))]
		random.shuffle(l2)
		
		self.assertFalse(l1 == l2)
		self.assertTrue(self.__all_in(l1, l2))
		

if __name__ == "__main__":
	tests = unittest.TestLoader().loadTestsFromTestCase(QuadraticGrid_Tests)
	unittest.TextTestRunner(verbosity=2).run(tests)
