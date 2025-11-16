import pygame
import colors
import random
import math
from typing import List
from disjoint_set import DisjointSet


# Colors
GAME_BACKGROUND_COLOR = colors.WHITE
BOARD_BACKGROUND_COLOR = colors.GREY
BOARD_BORDER_COLOR = colors.BLACK
WALL_COLOR = colors.BLACK

random.seed(10)

 
class GameBoard:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.border_offset = 10
        
        self.square_width = 40
        self.wall_width = 0

        self.n_units = self.__compute_units()

        self.board = self.__build_board()
        self.border = self.__build_border()
        self.grid = self.__gen_maze()
           

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
        n = int(self.n_units)
        for y in range(n):
            for x in range(n):
                cell = self.grid[y][x]
                px = x * self.unit_size + self.board_x
                py = y * self.unit_size + self.board_y

                # Draw walls as 1px lines where there is NO passage.

                # North wall
                if not cell['N']:
                    pygame.draw.line(
                        screen, WALL_COLOR,
                        (px, py), (px + self.unit_size, py), 1
                    )

                # West wall
                if not cell['W']:
                    pygame.draw.line(
                        screen, WALL_COLOR,
                        (px, py), (px, py + self.unit_size), 1
                    )

                # South wall: only draw on the bottom row
                if y == n - 1 and not cell['S']:
                    pygame.draw.line(
                        screen, WALL_COLOR,
                        (px, py + self.unit_size), (px + self.unit_size, py + self.unit_size), 1
                    )

                # East wall: only draw on the rightmost column
                if x == n - 1 and not cell['E']:
                    pygame.draw.line(
                        screen, WALL_COLOR,
                        (px + self.unit_size, py), (px + self.unit_size, py + self.unit_size), 1
                    )



    def __gen_maze(self):
        n = int(self.n_units)
        num_cells = n * n
        dsu = DisjointSet(num_cells)

        def cell_id(x, y):
            return y * n + x

        edges = []
        for y in range(n):
            for x in range(n):
                if x + 1 < n:
                    edges.append((x, y, x + 1, y))
                if y + 1 < n:
                    edges.append((x, y, x, y + 1))

        random.shuffle(edges)

        cells = [[{'N': False, 'S': False, 'E': False, 'W': False}
                  for _ in range(n)] for _ in range(n)]

        for x1, y1, x2, y2 in edges:
            id1 = cell_id(x1, y1)
            id2 = cell_id(x2, y2)

            if dsu.union(id1, id2):
                if x2 == x1 + 1:
                    cells[y1][x1]['E'] = True
                    cells[y2][x2]['W'] = True
                elif x2 == x1 - 1:
                    cells[y1][x1]['W'] = True
                    cells[y2][x2]['E'] = True
                elif y2 == y1 + 1:     
                    cells[y1][x1]['S'] = True
                    cells[y2][x2]['N'] = True
                elif y2 == y1 - 1:
                    cells[y1][x1]['N'] = True
                    cells[y2][x2]['S'] = True

        return cells
            

