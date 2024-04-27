import pygame
from ui_manager import UIManager, Button
from graphics import CircleContainer, Orb

class Game:
    def __init__(self):
        self.container = CircleContainer(600, 400)
        self.orb = Orb(640, 400, container=self.container)

        self.running = False
        self.screen = pygame.display.set_mode((1200, 800))
        self.ui_manager = UIManager(self.screen, self.play_game, self.pause_game, self.reset_game)

    def play_game(self):
        self.running = True

    def pause_game(self):
        self.running = False

    def reset_game(self):
        self.orb = Orb(640, 400, container=self.container)


    def draw(self):
        self.screen.fill((0, 0, 0))

        self.container.draw(self.screen)
        self.ui_manager.draw()

        if self.running:
            self.orb.update()

        self.orb.draw(self.screen)
