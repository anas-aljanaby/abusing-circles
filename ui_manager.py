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


class ToggleButton(Button):
    color_on = (0, 200, 0)
    color_off = (200, 0, 0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_on = False

    def draw(self, win, outline=None):
        color = self.color_on if self.is_on else self.color_off
        if outline:
            pygame.draw.rect(win, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
        
        pygame.draw.rect(win, color, self.rect, 0)
        
        if self.text != '':
            text = self.font.render(self.text, True, self.font_color)
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def toggle(self):
        self.is_on = not self.is_on


class UIManager:
    def __init__(self, game):
        # self.running = False
        self.buttons = []
        self.game = game
        self.create_buttons()

    
    def create_buttons(self):
        button_configs = [
            {'x': 10, 'y': 100, 'width': 80, 'height': 20, 'label': 'Play', 'action': 'play' },
            {'x': 10, 'y': 122, 'width': 80, 'height': 20, 'label': 'Pause', 'action': 'pause'},
            {'x': 10, 'y': 144, 'width': 80, 'height': 20, 'label': 'Reset', 'action': 'reset'}, 
        ]
        toggle_button_configs = [
            {'x': 10, 'y': 166, 'width': 80, 'height': 20, 'label': 'Size++', 'action': 'size_increase'}

        ]

        for config in button_configs:
            self.buttons.append(Button(config['x'], config['y'], config['width'], config['height'], config['label'], action=config['action']))
        for config in toggle_button_configs:
            self.buttons.append(ToggleButton(config['x'], config['y'], config['width'], config['height'], config['label'], action=config['action']))

    def add_button(self, x, y, width, height, label, action):
        self.buttons.append(Button(x, y, width, height, label, action=action))

    def draw(self):
        for bt in self.buttons:
            bt.is_over(pygame.mouse.get_pos())
            bt.draw(self.game.screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for bt in self.buttons:
                if bt.is_over(pygame.mouse.get_pos()):
                    if type(bt) == ToggleButton:
                        if not self.game.running:
                            bt.toggle()

                    #TODO fix this, reset button should not reset the users choices but only the game state, for now 
                    # must do this to be consistent with the game class
                    if bt.action == 'reset':
                        self.buttons[-1].is_on = False                        
                    ####

                    self.game.handle_event(bt.action)





