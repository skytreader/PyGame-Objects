#! usr/bin/env python
from __future__ import division

from components.core import Colors, GameScreen
from components.drawable import Drawable
from components.framework_exceptions import VectorDirectionException

import math
import pygame

"""
This file contains models for grids.
"""

class DimensionException(Exception):
    """
    Use this exception when indicating wrong dimensions for grids (i.e., if you
    set a minimum/maximum dimensions for your grids).
    """
    pass

class BorderProperties(object):

    def __init__(self, color=Colors.MAX_BLACK, thickness=1):
        self.color = color
        self.thickness = thickness

class Grid(Drawable):
    """
    A grid must be drawable (and traversable)!
    """
    
    def __init__(self, draw_width=-1, draw_height=-1, draw_offset=None):
        super(Grid, self).__init__(draw_offset)
    
    def traverse(self):
        """
        TODO: What happens here? :\
        """
        pass

class QuadraticGrid(Grid):
    """
    AKA 2D Cartesian Grid. A QuadraticGrid may hold some data in its cells (for
    instance, information on how to render a given cell) through its `grid`
    property but users of QuadraticGrid have to manually set this data for
    themselves (after instantiating a QuadraticGrid instance). By default this 
    contains integers. There is no dereferencing the `grid` property.
    """

    class Movements(object):
        UP = (-1, 0)
        DOWN = (1, 0)
        LEFT = (0, -1)
        RIGHT = (0, 1)
        STAY = (0, 0)

        """
        So that function interfaces can be consistent in this framework.
        """
        MOVEMAP = {'u': UP, 'd': DOWN, 'l': LEFT, 'r': RIGHT}

        INVERSE_MOVEMAP = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}
        KEY_TO_DIR = {pygame.K_UP: UP, pygame.K_DOWN: DOWN, pygame.K_LEFT: LEFT, pygame.K_RIGHT: RIGHT}


        @classmethod
        def compute_direction(cls, tail, head):
            """
            Compute the direction at which the vector starting at tail and ending
            at head is moving.

            Assumes that the movement described is only along the grid lines.
            """
            if tail[0] == head[0]:
                if tail[1] > head[1]:
                    return cls.LEFT
                elif tail[1] < head[1]:
                    return cls.RIGHT
                else:
                    return cls.STAY
            elif tail[1] == head[1]:
                if tail[0] > head[0]:
                    return cls.UP
                else:
                    return cls.DOWN # EQ case should've been caught above.
            else:
                raise VectorDirectionException("Given vector does not describe grid movement.")
    
    def __init__(self, grid_width, grid_height, hv_neighbors = True, diag_neighbors = True, draw_offset=None, border_properties=None):
        """
        Creates an instance of a quadratic grid.
        
        @param grid_width
        @param grid_height
        @param hv_neighbors
          If set to true, we consider the blocks above and below, left and right
          of a given block as a block's neighbors.
          
          Defaults to true.
        @param diag_neighbors
          If set to true, we consider the blocks at the upper left/right and lower
          left/right of a given block as a block's neighbors.
          
          Defaults to true.
        @param draw_offset
        @param border_properties
          A BorderProperties object that describes how the borders of the cells
          are to be drawn. A value of None (default) indicates that the cells
          should be drawn with no borders.
        """
        super(QuadraticGrid, self).__init__(draw_offset=draw_offset)
        
        if type(grid_width) != type(0) or type(grid_height) != type(0):
            raise TypeError("Grid dimensions must be specified as ints.")
        
        if grid_width <= 0 or grid_height <= 0:
            raise ValueError("Grid dimensions must be positive.")
        
        self.__grid = [[i for i in range(grid_width)] for j in range(grid_height)]
        self.hv_neighbors = hv_neighbors
        self.diag_neighbors = diag_neighbors
        self.border_properties = border_properties

    def __compute_block_dimension(self, config, dim):
        """
        Compute the given block dimension. This is affected by several variables
        in the game state. This method will take all of them into account.

        config - A GameConfig instance, the current configuration of the game.
        dim - A string, either "width" or "height", representing the dimension
        to be computed. Anything else results to a ValueError.
        """
        if dim not in ("width", "height"):
            raise ValueError("dim argument should only be either 'width' or 'height'. Given %s." % dim)

        dimdex = 0 if dim == "width" else 1
        debug_deductible = (
            GameScreen.DEBUG_SPACE_PROVISIONS
            if config.get_config_val("debug_mode") and dimdex
            else 0
        )
        deductibles = self.draw_offset[dimdex] + debug_deductible
        denominator = len(self.grid) if dimdex else len(self.grid[0])
        dimension_size = int(
            math.floor(
                (config.get_config_val("window_size")[dimdex] - deductibles) / denominator
            )
        )

        return dimension_size
    
    def draw(self, window, screen, **kwargs):
        """
        window - A Surface instance to draw on.
        screen - A GameScreen instance.
        """
        block_width = self.__compute_block_dimension(screen.config, "width")
        block_height = self.__compute_block_dimension(screen.config, "height")
        rects, renders = QuadraticGrid.cons_rect_list(
          self, screen.model, block_width, block_height, self.draw_offset
        )

        for rct, rndr in zip(rects, renders):
            pygame.draw.rect(window, rndr, rct, 0)

        # Draw the borders
        if self.border_properties:
            # There will always be n + 1 borders to be drawn on either direction
            # since we need to draw the end borders too. (Where n is the grid
            # dimension.)
            vborders_limit = len(self.grid[0]) + 1

            for vborders_offset in xrange(vborders_limit):
                vcons = block_width * vborders_offset + self.draw_offset[0]
                pygame.draw.line(
                    window, self.border_properties.color,
                    (vcons, self.draw_offset[1]), (vcons, screen.screen_size[1]),
                    self.border_properties.thickness
                )

            hborders_limit = len(self.grid[1]) + 1

            for hborders_offset in xrange(hborders_limit):
                hcons = block_height * hborders_offset + self.draw_offset[1]
                pygame.draw.line(
                    window, self.border_properties.color,
                    (self.draw_offset[0], hcons), (screen.screen_size[0], hcons),
                    self.border_properties.thickness
                )

    @property
    def grid(self):
        return self.__grid

    @staticmethod
    def cons_rect_list(grid, model, block_width, block_height, offset):
        """
        Looks like public access to this will be deprecated soon.

        grid - An instance of this class.
        model - An instance of components.core.GameModel

        Returns two parallel lists. The first list contains the dimensions of
        the rectangles in the format
            
            (upper_left_x, upper_left_y, width, height)

        while the second list contains render objects per block (i.e., it comes
        from the model given to this method).
        """
        grid = grid.grid
        rect_list = []
        render_list = []
        width_offset = offset[0]
        height_offset = offset[1]

        for i, row in enumerate(grid):
            for j, col in enumerate(row):
                upper_left_x = j * block_width + width_offset
                upper_left_y = i * block_height + height_offset
                rect = (upper_left_x, upper_left_y, block_width, block_height)
                rect_list.append(rect)

                render_list.append(model.render(row=i, col=j))

        return (rect_list, render_list)

    @staticmethod
    def make_rect(c, block_width, block_height, width_offset=0, height_offset=0):
        """
        Given a point in a grid c, create a rectangle out of it.
        """
        upper_left_x = c[1] * block_width + width_offset
        upper_left_y = c[0] * block_height + height_offset
        return (upper_left_x, upper_left_y, block_width, block_height)

    def get_clicked_cell(self, screen, pos):
        # TODO Optimize! Seems to me you can refactor these equations due to recurring terms.
        # Or even better, coming from Color Blocks, aren't block dimensions present in GameScreen? Check!
        block_height = int(math.floor(screen.screen_size[1] - self.draw_offset[1]) / len(self.grid))
        block_width = int(math.floor(screen.screen_size[0] - self.draw_offset[0]) / len(self.grid[0]))
        row_index = int(math.floor((pos[1] - self.draw_offset[1]) / block_height))
        col_index = int(math.floor((pos[0] - self.draw_offset[0]) / block_width))

        return (row_index, col_index)
    
    def __incr(self, index, dimension_length):
        if index == (dimension_length - 1):
            return index
        else:
            return index + 1
    
    def __decr(self, index):
        if index == 0:
            return index
        else:
            return index - 1
    
    def __list_unique(self, *items):
        """
        More Pythonically, list(set(items)) but this preserves the order in which
        the unique items first appeared.
        """
        unique = []
        
        for i in items:
            if i not in unique:
                unique.append(i)
        
        return unique
    
    def __hv_adj(self, current_block, is_height):
        """
        Returns the adjacent list for only one dimension as determined
        by argument is_height.
        
        The return value is a list of tuples.
        """
        adjacent = []
        
        if is_height:
            dim_len = len(self.grid)
            static_index = 1
            trans_index = 0
        else:
            dim_len = len(self.grid[0])
            static_index = 0
            trans_index = 1
        
        move_dim = current_block[trans_index]
        
        increased = self.__incr(move_dim, dim_len)
        decreased = self.__decr(move_dim)
        
        if increased == move_dim:
            pass
        else:
            t = []
            t.insert(trans_index, increased)
            t.insert(static_index, current_block[static_index])
            adjacent.append(tuple(t))
        
        if decreased == move_dim:
            pass
        else:
            t = []
            t.insert(trans_index, decreased)
            t.insert(static_index, current_block[static_index])
            adjacent.append(tuple(t))
        
        return adjacent
    
    def __diag_adj(self, current_block):
        """
        Returns _the whole_ adjacent list of diagonals (in contrast to
        __hv_adj) above.
        """
        row = current_block[0]
        col = current_block[1]
        
        rows = self.__list_unique(self.__incr(row, len(self.grid)), self.__decr(row))
        cols = self.__list_unique(self.__incr(col, len(self.grid[0])), self.__decr(col))
        adjacent = []
        
        for i in range(len(rows)):
            for j in range(len(cols)):
                if rows[i] != row and cols[j] != col:
                    adjacent.append((rows[i], cols[j]))
        
        return adjacent
    
    def get_adjacent(self, row, col):
        """
        Returns a list of all the adjacent cells to block (row, col), depending
        on the set-up of the invoking object. The return list contains tuples of
        the index coordinates of the adjacent blocks.
        """
        
        if type(row) != type(0) or type(col) != type(0):
            raise TypeError("Parameters should be of type int.")
        
        if row > len(self.grid) or col > len(self.grid[0]) or row < 0 or col < 0:
            raise IndexError("Invalid index!")
        
        current_block = (row, col)
        hv_adj = []
        diag_adj = []
        
        if self.hv_neighbors:
            hv_rows = self.__hv_adj(current_block, True)
            hv_cols = self.__hv_adj(current_block, False)
            hv_adj = hv_rows
            limit = len(hv_cols)
            
            for i in range(limit):
                hv_adj.append(hv_cols[i])
        
        if self.diag_neighbors:
            diag_adj = self.__diag_adj(current_block)
        
        limit = len(hv_adj)
        for i in range(limit):
            if hv_adj[i] not in diag_adj and hv_adj[i] != current_block:
                diag_adj.append(hv_adj[i])
        
        return diag_adj

class TriangularGrid(Grid):
    """
    Represents a triangular grid.
    """
    
    def __init__(self, grid_width, grid_height):
        """
        Given the grid width and the grid height, we determine the origin
        to be (floor(grid_width/2), floor(grid_height/2)). Take note of
        this.
        
        Indices less than the origin coordinates are taken as negative.
        Use these indices when referring to points in this grid.
        """
        super(Grid, self).__init__()
        self.__origin_x = math.floor(grid_width / 2)
        self.__origin_y = math.floor(grid_height / 2)
