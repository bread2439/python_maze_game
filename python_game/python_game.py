import pygame
from board import GameBoard
from player import Player
import colors

# Initialize Pygame
pygame.init()

# Define window dimensions
WIDTH, HEIGHT = 1280, 720

# Define game board
game_board = GameBoard(WIDTH, HEIGHT)
player = Player(WIDTH//2, HEIGHT//2, colors.RED)


# Create the display surface (window)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set the window title
pygame.display.set_caption("game project")

a_held = False
d_held = False
w_held = False
s_held = False

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Check if the user clicked the close button
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                a_held = True
            if event.key == pygame.K_d:
                d_held = True
            if event.key == pygame.K_w:
                w_held = True
            if event.key == pygame.K_s:
                s_held = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                a_held = False
            if event.key == pygame.K_d:
                d_held = False
            if event.key == pygame.K_w:
                w_held = False
            if event.key == pygame.K_s:
                s_held = False

    if(a_held == True):
        player.rotate_left()
    if(d_held == True):
        player.rotate_right()
    if(w_held == True):
        player.forward()
    if(s_held == True):
        player.backward()

    # Drawing (fill the background with a color)
    screen.fill(colors.WHITE)  # Black color (RGB: 0, 0, 0)




    # game drawing here
    game_board.draw(screen)
    player.draw(screen)





    # Update the display
    pygame.display.flip()  # or pygame.display.update()

# Quit Pygame
pygame.quit()