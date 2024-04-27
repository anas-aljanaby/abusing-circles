import pygame
import pygame.gfxdraw
import math


class CircleContainer:
    def __init__(self, x, y, color='white', r=300, shadow=True):
        self.x = x
        self.y = y
        self.radius = r 
        self.color = color
        self.shadow = shadow

           
    def draw(self, scr):
        alpha_surface = pygame.Surface((1200, 800), pygame.SRCALPHA)
        
        n_rings = 5
        for i in range(n_rings, 0, -1):
            color = (255, 255, 255, 255-i*10) 
            pygame.gfxdraw.filled_circle(alpha_surface, self.x, self.y, self.radius+i, color)

        color = (0, 0, 0, 255) 
        pygame.gfxdraw.filled_circle(alpha_surface, self.x, self.y, self.radius-10, color)

        scr.blit(alpha_surface, (0, 0))

class Orb:
    def __init__(self, x, y, color=(255, 255, 255), container=None):
        self.x = x
        self.y = y
        self.color = color
        self.base_speed = 5
        self.current_speed = 5
        self.container = container 
        self.y_speed = 0.5 
        self.x_speed = 0
        self.x_dir = 1
        self.y_dir = 1
        self.radius = 20
        self.gravity = 2 
        self.energy_gain = 1.1
        self.acc = 1
        self.x_acc = 0

    def draw(self, scr):
        pygame.draw.circle(scr, self.color, (self.x, self.y), self.radius)

    def update_pos(self):
        self.y_speed += self.acc
        self.x_speed += self.x_acc

        self.y += self.y_speed
        self.x += self.x_speed

        dist = math.sqrt((self.x - self.container.x)**2 + (self.y - self.container.y)**2)
        if dist + self.radius >= self.container.radius:
            angle = math.atan2(self.y - self.container.y, self.x - self.container.x)

            self.x = self.container.x + (self.container.radius - self.radius) * math.cos(angle)
            self.y = self.container.y + (self.container.radius - self.radius) * math.sin(angle)

            self.y_speed *= -1 
            self.y_speed *= 1.1            
            self.x_speed *= -1 
            self.x_speed *= 1.1

            if self.x_acc==0:
                self.x_acc = 1
                self.x_speed = 1
            



