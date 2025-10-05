import pygame
from tile import *

GRAY = (180, 180, 180)
BROWN = (180, 120, 60)

class WorldGeneration:
    def __init__(self, screen_width=800, screen_height=600, topbar_height=40, grid_size=25):
        self._screen_width = screen_width
        self._screen_height = screen_height
        self.grid_size = grid_size
        self.topbar_height = topbar_height

        available_height = self._screen_height - self.topbar_height
        tile_size_vert = available_height / self.grid_size
        tile_size_horz = self._screen_width / self.grid_size
        self._tile_size = int(min(tile_size_vert, tile_size_horz))

        self.tiles = {}

    def add_tile(self, gx, gy, color=BROWN):
        if (gx, gy) not in self.tiles:
            self.tiles[(gx, gy)] = Tile(gx, gy, self._tile_size, color)

    def remove_tile(self, gx, gy):
        if (gx, gy) in self.tiles:
            del self.tiles[(gx, gy)]

    def draw_grid(self, surface, camera, topbar_height):
        tile_size = self._tile_size

        for gx in range(self.grid_size):
            for gy in range(self.grid_size):
                wx = gx * tile_size
                wy = gy * tile_size + topbar_height
                sx, sy = camera.transform_coordinate((wx, wy))
                rect = pygame.Rect(sx, sy, tile_size, tile_size)
                pygame.draw.rect(surface, GRAY, rect, 1)

    def draw_tiles(self, surface, camera, topbar_height):
        for tile in self.tiles.values():
            tile.update_position(camera, self._tile_size)
            tile.rect.y += topbar_height
            surface.blit(tile.image, tile.rect)

    @property
    def tile_size(self):
        return self._tile_size

    @property
    def screen_size(self):
        return (self._screen_width, self._screen_height)
