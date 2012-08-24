#! usr/bin/env python

from color_blocks_model import ColorBlocksModel

game = ColorBlocksModel(9, 9)

while True:
	print str(game)
	tuple_toggle = input("toggle>")
	game.score += game.toggle(tuple_toggle[0], tuple_toggle[1])
	game.falldown()
	game.collapse()
	print "Score: " + str(game.score)
