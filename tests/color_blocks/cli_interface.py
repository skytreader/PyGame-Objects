#! usr/bin/env python

from color_blocks_model import ColorBlocksModel

game = ColorBlocksModel(8, 8)

while True:
	print str(game)
	tuple_toggle = input("toggle>")
	game.toggle(tuple_toggle[0], tuple_toggle[1])
