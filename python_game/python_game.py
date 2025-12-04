import pygame
from board import GameBoard
from player import Player
import colors
from pygame.math import Vector2
import math


def move_with_collisions(pos: Vector2, vel: Vector2, dt: float,
                         wall_rects, radius: float) -> Vector2:
    new_pos = Vector2(pos)

    # --- move X first ---
    new_pos.x += vel.x * dt
    if vel.x != 0:
        for wall in wall_rects:
            expanded = wall.inflate(radius * 2, radius * 2)
            if expanded.collidepoint(new_pos.x, new_pos.y):
                if vel.x > 0:  # moving right -> push to left side
                    new_pos.x = expanded.left - 0.0001
                else:          # moving left -> push to right side
                    new_pos.x = expanded.right + 0.0001

    # --- then move Y ---
    new_pos.y -= vel.y * dt
    if vel.y != 0:
        for wall in wall_rects:
            expanded = wall.inflate(radius * 2, radius * 2)
            if expanded.collidepoint(new_pos.x, new_pos.y):
                if vel.y < 0:  # moving down -> push up
                    new_pos.y = expanded.top - 0.0001
                else:          # moving up -> push down
                    new_pos.y = expanded.bottom + 0.0001

    return new_pos



# Initialize Pygame
pygame.init()

# Define window dimensions
WIDTH, HEIGHT = 1280, 720

# Define game board
game_board = GameBoard(WIDTH, HEIGHT)
player = Player(460, 220, colors.BLACK)


# Create the display surface (window)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set the window title
pygame.display.set_caption("game project")

a_held = False
d_held = False
w_held = False
s_held = False

clock = pygame.time.Clock()

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
            if event.key == pygame.K_SPACE:
                player.shoot()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                a_held = False
            if event.key == pygame.K_d:
                d_held = False
            if event.key == pygame.K_w:
                w_held = False
            if event.key == pygame.K_s:
                s_held = False

    dt = clock.tick(60)/1000.0

    move_forward = 0
    move_backward = 0
    
    if(a_held == True):
        player.rotate_left(dt)
    if(d_held == True):
        player.rotate_right(dt)
    if(w_held == True):
        move_forward = 1
    else:
        move_forward = 0
    if(s_held == True):
        move_backward = 1
    else:
        move_backward = 0


    player_pos = Vector2(player.x, player.y)

    direction = 0
    if(move_forward + move_backward == 2):
        direction = 0
    elif(move_forward + move_backward == 0):
        direction = 0
    elif(move_forward == 1):
        direction = 1
    else:
        direction = -1
    vx = player.movement_v * math.cos(3.14 / 180.0 * player.angle) * direction
    vy = player.movement_v * math.sin(3.14 / 180.0 * player.angle) * direction
    vel = Vector2(vx, vy)

    player_pos = move_with_collisions(player_pos, vel, dt, game_board.wall_rects, player.r)
    player.x = player_pos.x
    player.y = player_pos.y

    # Drawing (fill the background with a color)
    screen.fill(colors.WHITE)  # Black color (RGB: 0, 0, 0)



    # game drawing here
    game_board.draw(screen)
    player.draw(screen, dt, game_board.wall_rects)





    # Update the display
    pygame.display.flip()  # or pygame.display.update()

# Quit Pygame
pygame.quit()