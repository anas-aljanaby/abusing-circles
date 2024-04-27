import pygame

OFF_WHITE = (225, 225, 225)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
RED = (255, 0, 0)
DARK_RED = (200, 0, 0)

class Button:
    def __init__(self, x, y, width, height, text='', action=None, color='white', highlight_color=OFF_WHITE, font_color='black'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.original_color = color
        self.highlight_color = highlight_color
        self.font_color = font_color
        self.font = pygame.font.SysFont(None, 30)
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
        
        pygame.draw.rect(win, self.color, self.rect, 0)
        
        if self.text != '':
            text = self.font.render(self.text, True, self.font_color)
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def is_over(self, pos):
        if self.rect.collidepoint(pos):
            self.color = self.highlight_color
            return True
        self.color = self.original_color
        return False


class UIManager:
    def __init__(self, screen, play_callback, pause_callback, reset_callback):
        self.screen = screen
        self.running = False
        self.buttons = [
            Button(10, 100, 80, 20, 'Play', action=play_callback),
            Button(10, 122, 80, 20, 'Pause', action=pause_callback),
            Button(10, 144, 80, 20, 'Reset', action=reset_callback),
        ]

    def draw(self):
        for bt in self.buttons:
            bt.is_over(pygame.mouse.get_pos())
            bt.draw(self.screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for bt in self.buttons:
                if bt.is_over(pygame.mouse.get_pos()):
                    bt.action()





