import pygame
from board import GameBoard
import colors

# Initialize Pygame
pygame.init()

# Define window dimensions
WIDTH, HEIGHT = 1280, 720

# Define game board
game_board = GameBoard(WIDTH, HEIGHT)
game_board.gen_maze()



# Create the display surface (window)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set the window title
pygame.display.set_caption("game project")

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Check if the user clicked the close button
            running = False

    # Drawing (fill the background with a color)
    screen.fill(colors.WHITE)  # Black color (RGB: 0, 0, 0)




    # game drawing here
    game_board.draw(screen)





    # Update the display
    pygame.display.flip()  # or pygame.display.update()

# Quit Pygame
pygame.quit()