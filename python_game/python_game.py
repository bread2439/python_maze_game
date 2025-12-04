import pygame
from board import GameBoard
from player import Player
import colors
from pygame.math import Vector2
import math

# moves the player and checks for collisions
def move_with_collisions(pos, vel, d, wall_rects, radius):
    new_pos = Vector2(pos)

    # move in x direction and check x direction
    new_pos.x += vel.x * dt
    if vel.x != 0:
        for wall in wall_rects:
            expanded = wall.inflate(radius * 2, radius * 2)
            if expanded.collidepoint(new_pos.x, new_pos.y):
                if vel.x > 0:  
                    # moving right -> push to left side
                    new_pos.x = expanded.left - 0.0001
                else:          
                    # moving left -> push to right side
                    new_pos.x = expanded.right + 0.0001

    # move in y direction and check y direction
    new_pos.y -= vel.y * dt
    if vel.y != 0:
        for wall in wall_rects:
            expanded = wall.inflate(radius * 2, radius * 2)
            if expanded.collidepoint(new_pos.x, new_pos.y):
                if vel.y < 0:  
                    # moving down -> push up
                    new_pos.y = expanded.top - 0.0001
                else:         
                    # moving up -> push down
                    new_pos.y = expanded.bottom + 0.0001

    return new_pos



# initialize Pygame
pygame.init()

# define window dimensions
WIDTH, HEIGHT = 1280, 720

# define game board
game_board = GameBoard(WIDTH, HEIGHT)
player1 = Player(460, 220, colors.BLACK)
player2 = Player(500, 500, colors.RED)


# create the display surface (window)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# set the window title
pygame.display.set_caption("game project")

# smooth keyboard input handling
a_held = False
d_held = False
w_held = False
s_held = False

left_held = False
right_held = False
up_held = False
down_held = False

# game clock for fps and frame independent actions
clock = pygame.time.Clock()

# game loop
running = True

while running:
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # checks first key down press
        if event.type == pygame.KEYDOWN:
            # no elif to allow for move accurate movement
            if event.key == pygame.K_a:
                a_held = True
            if event.key == pygame.K_d:
                d_held = True
            if event.key == pygame.K_w:
                w_held = True
            if event.key == pygame.K_s:
                s_held = True
            if event.key == pygame.K_e:
                player1.shoot()

            if event.key == pygame.K_LEFT:
                left_held = True
            if event.key == pygame.K_RIGHT:
                right_held = True
            if event.key == pygame.K_UP:
                up_held = True
            if event.key == pygame.K_DOWN:
                down_held = True
            if event.key == pygame.K_SLASH:
                player2.shoot()

        # checks when key is no longer held
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                a_held = False
            if event.key == pygame.K_d:
                d_held = False
            if event.key == pygame.K_w:
                w_held = False
            if event.key == pygame.K_s:
                s_held = False

            if event.key == pygame.K_LEFT:
                left_held = False
            if event.key == pygame.K_RIGHT:
                right_held = False
            if event.key == pygame.K_UP:
                up_held = False
            if event.key == pygame.K_DOWN:
                down_held = False
    
    # tracks time since last call with a 60fps cap
    dt = clock.tick(60)/1000.0

    # swtiches direction without using two functions
    player_1_move_forward = 0
    player_1_move_backward = 0

    player_2_move_forward = 0
    player_2_move_backward = 0
    
    # rotation
    if(a_held == True):
        player1.rotate_left(dt)
    if(d_held == True):
        player1.rotate_right(dt)

    if(left_held == True):
        player2.rotate_left(dt)
    if(right_held == True):
        player2.rotate_right(dt)

    # translation
    if(w_held == True):
        player_1_move_forward = 1
    else:
        player_1_move_forward = 0
    if(s_held == True):
        player_1_move_backward = 1
    else:
        player_1_move_backward = 0

    if(up_held == True):
        player_2_move_forward = 1
    else:
        player_2_move_forward = 0
    if(down_held == True):
        player_2_move_backward = 1
    else:
        player_2_move_backward = 0

    # converts the player position into a vector
    player1_pos = Vector2(player1.x, player1.y)
    player2_pos = Vector2(player2.x, player2.y)

    # if the move forward or move backward is not pressed dont move
    player_1_direction = 0
    # quick check for both
    if(player_1_move_forward + player_1_move_backward == 2):
        player_1_direction = 0
    # quick check for non
    elif(player_1_move_forward + player_1_move_backward == 0):
        player_1_direction = 0
    # checks for forward (most common)
    elif(player_1_move_forward == 1):
        player_1_direction = 1
    # default case
    else:
        player_1_direction = -1

    player_2_direction = 0
    # quick check for both
    if(player_2_move_forward + player_2_move_backward == 2):
        player_2_direction = 0
    # quick check for non
    elif(player_2_move_forward + player_2_move_backward == 0):
        player_2_direction = 0
    # checks for forward (most common)
    elif(player_2_move_forward == 1):
        player_2_direction = 1
    # default case
    else:
        player_2_direction = -1

    # velocity in the direction of the angle, with magnitude from velocity along the movement direction
    p1_vx = player1.movement_v * math.cos(3.14 / 180.0 * player1.angle) * player_1_direction
    p1_vy = player1.movement_v * math.sin(3.14 / 180.0 * player1.angle) * player_1_direction
    p1_vel = Vector2(p1_vx, p1_vy)

    p2_vx = player2.movement_v * math.cos(3.14 / 180.0 * player2.angle) * player_2_direction
    p2_vy = player2.movement_v * math.sin(3.14 / 180.0 * player2.angle) * player_2_direction
    p2_vel = Vector2(p2_vx, p2_vy)

    # update player position
    player1_pos = move_with_collisions(player1_pos, p1_vel, dt, game_board.wall_rects, player1.r)
    player1.x = player1_pos.x
    player1.y = player1_pos.y

    player2_pos = move_with_collisions(player2_pos, p2_vel, dt, game_board.wall_rects, player2.r)
    player2.x = player2_pos.x
    player2.y = player2_pos.y

    # fill in the window backgrounds
    screen.fill(colors.WHITE)

    # game drawing below here (V)
    # draw board and all of its components
    game_board.draw(screen)
    # draw player 1 and all of its components
    player1.draw(screen, dt, game_board.wall_rects)
    # draw player 2 and all of its components
    player2.draw(screen, dt, game_board.wall_rects)





    # updates the display
    pygame.display.flip()

# quit Pygame
pygame.quit()