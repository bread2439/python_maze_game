import pygame
import colors
import random
from disjoint_set import DisjointSet



# colors
GAME_BACKGROUND_COLOR = colors.WHITE
BOARD_BACKGROUND_COLOR = colors.GREY
BOARD_BORDER_COLOR = colors.BLACK
WALL_COLOR = colors.BLACK



random.seed(10)

# game board class
class GameBoard:
    # initializes the board, boarder, maze(grid), and wall hit boxes
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

        self.wall_thickness = 6
        self.wall_rects = self.__build_wall_rects()
           
    # figures out how many units to make the screen, assumes: screen height is less than screen width
    # builds a rectangular board to fit the height
    def __compute_units(self):
        self.unit_size = self.square_width + self.wall_width
        return ((self.screen_height - (self.screen_height % self.unit_size)) / self.unit_size) - 2

    # builds the board rect (background)
    def __build_board(self):
        self.board_width = self.n_units * self.unit_size
        self.board_height = self.board_width
        # centers the board in the middle of the screen with equal offset on the y and x axis
        self.board_x = (self.screen_width  - (self.board_width)) / 2.0
        self.board_y = (self.screen_height - (self.board_height)) / 2.0
        return pygame.Rect(self.board_x, self.board_y, self.board_width, self.board_height)

    # builds the board border (maze border)
    def __build_border(self):
        # centers the border around the board
        self.border_x = self.board_x - self.border_offset
        self.border_y = self.board_y - self.border_offset
        self.border_width  = self.board_width + self.border_offset * 2
        self.border_height = self.board_height + self.border_offset * 2
        return pygame.Rect(self.border_x, self.border_y, self.border_width, self.border_height) 

    # builds the maze walls (visual)
    def __gen_maze(self):
        # width of maze in maze units
        n = int(self.n_units)
        # total grid(maze) size
        num_cells = n * n
        dsu = DisjointSet(num_cells)

        # returns the cell id
        def cell_id(x, y):
            return y * n + x

        # constructs all edges needed in a clean manner
        edges = []
        for y in range(n):
            for x in range(n):
                if x + 1 < n:
                    edges.append((x, y, x + 1, y))
                if y + 1 < n:
                    edges.append((x, y, x, y + 1))

        # shuffles edges to make the maze appear random
        random.shuffle(edges)

        # each cell has a state to track where edges (walls) are
        cells = [[{'N': False, 'S': False, 'E': False, 'W': False}
                  for _ in range(n)] for _ in range(n)]

        # pulls the two coordinates from the shuffled edges p1(x1,y1) and p2(x2,y2)
        for x1, y1, x2, y2 in edges:
            id1 = cell_id(x1, y1)
            id2 = cell_id(x2, y2)

            # checks to see if two cells are connected
            ## if they are not connected connect them
            ## if they are connected don't do anything
            if dsu.union(id1, id2):
                if x2 == x1 + 1:
                    # remove the east and west wall connecting a right cell to a left cell
                    # x1 -> | <- x2 wall is removed
                    cells[y1][x1]['E'] = True
                    cells[y2][x2]['W'] = True
                elif x2 == x1 - 1:
                    # remove the west and east wall connecting a left cell to a right cell
                    # x2 -> | <- x1 wall is removed
                    cells[y1][x1]['W'] = True
                    cells[y2][x2]['E'] = True
                elif y2 == y1 + 1:     
                    # remove the south and north wall connecting a bottom cell to a top cell
                    # y1 v
                    # ----- wall is removed
                    # y2 ^
                    cells[y1][x1]['S'] = True
                    cells[y2][x2]['N'] = True
                elif y2 == y1 - 1:
                    # remove the north and south wall connecting a top cell to a bottom cell
                    # y2 v
                    # ----- wall is removed
                    # y1 ^
                    cells[y1][x1]['N'] = True
                    cells[y2][x2]['S'] = True

        return cells

    # builds the maze wall (hitboxes)
    def __build_wall_rects(self):
        # grid(maze) width
        n = int(self.n_units)
        walls = []

        # hitbox thickness (takes into account barrel length to avoid
        # barrel poking through walls
        t = self.wall_thickness
        half_t = t / 2.0

        # goes through the maze grid and matchez visual walls with hitboxes to build
        for y in range(n):
            for x in range(n):
                cell = self.grid[y][x]
                px = x * self.unit_size + self.board_x
                py = y * self.unit_size + self.board_y

                # cell['direction'] checks to see if there is a wall
                # false = wall present
                # true = gap/tunnel present

                # builds a hitbox on the north wall
                if not cell['N']:
                    rect = pygame.Rect(px,
                                       py - half_t,
                                       self.unit_size,
                                       t)
                    walls.append(rect)

                # builds a hitbox on the west wall
                if not cell['W']:
                    rect = pygame.Rect(px - half_t,
                                       py,
                                       t,
                                       self.unit_size)
                    walls.append(rect)

                # checks are to make sure north and west walls are not rebuilt
                # builds a hitbox on the south wall
                if y == n - 1 and not cell['S']:
                    rect = pygame.Rect(px,
                                       py + self.unit_size - half_t,
                                       self.unit_size,
                                       t)
                    walls.append(rect)

                # builds a hitbox on the east wall
                if x == n - 1 and not cell['E']:
                    rect = pygame.Rect(px + self.unit_size - half_t,
                                       py,
                                       t,
                                       self.unit_size)
                    walls.append(rect)

        return walls

    # draws all the components that make up the "game board"
    def draw(self, screen):
        # draws the border first since it is larger and prevents from having to handle 4 border walls
        pygame.draw.rect(screen, BOARD_BORDER_COLOR, self.border)
        # draws the small board (background for maze walls)
        pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, self.board)

        # maze width
        n = int(self.n_units)
        # iterates by row -> colum
        for y in range(n):
            for x in range(n):
                cell = self.grid[y][x]
                px = x * self.unit_size + self.board_x
                py = y * self.unit_size + self.board_y

                # draws walls as 1px lines

                # north wall
                if not cell['N']:
                    pygame.draw.line(
                        screen, WALL_COLOR,
                        (px, py), (px + self.unit_size, py), 1
                    )

                # west wall
                if not cell['W']:
                    pygame.draw.line(
                        screen, WALL_COLOR,
                        (px, py), (px, py + self.unit_size), 1
                    )

                # section below includes extra checks to prevent a north or west wall from being redrawn
                # south wall only draw on the bottom row
                if y == n - 1 and not cell['S']:
                    pygame.draw.line(
                        screen, WALL_COLOR,
                        (px, py + self.unit_size), (px + self.unit_size, py + self.unit_size), 1
                    )

                # east wall only draw on the rightmost column
                if x == n - 1 and not cell['E']:
                    pygame.draw.line(
                        screen, WALL_COLOR,
                        (px + self.unit_size, py), (px + self.unit_size, py + self.unit_size), 1
                    )