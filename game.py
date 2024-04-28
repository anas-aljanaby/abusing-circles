import pygame
from ui_manager import UIManager, Button
from graphics import CircleContainer, Orb
import random 
# random.seed(0)

class Game:
    def __init__(self):
        self.container = CircleContainer(600, 400)
        self.running = False
        self.screen = pygame.display.set_mode((1200, 800))
        self.create_orb()
        # self.ui_manager = UIManager(self.screen, self.play_game, self.pause_game, self.reset_game)

    def create_orb(self):
        self.orb = Orb(random.randint(500, 700), random.randint(300, 500),
                       container=self.container, tail_type='comet', )
 
    def play_game(self):
        self.running = True

    def pause_game(self):
        self.running = False

    def reset_game(self):
        self.create_orb()
        
       
    def toggle_size_increase(self):
        if not self.running:
            self.orb.gets_bigger = not self.orb.gets_bigger
        print(self.running)
        print(self.orb.gets_bigger) 
        
    def handle_event(self, event):
        if event.lower() == 'play':
            self.play_game()
        elif event.lower() == 'pause':
            self.pause_game()
        elif event.lower() == 'reset':
            self.reset_game()
        elif event == 'size_increase':
            self.toggle_size_increase() 

    def draw(self):
        self.screen.fill((0, 0, 0))

        self.container.draw(self.screen)

        if self.running:
            self.orb.update()

        self.orb.draw(self.screen)

    


