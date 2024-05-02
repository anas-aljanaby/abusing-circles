import pygame
import pygame.gfxdraw
import math


class CircleContainer:
    def __init__(self, x, y, color='white', radius=300, shadow=True):
        self._x = x
        self._y = y
        self._radius = radius 
        self.color = color
        self.shadow = shadow

    def draw(self, scr):
        pygame.draw.circle(scr, (self.color), (self._x, self._y), self._radius, width=1)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def radius(self):
        return self._radius
    
class Orb:
    def __init__(self, x, y, color=(255, 255, 255), tail_type='history'):
        self._x = x
        self._y = y
        self.color = color
        self._y_speed = 0
        self._x_speed = 0
        self._radius = 10 
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
    
    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def radius(self):
        return self._radius
   
    @x.setter
    def x(self, value):
        self._x = value

    @y.setter
    def y(self, value):
        self._y = value

    @radius.setter
    def radius(self, value):
        self._radius = value

    @property
    def x_speed(self):
        return self._x_speed
   
    @x_speed.setter
    def x_speed(self, value):
        self._x_speed = value

    @property
    def y_speed(self):
        return self._y_speed
   
    @y_speed.setter
    def y_speed(self, value):
        self._y_speed = value

    def draw(self, scr):
        self.draw_tail(scr)
        pygame.draw.circle(scr, self.history_tail_color, (self._x, self._y), self._radius)
        pygame.draw.circle(scr, (255, 255, 255), (self._x, self._y), self._radius+1, width=1)
        
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
        self._y_speed += self.acc
        self._y += self._y_speed
        self._x += self._x_speed
        self.speed = math.sqrt(self._x_speed**2 + self._y_speed**2)

    def update_tail(self):
        if self.tail_type == 'history':
            self.counter += 1
            
            if self.speed != 0:
                self.update_interval = max(1, int(30 / self.speed))

            if self.counter >= self.update_interval:
                self.update_color()
                self.tail.append((tuple(self.history_tail_color), (self._x, self._y)))
                self.counter = 0

        elif self.tail_type == 'comet':
            self.update_color()
            self.tail.append((tuple(self.history_tail_color), (self._x, self._y)))

    def draw_tail(self, scr):
        if self.tail_type == 'history':
            if len(self.tail) >= 5000:
                print('reduced trail')
                self.tail = self.tail[-4000:]
            for p in self.tail:
                pygame.draw.circle(scr, p[0], p[1], self._radius)
                pygame.draw.circle(scr, (255, 255, 255), p[1], self._radius+1, width=1)

        elif self.tail_type == 'comet':
            if len(self.tail) > 40:
                self.tail = self.tail[-40:]
            for i, p in enumerate(self.tail):
                pygame.draw.circle(scr, p[0], p[1], self._radius-(40-i))

    def update(self):
        self.update_pos()
        self.update_tail()


    
