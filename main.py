import pygame
from ui_manager import UIManager
from game import Game
import cProfile
import pstats
import argparse


def handle_events(ui_manager):
    """
    Handle all Pygame events.

    Args:
        ui_manager (UIManager): The UIManager instance to handle events.

    Returns:
        bool: False if quit event is detected, True otherwise.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        ui_manager.handle_event(event)
    return True


def render_text(text, pos, screen, font):
    """
    Render text on the screen.

    Args:
        text (str): The text to render.
        pos (tuple): The position to render the text (x, y).
        screen (pygame.Surface): The screen surface to draw the text on.
        font (pygame.font.Font): The font to use for rendering the text.
    """
    text_surface = font.render(text, True, pygame.Color('white'))
    screen.blit(text_surface, pos)


def main(silent=False):
    pygame.init()
    font = pygame.font.Font(None, 30)

    clock = pygame.time.Clock()
    game = Game(silent=silent)
    ui_manager = UIManager(game)
    running = True

    while running:
        running = handle_events(ui_manager)
        game.update_draw()
        ui_manager.draw()

        fps = clock.get_fps()
        render_text(f'FPS: {fps:.2f}', (10, 10), game.screen, font)
        render_text(f'Speed {game.orb.speed:.2f}', (10, 30), game.screen, font)
        render_text(f'Size {game.orb.radius:.2f}', (10, 50), game.screen, font)
        render_text('Upon collision: ', (10, 175), game.screen, font)
        render_text('Container: ', (10, 270), game.screen, font)

        pygame.display.update()
        clock.tick(120)

    pygame.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--silent', '-s', action='store_true', help='Turn off sound')
    parser.add_argument('--profile', '-p', action='store_true', help='Enable Profiling')
    args = parser.parse_args()

    if args.profile:
        profiler = cProfile.Profile()
        profiler.enable()

    main(silent=args.silent)

    if args.profile:
        profiler.disable()
        stats = pstats.Stats(profiler).sort_stats('cumulative')
        stats.print_stats()
