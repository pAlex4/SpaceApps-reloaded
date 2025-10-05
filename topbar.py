import pygame

class TopBar:
    def __init__(self, width, height=40):
        self.width = width
        self.height = height
        self.widgets = ["Widget1", "Widget2", "Widget3"]  # Placeholder widgets
        self.bg_color = (50, 50, 50)
        self.text_color = (255, 255, 255)
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 20)

    def draw(self, surface):
        # Draw background
        pygame.draw.rect(surface, self.bg_color, (0, 0, self.width, self.height))
        # Draw widgets as text
        x = 10
        for widget in self.widgets:
            text_surf = self.font.render(widget, True, self.text_color)
            surface.blit(text_surf, (x, 10))
            x += text_surf.get_width() + 20
