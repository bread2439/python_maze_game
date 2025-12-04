import pygame
import math

class Projectile:
    def __init__(self, x, y, a, color):
        self.r = 2
        self.v = 125
        self.x = x
        self.y = y
        self.a = a
        self.color = color
        self.bounce_limit = 3
        self.alive = True
        self.bounces_left = self.bounce_limit

        self.vx = self.v * math.cos(3.14 / 180.0 * self.a)
        self.vy = self.v * math.sin(3.14 / 180.0 * self.a)


    def update(self, dt, wall_rects):
        # simple collision detection
        """
        # move the projectile
        delta_x = self.v * math.cos(3.14 / 180.0 * self.a)
        delta_y = self.v * math.sin(3.14 / 180.0 * self.a)
        self.x += delta_x * dt
        self.y -= delta_y * dt
        
        # check for collisions
        for wall in wall_rects:
            expanded = wall.inflate(self.r * 2, self.r * 2)
            if expanded.collidepoint(self.x, self.y):
                # collision detected
                
                break
        """


        self.x += self.vx * dt
        if self.vx != 0:
            for wall in wall_rects:
                expanded = wall.inflate(self.r * 2, self.r * 2)
                if expanded.collidepoint(self.x, self.y):
                    # push out of wall on X
                    if self.vx > 0:
                        self.x = expanded.left - 0.0001
                    else:
                        self.x = expanded.right + 0.0001

                    # reflect X velocity
                    self.vx *= -1
                    self.bounces_left -= 1
                    if self.bounces_left <= 0:
                        self.alive = False
                    break

        # --- move on Y ---
        # use the same sign convention as your player:
        # if your player does new_pos.y -= vel.y * dt, do the same here
        self.y -= self.vy * dt
        if self.vy != 0 and self.alive:
            for wall in wall_rects:
                expanded = wall.inflate(self.r * 2, self.r * 2)
                if expanded.collidepoint(self.x, self.y):
                    # push out of wall on Y
                    if self.vy < 0:   # moving down in world coords
                        self.y = expanded.top - 0.0001
                    else:                # moving up in world coords
                        self.y = expanded.bottom + 0.0001

                    # reflect Y velocity
                    self.vy *= -1
                    self.bounces_left -= 1
                    if self.bounces_left <= 0:
                        self.alive = False
                    break

        


    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)



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

        self.projectiles = []

    def __build_barrel(self):
        barrel_image = pygame.Surface((self.barrel_w, self.barrel_h), pygame.SRCALPHA)
        barrel_image.fill(self.TOP_COLOR)
        return barrel_image

    def rotate_left(self, dt):
        self.angle += self.rotation_v * dt

    def rotate_right(self, dt):
        self.angle -= self.rotation_v * dt

    def forward(self, dt):
        delta_x = self.movement_v * math.cos(3.14 / 180.0 * self.angle)
        delta_y = self.movement_v * math.sin(3.14 / 180.0 * self.angle)
        self.x += delta_x * dt
        self.y -= delta_y * dt
    
    def backward(self, dt):
        delta_x = self.movement_v * math.cos(3.14 / 180.0 * self.angle)
        delta_y = self.movement_v * math.sin(3.14 / 180.0 * self.angle)
        self.x -= delta_x * dt
        self.y += delta_y * dt

    def shoot(self):
        dx = (self.barrel_h + 8) / 2
        dy = (self.barrel_h + 8) / 2
        b_dx =  dx * math.cos(3.14 / 180 * self.angle)
        b_dy = -dy * math.sin(3.14 / 180 * self.angle)
        bx = self.x + b_dx
        by = self.y + b_dy
        self.projectiles.append(Projectile(bx, by, self.angle, self.TOP_COLOR))

    def draw(self, screen, dt, wall_rects):
        # draw circle
        pygame.draw.circle(screen, self.BOTTOM_COLOR, (self.x, self.y), self.r)
        
        for proj in self.projectiles:
            proj.update(dt, wall_rects)
            proj.draw(screen)
        
        
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



