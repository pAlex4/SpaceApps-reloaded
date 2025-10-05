import pygame
from tile import TileBlock

GRAY = (180, 180, 180)

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

        self.tile_blocks = []

    def add_tile_block(self, gx, gy, width, height):
        # Optional: add overlap checking if needed
        block = TileBlock(gx, gy, width, height, self._tile_size)
        self.tile_blocks.append(block)

    def remove_tile_at(self, gx, gy):
        for block in self.tile_blocks:
            if block.covers(gx, gy):
                self.tile_blocks.remove(block)
                break

    def get_block_at(self, gx, gy):
        for block in self.tile_blocks:
            if block.covers(gx, gy):
                return block
        return None

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
        for block in self.tile_blocks:
            wx = block.gx * self._tile_size
            wy = block.gy * self._tile_size + topbar_height
            sx, sy = camera.transform_coordinate((wx, wy))
            block.rect.topleft = (sx, sy)
            surface.blit(block.image, block.rect)

    @property
    def tile_size(self):
        return self._tile_size

    @property
    def screen_size(self):
        return (self._screen_width, self._screen_height)

    def remove_tile_block(self, block):
        if block in self.tile_blocks:
            self.tile_blocks.remove(block)

    def get_block_at(self, gx, gy):
        for block in self.tile_blocks:
            if block.covers(gx, gy):
                return block
        return None
