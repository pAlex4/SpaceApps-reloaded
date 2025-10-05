import pygame
from dropdown_menu import DropdownMenu
from button import ToggleButton
from rotate_button import RotateButton

class TopBar:
    def __init__(self, width, height=40):
        self.width = width
        self.height = height
        self.bg_color = (50, 50, 50)
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 20)

        options = [f"Option {i}" for i in range(20)]
        self.dropdown = DropdownMenu(10, 5, 150, 30, options, self.font)

        button_options = ["draw", "remove"]
        self.toggle_button = ToggleButton(180, 5, 100, 30, button_options, self.font)

        self.rotate_button = RotateButton(290, 5, 30, self.font)

    def handle_event(self, event):
        self.dropdown.handle_event(event)
        self.toggle_button.handle_event(event)
        self.rotate_button.handle_event(event)

    def draw(self, surface):
        pygame.draw.rect(surface, self.bg_color, (0, 0, self.width, self.height))
        self.dropdown.draw(surface)
        self.toggle_button.draw(surface)
        self.rotate_button.draw(surface)
