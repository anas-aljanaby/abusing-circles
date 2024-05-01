import pygame
from pygame import mixer
from graphics import CircleContainer, Orb
import random 
import math
import time

class Game:
    def __init__(self, play_sound=False):
        self.container = CircleContainer(600, 400)
        self.running = False
        self.screen = pygame.display.set_mode((1200, 800))
        self.orb = None
        self.increase_orb_size = False
        self.play_sound = play_sound 
        if self.play_sound:
            mixer.init()
            self.sound = pygame.mixer.Sound('ball_hit.mp3')
        self.create_orb()


    def get_squared_distance(self):
        if not self.orb:
            return 
        return (self.orb._x - self.container._x) ** 2 + (self.orb._y - self.container._y) ** 2

    def check_collision(self):
        squared_distance = self.get_squared_distance()
        if not self.orb or not squared_distance:
            return 

        if squared_distance >= (self.container.radius - self.orb.radius) ** 2:
            if self.play_sound:
                self.sound.play()

            angle = math.atan2(self.orb.y - self.container.y, self.orb.x - self.container.x)
            normal_x = math.cos(angle)
            normal_y = math.sin(angle)

            self.orb.x = self.container.x + (self.container.radius - self.orb.radius) * normal_x
            self.orb.y = self.container.y + (self.container.radius - self.orb.radius) * normal_y

            dot = self.orb._x_speed * normal_x + self.orb._y_speed * normal_y

            self.orb.x_speed = (self.orb.x_speed - 2 * dot * normal_x)  
            self.orb.y_speed = (self.orb.y_speed - 2 * dot * normal_y) 
            y_speed = self.orb.y_speed * 1.06
            if (self.orb.x_speed ** 2 + self.orb.y_speed ** 2) < 1600:
                self.orb.y_speed = y_speed
 
            if self.increase_orb_size:
                if self.orb.radius < self.container.radius:
                    self.orb.radius += 1

                else:
                    time.sleep(2)
                    self.create_orb(running=True)

    def speed_in_bounds(self, x_speed, y_speed):
        speed = math.sqrt(x_speed**2 + y_speed**2)
        return speed < 40 

    def create_orb(self, running=False):
        self.orb = Orb(random.randint(500, 700), random.randint(300, 500),
                        tail_type='comet')
        self.running = running

    def play_game(self):
        self.running = True

    def reset_game(self, running=False):
        self.create_orb(running=running)
       
    def toggle_size_increase(self):
        if not self.running:
            self.increase_orb_size = not self.increase_orb_size
        
    def handle_event(self, event):
        if event.lower() == 'play':
            self.play_game()
        elif event.lower() == 'reset':
            self.reset_game()
        elif event == 'size_increase':
            self.toggle_size_increase() 

    def draw(self):
        if self.orb is None:
            return 
        self.screen.fill((0, 0, 0))

        self.container.draw(self.screen)


        if self.running:
            self.check_collision()
            self.orb.update()

        self.orb.draw(self.screen)


