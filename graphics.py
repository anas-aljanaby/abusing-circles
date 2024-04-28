import pygame
import pygame.gfxdraw
from pygame import mixer
import math
import random
import sys

mixer.init()
sound =  pygame.mixer.Sound('ball_hit.mp3')

class CircleContainer:
    def __init__(self, x, y, color='white', r=300, shadow=True):
        self.x = x
        self.y = y
        self.radius = r 
        self.color = color
        self.shadow = shadow

    def draw(self, scr):
        pygame.draw.circle(scr, (self.color), (self.x, self.y), self.radius, width=1)

class Orb:
    def __init__(self, x, y, color=(255, 255, 255), container=None, tail_type='history'):
        self.x = x
        self.y = y
        self.color = color
        self.container = container 
        self.y_speed = 0
        self.x_speed = 0
        self.radius = 10 
        self.acc = 0.03
        self.tail = []
        self.counter = 0 
        self.history_tail_color = [0, 255, 0]
        self.comet_color = [139, 0, 0]
        self.color_idx = 0
        self.i = 0
        self.increasing = True
        self.update_interval = 10
        self.speed = 0
        self.tail_type = tail_type 
        self.gets_bigger = False

    def draw(self, scr):
        self.draw_tail(scr)
        pygame.draw.circle(scr, self.history_tail_color, (self.x, self.y), self.radius)
        pygame.draw.circle(scr, (255, 255, 255), (self.x, self.y), self.radius+1, width=1)
        
    def update_color(self):
        max_color_value = 255
        min_color_value = 0
        step = 1  

        if self.increasing:
            if self.history_tail_color[self.color_idx] < max_color_value:
                self.history_tail_color[self.color_idx] += step
            else:
                self.increasing = False
                self.color_idx = (self.color_idx + 1) % 3
        else:
            if self.history_tail_color[self.color_idx] > min_color_value:
                self.history_tail_color[self.color_idx] -= step
            else:
                self.increasing = True
                self.color_idx = (self.color_idx + 1) % 3

    def update_pos(self):
        self.y_speed += self.acc
        self.y += self.y_speed
        self.x += self.x_speed
        self.speed = math.sqrt(self.x_speed**2 + self.y_speed**2)
         
        # if self.speed_in_bounds(self.x_speed, self.y_speed):
        #     self.speed = math.sqrt(self.x_speed)

    def update_tail(self):        
        if self.tail_type == 'history':
            self.counter += 1
            
            if self.speed != 0:
                self.update_interval = max(1, int(30 / self.speed))

            if self.counter >= self.update_interval:
                self.update_color()
                self.tail.append((tuple(self.history_tail_color), (self.x, self.y)))
                self.counter = 0

        elif self.tail_type == 'comet':
            self.update_color()
            self.tail.append((tuple(self.history_tail_color), (self.x, self.y)))


    def check_collision(self):
        if self.container is None:
            return 
        dist_squared = (self.x - self.container.x)**2 + (self.y - self.container.y)**2
        if dist_squared >= (self.container.radius-self.radius) ** 2:
            sound.play()

            angle = math.atan2(self.y - self.container.y, self.x - self.container.x)

            self.x = self.container.x + (self.container.radius - self.radius) * math.cos(angle)
            self.y = self.container.y + (self.container.radius - self.radius) * math.sin(angle)

            normal_x = math.cos(angle)
            normal_y = math.sin(angle)

            dot = self.x_speed * normal_x + self.y_speed * normal_y

            self.x_speed = (self.x_speed - 2 * dot * normal_x)  
            self.y_speed = (self.y_speed - 2 * dot * normal_y) 
    
            speed = self.speed_in_bounds(self.x_speed, self.y_speed*1.03) 
            if speed:
                self.y_speed *= 1.06

            #turn on if you want the circle to increase in size after each collision
            if self.gets_bigger:
                if self.radius < self.container.radius:
                    self.radius += 1

    def draw_tail(self, scr):
        if self.tail_type == 'history':
            if len(self.tail) >= 5000:
                print('reduced trail')
                self.tail = self.tail[-4000:]
            for p in self.tail:
                pygame.draw.circle(scr, p[0], p[1], self.radius)
                pygame.draw.circle(scr, (255, 255, 255), p[1], self.radius+1, width=1)

        elif self.tail_type == 'comet':
            if len(self.tail) > 40:
                self.tail = self.tail[-40:]
            for i, p in enumerate(self.tail):
                pygame.draw.circle(scr, p[0], p[1], self.radius-(40-i))


    def speed_in_bounds(self, x_speed, y_speed):
        speed = math.sqrt(x_speed**2 + y_speed**2)
        return speed < 40 
    
    def update(self):
        self.check_collision()
        self.update_pos()
        self.update_tail()

    # def loop(self, screen):
    #     self.draw(screen)


    
