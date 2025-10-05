import pygame
GRAY = (180, 180, 180)
class Tile(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y, size, color=GRAY):
        super().__init__()
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.color = color
        self.image = pygame.Surface((size, size))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

    def update_position(self, camera, size):
        wx = self.grid_x * size
        wy = self.grid_y * size
        sx, sy = camera.transform_coordinate((wx, wy))
        self.rect.topleft = (sx, sy)
