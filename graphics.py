import pygame
import math
import random

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


class Particle:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.color = (255, 255, 255)
        self.lifespan = random.randint(10, 20)
        angle = random.uniform(0, 2 * math.pi)
        speed = 1
        self.x_speed = speed * math.cos(angle)
        self.y_speed = speed * math.sin(angle)

    def update(self):
        self.x += self.x_speed
        self.y += self.y_speed
        self.lifespan -= 1

    def draw(self, screen, color):
        if self.lifespan > 0:
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)

class Orb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.y_speed = 0
        self.x_speed = 0
        self.radius = 10 
        self._acc = 0.1
        self._tail = []
        self._counter = 0 
        self._history_tail_color = [0, 255, 0]
        self._color_idx = 0
        self._increasing_color = True
        self._update_interval = 10
        self.speed = 0

    def draw(self, scr):
        pygame.draw.circle(scr, self._history_tail_color, (self.x, self.y), self.radius)
        pygame.draw.circle(scr, (255, 255, 255), (self.x, self.y), self.radius + 1, width=2)

    def update_color(self):
        max_color_value = 255
        min_color_value = 0
        step = 1  

        if self._increasing_color:
            if self._history_tail_color[self._color_idx] < max_color_value:
                self._history_tail_color[self._color_idx] += step
            else:
                self._increasing_color = False
                self._color_idx = (self._color_idx + 1) % 3
        else:
            if self._history_tail_color[self._color_idx] > min_color_value:
                self._history_tail_color[self._color_idx] -= step
            else:
                self._increasing_color = True
                self._color_idx = (self._color_idx + 1) % 3

    def update_pos(self):
        self.y_speed += self._acc
        self.y += self.y_speed
        self.x += self.x_speed
        self.speed = math.sqrt(self.x_speed**2 + self.y_speed**2)

    def update_tail(self):
        self.update_color()
        self._tail.append((tuple(self._history_tail_color), (self.x, self.y)))

    def draw_tail(self, scr):
        for i, p in enumerate(self._tail[-10:]):
            surface = pygame.Surface((1200, 800), pygame.SRCALPHA)
            color = p[0]  + (0 + (i*25),)
            pygame.draw.circle(surface, color, p[1], self.radius)
            pygame.draw.circle(surface, (0, 0, 0), p[1], self.radius + 1, width=1)
            scr.blit(surface, (0, 0))

    def update(self):
        self.update_pos()
        self.update_tail()

