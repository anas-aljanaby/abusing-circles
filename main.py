import pygame
from graphics import CircleContainer, Orb

pygame.init()
screen = pygame.display.set_mode([1200, 800])

circle = CircleContainer(600, 400)
orb = Orb(600, 400, container=circle)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    circle.draw(screen)    
    orb.draw(screen)
    orb.update_pos()
    pygame.display.flip()

pygame.quit()









