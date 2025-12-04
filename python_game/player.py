import pygame
import math

# basic projectile class
class Projectile:
    # initializes member variables
    def __init__(self, x, y, a, color):
        self.r = 2
        self.v = 125
        self.x = x
        self.y = y
        self.a = a
        self.color = color
        self.bounce_limit = 6
        self.alive = True
        self.bounces_left = self.bounce_limit

        self.vx = self.v * math.cos(3.14 / 180.0 * self.a)
        self.vy = -self.v * math.sin(3.14 / 180.0 * self.a)

    # updates the projectile position and checks for bounces left
    def update(self, dt, wall_rects):
        # move in x direction
        dx = self.vx * dt
        self.x += dx

        # checks for colliion after moving in the x direction
        if dx != 0:
            for wall in wall_rects:
                expanded = wall.inflate(self.r * 2, self.r * 2)
                if expanded.collidepoint(self.x, self.y):
                    if dx > 0:
                        self.x = expanded.left - 0.0001
                    else:
                        self.x = expanded.right + 0.0001

                    self.vx *= -1
                    self.bounces_left -= 1
                    if self.bounces_left <= 0:
                        self.alive = False
                    break

        # quick sanity check after possible last bounce
        if not self.alive:
            return

        # move in the y direction
        dy = self.vy * dt
        self.y += dy

        # checks for collision after moving in the y direction
        if dy != 0:
            for wall in wall_rects:
                expanded = wall.inflate(self.r * 2, self.r * 2)
                if expanded.collidepoint(self.x, self.y):
                    if dy > 0:
                        # moving down on screen
                        self.y = expanded.top - 0.0001
                    else:        
                        # moving up on screen
                        self.y = expanded.bottom + 0.0001

                    self.vy *= -1
                    self.bounces_left -= 1
                    if self.bounces_left <= 0:
                        self.alive = False
                    break

    # draws the projectile
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)



# player class
class Player:
    def __init__(self, x, y, color):
        # position
        self.x:int = x 
        self.y:int = y

        # color
        self.TOP_COLOR:tuple    = color
        self.BOTTOM_COLOR:tuple = color

        # barrel
        self.barrel_w:float = 7.5
        self.barrel_h:float = 12
        self.angle:float = 0.0
        self.barrel = self.__build_barrel()

        # circle
        self.r:float = 7.5

        # movement
        self.movement_v = 100
        self.rotation_v = 270

        # projectiles
        self.projectiles = []

        # alive condition
        self.alive = True

    # builds the barrel
    def __build_barrel(self):
        barrel_image = pygame.Surface((self.barrel_w, self.barrel_h), pygame.SRCALPHA)
        barrel_image.fill(self.TOP_COLOR)
        return barrel_image
    
    # rotates the player left not visually just logically
    def rotate_left(self, dt):
        self.angle += self.rotation_v * dt

    # rotates the player right not visually just logically
    def rotate_right(self, dt):
        self.angle -= self.rotation_v * dt

    # creates a projectile to move in the direction of the player
    def shoot(self):
        dx = 1
        dy = 1
        b_dx =  dx * math.cos(3.14 / 180 * self.angle)
        b_dy = -dy * math.sin(3.14 / 180 * self.angle)
        bx = self.x + b_dx
        by = self.y + b_dy
        self.projectiles.append(Projectile(bx, by, self.angle, self.TOP_COLOR))

    # draws the player and all projectiles
    def draw(self, screen, dt, wall_rects):
        # draw player circle
        pygame.draw.circle(screen, self.BOTTOM_COLOR, (self.x, self.y), self.r)
        
        # draw projectiles
        for proj in self.projectiles:
            proj.update(dt, wall_rects)
            proj.draw(screen)

        # if a projectile bounced and is its last bounce remove
        for proj in self.projectiles:
            if(proj.bounces_left == 0):
                self.projectiles.remove(proj)
        
        
        # rotate the barrel if necessary
        rotated_image = pygame.transform.rotate(self.barrel, self.angle+90.0)

        # compute the new center based on the center of the circle
        # since the barrel by default will be rotated around its center
        # the barrels center needs to be translated so the barrel is pointing in
        # the direction of the angle

        # since the barrel is initially centered the center
        # must be moved a distance of half the height away from the player center
        dx = self.barrel_h / 2
        dy = self.barrel_h / 2
        b_dx =  dx * math.cos(3.14 / 180 * self.angle)
        b_dy = -dy * math.sin(3.14 / 180 * self.angle)
        bx = self.x + b_dx
        by = self.y + b_dy
        new_barrel = rotated_image.get_rect(center=(bx,by))


        # draw barrel
        screen.blit(rotated_image, new_barrel)



