import pygame
from pygame import mixer
from graphics import CircleContainer, Orb, Particle
import random
import math
import time


class Game:
    def __init__(self, play_sound=False):
        self.prev_cont = time.time()
        self.cur_cont = 0
        self.orb_out = False
        self.dynamic_cont = False
        self.container = CircleContainer(600, 400, radius=200)
        self.containers = [self.container]
        self.speed_mult = 1.06
        self.max_speed = 1600
        self.running = False
        self.screen = pygame.display.set_mode((1200, 800))
        self.orb = self.create_orb()
        self.increase_orb_size = False
        self.increase_speed = False
        self.play_sound = play_sound 
        self.particles = []
        if self.play_sound:
            mixer.init()
            self.sound = pygame.mixer.Sound('ball_hit.mp3')

    def add_containers(self, n, sep_width=2):
        if len(self.containers):
            starting_r = self.containers[-1].radius
        else:
            starting_r = 300 
        for i in range(1, n+1):
            self.containers.append(CircleContainer(600, 400, radius=starting_r + (i*sep_width)))

    def get_squared_distance(self, cont):
        return (self.orb.x - cont.x) ** 2 + (self.orb.y - cont.y) ** 2

    def check_collision(self):
        if not self.containers:
            return 
        cont = self.containers[0]
        squared_distance = self.get_squared_distance(cont)

        if squared_distance >= (cont.radius - self.orb.radius) ** 2:
            if self.play_sound:
                self.sound.play()

            angle = math.atan2(self.orb.y - cont.y, self.orb.x - cont.x)
            normal_x = math.cos(angle)
            normal_y = math.sin(angle)

            self.orb.x = cont.x + (cont.radius - self.orb.radius) * normal_x
            self.orb.y = cont.y + (cont.radius - self.orb.radius) * normal_y

            dot = self.orb.x_speed * normal_x + self.orb.y_speed * normal_y

            self.orb.x_speed = (self.orb.x_speed - 2 * dot * normal_x)  
            self.orb.y_speed = (self.orb.y_speed - 2 * dot * normal_y) 

            if self.increase_speed:
                y_speed = self.orb.y_speed * self.speed_mult 
                if (self.orb.x_speed ** 2 + self.orb.y_speed ** 2) < self.max_speed:
                    self.orb.y_speed = y_speed

            if self.increase_orb_size:
                if self.orb.radius < cont.radius:
                    self.orb.radius += 1
                else:
                    time.sleep(2)
                    self.create_orb(running=True)

            if self.orb.speed > 10:
                if random.random() > 0.9:
                     self.orb.x_speed, self.orb.y_speed = self.rotate_vector(
                        self.orb.x_speed, self.orb.y_speed,
                        random.uniform(5, 15))

            if self.dynamic_cont:
                self.containers.pop(0)

            self.create_particles()

    def is_orb_out(self):
        if self.containers:
            cont = self.containers[-1]
        else:
            cont = CircleContainer(600, 400, radius=200)

        squared_dist = self.get_squared_distance(cont)
        if squared_dist >= (cont.radius + self.orb.radius)**2:
            self.orb_out = True
        if squared_dist >= 700_000: #(cont.radius + self.orb.radius)**2: # - self.orb.radius)**2 + 10000:
            self.running = False

    def rotate_vector(self, vx, vy, angle):
        radians = math.radians(angle)
        cos_angle = math.cos(radians)
        sin_angle = math.sin(radians)
        new_vx = vx * cos_angle - vy * sin_angle
        new_vy = vx * sin_angle + vy * cos_angle
        return new_vx, new_vy

    def speed_in_bounds(self, x_speed, y_speed):
        speed = math.sqrt(x_speed**2 + y_speed**2)
        return speed < 40 

    def create_orb(self, running=False):
        self.running = running
        return Orb(random.randint(500, 700), random.randint(300, 500))

    def play_game(self):
        self.running = True

    def reset_game(self, running=False):
        self.orb = self.create_orb(running=running)
        self.containers = []
        self.container = CircleContainer(600, 400, radius=200)
        self.containers = [self.container]
        self.orb_out = False

    def toggle_size_increase(self):
        if not self.running:
            self.increase_orb_size = not self.increase_orb_size

    def toggle_speed_increase(self):
        if not self.running:
            self.increase_speed = not self.increase_speed

    def toggle_container(self):
        self.dynamic_cont = not self.dynamic_cont

    def handle_event(self, event):
        if event.lower() == 'play':
            self.play_game()
        elif event.lower() == 'reset':
            self.reset_game()
        elif event == 'size_increase':
            self.toggle_size_increase() 
        elif event == 'speed_increase':
            self.toggle_speed_increase()
        elif event == 'toggle_container':
            self.toggle_container()

    def update_container(self):
        if self.dynamic_cont and not self.orb_out:
            if  time.time() - self.prev_cont > 0.7:
                try:
                    self.containers.insert(0, CircleContainer(600, 400, radius=self.containers[0].radius-2))
                except IndexError:
                    self.containers.insert(0, CircleContainer(600, 400, radius=200))
                self.prev_cont = time.time()

    def draw(self):
        self.screen.fill((0, 0, 0))
        for cont in self.containers:
            cont.draw(self.screen)
        self.orb.draw(self.screen)
        if self.orb._tail:
            for pt in self.particles:
                pt.draw(self.screen, self.orb._tail[-1][0])

    def create_particles(self):
        num_particles = 5 
        self.particles = []
        for _ in range(num_particles):
            particle = Particle(self.orb.x, self.orb.y, 1)
            self.particles.append(particle)

    def update_particles(self):
        for particle in self.particles[:]:
            particle.update()
            if particle.lifespan <= 0:
                self.particles.remove(particle)

    def update(self):
        self.update_container()
        self.orb.update()
        self.is_orb_out()
        self.check_collision()
        self.update_particles()

    def update_draw(self):
        self.draw()

        if self.running:
            self.update()
