import pygame
from tile import *

WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
DARK_GRAY = (40, 40, 40)
GREEN = (50, 200, 100)
BROWN = (180, 120, 60)


class WorldGeneration:
    def __init__(self, screen_width=800, screen_height=600, tile_size=64):
        self._screen_width = screen_width
        self._screen_height = screen_height
        self._tile_size = tile_size
        self.tiles = {}

    # --- Métodos públicos para modificar el mundo ---
    def add_tile(self, gx, gy, color=BROWN):
        if (gx, gy) not in self.tiles:
            self.tiles[(gx, gy)] = Tile(gx, gy, self._tile_size, color)

    def remove_tile(self, gx, gy):
        if (gx, gy) in self.tiles:
            del self.tiles[(gx, gy)]

    # --- Métodos de dibujo ---
    def draw_grid(self, surface, camera):
        """Dibuja el grid visible"""
        start_x = int(camera.x // self._tile_size) - 1
        end_x = int((camera.x + self._screen_width) // self._tile_size) + 2
        start_y = int(camera.y // self._tile_size) - 1
        end_y = int((camera.y + self._screen_height) // self._tile_size) + 2

        for gx in range(start_x, end_x):
            for gy in range(start_y, end_y):
                wx = gx * self._tile_size
                wy = gy * self._tile_size
                sx, sy = camera.transform_coordinate((wx, wy))
                rect = pygame.Rect(sx, sy, self._tile_size, self._tile_size)
                pygame.draw.rect(surface, GRAY, rect, 1)

    def draw_tiles(self, surface, camera):
        for tile in self.tiles.values():
            tile.update_position(camera, self._tile_size)
            surface.blit(tile.image, tile.rect)

    # --- Getters opcionales si quieres acceder desde fuera ---
    @property
    def tile_size(self):
        return self._tile_size

    @property
    def screen_size(self):
        return (self._screen_width, self._screen_height)
