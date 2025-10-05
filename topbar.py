import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
BLUE = (50, 100, 200)

class ToggleButton:
    def __init__(self, position, size, font, options=None):
        self.rect = pygame.Rect(position, size)
        self.font = font
        self.options = options if options else []
        self.current_index = 0
        self.is_open = False

        self.bg_color = GRAY
        self.text_color = BLACK
        self.highlight_color = BLUE

    def set_options(self, options_list):
        self.options = options_list
        self.current_index = 0

    def get_current_option(self):
        if self.options:
            return self.options[self.current_index]
        return None

    def toggle(self):
        if len(self.options) == 2:
            self.current_index = 1 - self.current_index

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if len(self.options) == 2:
                    self.toggle()
                else:
                    self.is_open = not self.is_open
            elif self.is_open:
                for i, option in enumerate(self.options):
                    option_rect = pygame.Rect(
                        self.rect.x,
                        self.rect.y + self.rect.height * (i + 1),
                        self.rect.width,
                        self.rect.height)
                    if option_rect.collidepoint(event.pos):
                        self.current_index = i
                        self.is_open = False
                        break
                else:
                    self.is_open = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.bg_color, self.rect)
        text = self.get_current_option() or ""
        text_surface = self.font.render(text, True, self.text_color)
        surface.blit(text_surface, (self.rect.x + 5, self.rect.y + (self.rect.height - text_surface.get_height()) // 2))

        if len(self.options) > 2:
            pygame.draw.polygon(surface, self.text_color,
                                [(self.rect.right - 15, self.rect.y + self.rect.height // 3),
                                 (self.rect.right - 5, self.rect.y + self.rect.height // 3),
                                 (self.rect.right - 10, self.rect.y + self.rect.height * 2 // 3)])

            if self.is_open:
                for i, option in enumerate(self.options):
                    option_rect = pygame.Rect(
                        self.rect.x,
                        self.rect.y + self.rect.height * (i + 1),
                        self.rect.width,
                        self.rect.height)
                    pygame.draw.rect(surface, self.bg_color, option_rect)
                    option_text = self.font.render(option, True, self.text_color)
                    surface.blit(option_text, (option_rect.x + 5, option_rect.y + (option_rect.height - option_text.get_height()) // 2))
                    if option_rect.collidepoint(pygame.mouse.get_pos()):
                        pygame.draw.rect(surface, self.highlight_color, option_rect, 2)

class TopBar:
    def __init__(self, screen_width, height=40):
        self.height = height
        self.bg_color = (50, 50, 50)
        self.font = pygame.font.SysFont(None, 24)

        button_width = 100
        button_height = 30
        button_x = 10
        button_y = (height - button_height) // 2

        self.draw_remove_toggle = ToggleButton(
            (button_x, button_y),
            (button_width, button_height),
            self.font,
            options=["Draw", "Remove"]
        )

        dropdown_width = 80
        dropdown_height = 30
        dropdown_x = screen_width - dropdown_width - 10
        dropdown_y = button_y

        self.toggle_button = ToggleButton(
            (dropdown_x, dropdown_y),
            (dropdown_width, dropdown_height),
            self.font,
            options=["1x1", "2x2", "3x1", "4x4"]
        )

    def handle_event(self, event):
        self.draw_remove_toggle.handle_event(event)
        self.toggle_button.handle_event(event)

    def draw(self, surface, money=0):
        pygame.draw.rect(surface, self.bg_color, (0, 0, surface.get_width(), self.height))
        self.draw_remove_toggle.draw(surface)
        self.toggle_button.draw(surface)

        money_text = self.font.render(f"Money: ${money}", True, (255, 255, 255))
        text_rect = money_text.get_rect()
        
        # Center text horizontally and vertically in the topbar
        center_x = surface.get_width() // 2
        center_y = self.height // 2
        text_rect.center = (center_x, center_y)
        
        surface.blit(money_text, text_rect)
