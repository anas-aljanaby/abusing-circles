import pygame
from pygame import mixer
from graphics import CircleContainer, Orb, Particle
import random
import math
import time

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
CONT_WIDTH = SCREEN_WIDTH / 2
CONT_HEIGHT = SCREEN_HEIGHT / 2
MIN_SPEED_FOR_ROTATION = 10
ROTATION_PROBABILITY = 0.9
MIN_ROTATION_ANGLE = 5
MAX_ROTATION_ANGLE = 15


class Game:
    def __init__(self, play_sound=False, radius=350, speed_boost=1.06,
                 max_square_speed=1600):
        self.prev_cont = time.time()
        self.cur_cont = 0
        self.orb_out = False
        self.dynamic_cont = False
        self.screen_width = 1200 
        self.screen_height = 800
        self.cont_width = self.screen_width / 2
        self.cont_height = self.screen_height / 2 
        self.radius = radius 
        self.screen = pygame.display.set_mode((self.screen_width,
                                               self.screen_height))
        self.container = CircleContainer(self.cont_width,
                                         self.cont_height, radius=self.radius)
        self.containers = [self.container]
        self.speed_boost = speed_boost
        self.max_square_speed = max_square_speed
        self.running = False
        self.orb = self.create_orb()
        self.increase_orb_size = False
        self.increase_speed = False
        self.play_sound = play_sound 
        self.particles = []
        if self.play_sound:
            mixer.init()
            self.sound = pygame.mixer.Sound('ball_hit.mp3')

    def square_dist_to_container(self, cont):
        return (self.orb.x - cont.x) ** 2 + (self.orb.y - cont.y) ** 2

    def check_collision(self):
        if not self.containers:
            return 
        cont = self.containers[0]
        squared_distance = self.square_dist_to_container(cont)

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
                self.boost_orb_speed()

            if self.increase_orb_size:
                self.grow_orb(cont)

            if self.orb.speed > MIN_SPEED_FOR_ROTATION:
                if random.random() > ROTATION_PROBABILITY:
                    self.orb.x_speed, self.orb.y_speed = self.rotate_vector(
                        self.orb.x_speed, self.orb.y_speed,
                        random.uniform(MIN_ROTATION_ANGLE, MAX_ROTATION_ANGLE))

            if self.dynamic_cont:
                self.containers.pop(0)

            self.create_particles()

    def boost_orb_speed(self):
        y_speed = self.orb.y_speed * self.speed_boost 
        if (self.orb.x_speed ** 2 + self.orb.y_speed ** 2) < self.max_square_speed:
            self.orb.y_speed = y_speed

    def grow_orb(self, cont):
        if self.orb.radius >= cont.radius:
            time.sleep(2)
            self.create_orb(running=True)
        else:
            self.orb.radius += 1

    def is_orb_out(self):
        if self.containers:
            cont = self.containers[-1]
        else:
            cont = CircleContainer(self.cont_width, self.cont_height, radius=self.radius)

        squared_dist = self.square_dist_to_container(cont)
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
        self.container = CircleContainer(self.cont_width, self.cont_height, radius=self.radius)
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
                    self.containers.insert(0, CircleContainer(self.cont_width, self.cont_height, radius=self.containers[0].radius-2))
                except IndexError:
                    self.containers.insert(0, CircleContainer(self.cont_width, self.cont_height, radius=self.radius))
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
