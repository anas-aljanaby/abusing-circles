import pygame
from graphics import CircleContainer, Orb
import random
from ui_manager import UIManager, Button
from game import Game

pygame.init()

clock = pygame.time.Clock()

game = Game(play_sound=True)
ui_manager = UIManager(game)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           running = False
        ui_manager.handle_event(event)

    game.draw()
    ui_manager.draw()

    fps = clock.get_fps()
    font = pygame.font.Font(None, 30)
    fps_text = font.render(f"FPS: {fps:.2f}", True, pygame.Color('white'))
    speed_text = font.render(f'Speed {game.orb.speed:.2f}', True, pygame.Color('white'))
    size_text = font.render(f'Size {game.orb.radius:.2f}', True, pygame.Color('white'))
    game.screen.blit(fps_text, (10, 10))
    game.screen.blit(speed_text, (10, 30))
    game.screen.blit(size_text, (10, 50))

    pygame.display.update()

    clock.tick(60)

pygame.quit()
