import pygame
import colors
import random
import math
from typing import List


# Colors
GAME_BACKGROUND_COLOR = colors.WHITE
BOARD_BACKGROUND_COLOR = colors.GREY
BOARD_BORDER_COLOR = colors.BLACK

random.seed(10)

 
class GameBoard:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.border_offset = 10
        
        self.square_width = 40
        self.wall_width = 10

        self.n_units = self.__compute_units()

        self.board = self.__build_board()
        self.border = self.__build_border()

        self.grid = self.__build_grid()

        self.__print_grid()
           
    def __print_grid(self):
        max_width = max(len(str(x)) for row in self.grid for x in row)

        for row in self.grid:
            for val in row:
                print(f"{val:>{max_width}}", end=" ")
            print()  # newline after each row


    def __compute_units(self):
        self.unit_size = self.square_width + self.wall_width
        return ((self.screen_height - (self.screen_height % self.unit_size)) / self.unit_size) - 2

    def __build_board(self):
        self.board_width = self.n_units * self.unit_size
        self.board_height = self.board_width
        # centers the board in the middle of the screen with equal offset on the y and x axis
        self.board_x = (self.screen_width  - (self.board_width)) / 2.0
        self.board_y = (self.screen_height - (self.board_height)) / 2.0
        return pygame.Rect(self.board_x, self.board_y, self.board_width, self.board_height)

    def __build_border(self):
        self.border_x = self.board_x - self.border_offset
        self.border_y = self.board_y - self.border_offset
        self.border_width  = self.board_width + self.border_offset * 2
        self.border_height = self.board_height + self.border_offset * 2
        return pygame.Rect(self.border_x, self.border_y, self.border_width, self.border_height) 

    def draw(self, screen):
        pygame.draw.rect(screen, BOARD_BORDER_COLOR, self.border)
        pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, self.board)

    def __build_grid(self):
        n = int(self.n_units)
        grid = []
        v = 0
        for x in range(n):
            row = []
            for y in range(n):
                v+=1
                row.append(v)
            grid.append(row)
        return grid

    def __find_root_cell(self, unique_cells: List[int], flat_grid: List[int]):

        # root cell should be randomly picked from unique_cells
        cell_candidate_idx = random.randint(0, len(unique_cells) - 1)
        cell_candidate     = unique_cells[cell_candidate_idx]
        
        print(cell_candidate_idx)
        print(cell_candidate)
        print(unique_cells)

        candidates_idx = [cell_candidate_idx]
        # check the count of root cell, if > 1 then find the first that has 
        n_candidates = flat_grid.count(cell_candidate)
        if(n_candidates > 1):
            candidates_idx = [i for i, x in enumerate(flat_grid) if x == cell_candidate]
        
        n = int(self.n_units)

        print(candidates_idx)


        if(len(candidates_idx) == 1):
            root_cell_idx = flat_grid.index(cell_candidate)
            root_cell = cell_candidate
            return (root_cell_idx, root_cell)
        else:
            valid_cell = False
            while(not valid_cell):
                # loop over the candidates_idx array for the first valid cell
                cell_candidate_idx = random.randint(0, len(candidates_idx) - 1)
                cell_candidate     = flat_grid[candidates_idx[cell_candidate_idx]]

                # check if candidate has a non same value neighbor
                flat_idx = cell_candidate_idx
                col_idx = flat_idx % n
                row_idx = math.floor(float(flat_idx)/float(n))

                col_idx_lim = len(self.grid[0])-1
                row_idx_lim = len(self.grid)-1

                directions = ["N","E","S","W"]

                # check for cells that are on the grid border
                ## checks left and right border cells
                if(row_idx == 0):
                    directions.remove("N")
                if(row_idx == row_idx_lim):
                    directions.remove("S")
                
                ## checks top and bottom border cells
                if(col_idx == 0):
                    directions.remove("W")
                if(col_idx == col_idx_lim):
                    directions.remove("E")

                # now check for possible non same neighbor cells in valid directions
                direction_idx = random.randint(0,len(directions)-1)
                direction = directions[direction_idx]

                while(len(directions) != 0):
                    # finds the new col_idx
                    if(direction == "N"):
                        row_idx -= 1
                    if(direction == "S"):
                        row_idx += 1

                    # finds the new row_idx
                    if(direction == "E"):
                        col_idx -= 1
                    if(direction == "W"):
                        col_idx += 1

                    test_idx = n * row_idx + col_idx
                    if(flat_grid[test_idx] != cell_candidate):
                        break
                        return (test_idx, flat_gird[test_idx])
                    else:
                        # remove direction with no results
                        direction.remove(direction)

                        # pick a new direction
                        direction_idx = random.randint(0, len(directions) - 1)
                        direction = directions[direction_idx]

                # no valid direction found remove cell 
                candidates_idx.remove(cell_candidate_idx)


    def __find_leaf_cell(self, flat_grid: List[int], root_cell_idx: int, root_cell: int):
        flat_idx = root_cell_idx
        n = int(self.n_units)


        col_idx = flat_idx % n
        row_idx = math.floor(float(flat_idx)/float(n))
        col_idx_lim = len(self.grid[0]) - 1
        row_idx_lim = len(self.grid) - 1

        
        
        directions = ["N","E","S","W"]

        # check for cells that are on the grid border
        ## checks left and right border cells
        if(row_idx == 0):
            directions.remove("N")
        if(row_idx == row_idx_lim):
            directions.remove("S")
        
        ## checks top and bottom border cells
        if(col_idx == 0):
            directions.remove("W")
        if(col_idx == col_idx_lim):
            directions.remove("E")

        # now check for possible non same neighbor cells in valid directions
        direction_idx = random.randint(0,len(directions)-1)
        direction = directions[direction_idx]


        while(len(directions)!=0):
            # finds the new col_idx
            if(direction == "N"):
                row_idx -= 1
            if(direction == "S"):
                row_idx += 1

            # finds the new row_idx
            if(direction == "E"):
                col_idx -= 1
            if(direction == "W"):
                col_idx += 1

            cell_candidate_idx = n * row_idx + col_idx
            if(flat_grid[cell_candidate_idx] != root_cell):
                return (cell_candidate_idx, flat_grid[cell_candidate_idx])
            else:
                # remove direction with no results
                direction.remove(direction)

                # pick a new direction
                direction_idx = random.randint(0, len(directions) - 1)
                direction = directions[direction_idx]

    def gen_maze(self):
        n = int(self.n_units)
        unique_cells = [i+1 for i in range(n*n)]

        # iterate over all the cells until there are no unique cells
        while(len(unique_cells) != 1):
            flat_grid = []
            for row in self.grid:
                for val in row:
                    flat_grid.append(val)



            root_cell_idx, root_cell = self.__find_root_cell(unique_cells, flat_grid)

            leaf_cell_idx, leaf_cell = self.__find_leaf_cell(flat_grid, root_cell_idx, root_cell)
            print(f"root: {root_cell}", f"leaf: {leaf_cell}")


            col_idx = leaf_cell_idx % n
            row_idx = math.floor(float(leaf_cell_idx)/float(n))
            self.grid[row_idx][col_idx] = root_cell
            if(leaf_cell in unique_cells):
                unique_cells.remove(leaf_cell)
            if(root_cell in unique_cells):
                unique_cells.remove(root_cell)

            input()

            self.__print_grid()

            # non same cell around it 
            # random direction should handle the case where 
            

