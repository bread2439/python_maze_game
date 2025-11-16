import pygame
import math


class Player:
    def __init__(self, x, y, top_color, bottom_color):
        # position
        self.x:int = x 
        self.y:int = y

        # color
        self.TOP_COLOR:tuple    = top_color
        self.BOTTOM_COLOR:tuple = bottom_color

        # barrel
        self.barrel_w:float = 7.5
        self.barrel_h:float = 12
        self.angle:float = 0.0
        self.barrel = self.__build_barrel()

        # circle
        self.r:float = 7.5

        # movement
        self.v = 0.2

    def __build_barrel(self):
        barrel_image = pygame.Surface((self.barrel_w, self.barrel_h), pygame.SRCALPHA)
        barrel_image.fill(self.TOP_COLOR)
        return barrel_image

    def rotate_left(self):
        self.angle += 1

    def rotate_right(self):
        self.angle -= 1

    def forward(self):
        delta_x = self.v * math.cos(3.14 / 180.0 * self.angle)
        delta_y = self.v * math.sin(3.14 / 180.0 * self.angle)
        self.x += delta_x
        self.y -= delta_y
    
    def backward(self):
        delta_x = self.v * math.cos(3.14 / 180.0 * self.angle)
        delta_y = self.v * math.sin(3.14 / 180.0 * self.angle)
        self.x -= delta_x
        self.y += delta_y

    def draw(self, screen):
        # draw circle
        pygame.draw.circle(screen, self.TOP_COLOR, (self.x, self.y), self.r)
        
        
        
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



