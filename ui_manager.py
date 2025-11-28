import pygame

OFF_WHITE = (225, 225, 225)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
RED = (255, 0, 0)
DARK_RED = (200, 0, 0)


class Button:
    def __init__(self, x, y, width, height, text='', action=None,
                 color='white', font_color='black'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.font_color = font_color
        self.font = pygame.font.SysFont(None, 30)
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect, 0)
        if self.text != '':
            text = self.font.render(self.text, True, self.font_color)
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def is_over(self, pos):
        if self.rect.collidepoint(pos):
            return True
        return False


class ToggleButton(Button):
    color_on = (0, 200, 0)
    color_off = (200, 0, 0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_on = False

    def draw(self, win):
        color = self.color_on if self.is_on else self.color_off
        if self.text in ['Static', 'Dynamic']:
           self.text = 'Dynamic' if self.is_on else 'Static' 
        pygame.draw.rect(win, color, self.rect, 0)
        if self.text != '':
            text = self.font.render(self.text, True, self.font_color)
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def toggle(self):
        self.is_on = not self.is_on

class UIManager:
    def __init__(self, game):
        self.buttons = []
        self.toggle_buttons = []
        self.game = game
        self.create_buttons()
        for bt in self.buttons:
            bt.draw(self.game.screen)

    def create_buttons(self):
        button_configs = [
            {'x': 10, 'y': 100, 'width': 80, 'height': 20, 'label': 'Play', 'action': 'play' },
            {'x': 10, 'y': 122, 'width': 80, 'height': 20, 'label': 'Reset', 'action': 'reset'}, 
        ]
        toggle_button_configs = [
            {'x': 10, 'y': 200, 'width': 100, 'height': 25, 'label': 'Size++',
             'action': 'size_increase'},
            {'x': 10, 'y': 230, 'width': 100, 'height': 25, 'label': 'Speed++',
             'action': 'speed_increase'},
            {'x': 10, 'y': 290, 'width': 100, 'height': 25, 'label': 'Static',
             'action': 'toggle_container'}
        ]
        for config in button_configs:
            self.buttons.append(Button(config['x'], config['y'], config['width'], config['height'], config['label'], action=config['action']))
        for config in toggle_button_configs:
            bt = ToggleButton(config['x'], config['y'], config['width'], config['height'], config['label'], action=config['action'])
            self.buttons.append(bt)
            self.toggle_buttons.append(bt)

    def add_button(self, x, y, width, height, label, action):
        self.buttons.append(Button(x, y, width, height, label, action=action))

    def draw(self):
        for bt in self.buttons:
            bt.draw(self.game.screen)

    def reset(self):
        for bt in self.toggle_buttons:
            bt.action(bt.is_on())

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for bt in self.buttons:
                if bt.is_over(pygame.mouse.get_pos()):
                    if type(bt) == ToggleButton:
                        if not self.game.running:
                            bt.toggle()
                            bt.draw(self.game.screen)
                    self.game.handle_event(bt.action)
