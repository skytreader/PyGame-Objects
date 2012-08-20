#! usr/bin/env python

from ...helpers.grid import QuadraticGrid

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
		adj0 = one_row.get_adjacent(0, 0)
		print adj0
		self.assertTrue(self.__all_in(adj0, [(0, 1)]))

if __name__ == "__main__":
	tests = unittest.TestLoader().loadTestsFromTestCase(QuadraticGrid_Tests)
	unittest.TextTestRunner(verbosity=2).run(tests)
