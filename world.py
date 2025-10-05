import pygame
from tile import * # ajusta el import según tu estructura

GRAY = (180, 180, 180)


class WorldGeneration:
    def __init__(self, screen_width=800, screen_height=600, tile_size=64):
        self._screen_width = screen_width
        self._screen_height = screen_height
        self._tile_size = tile_size

        # Grupo de sprites para dibujar los tiles
        self.sprites = pygame.sprite.LayeredUpdates()

    def add_tile(self, gx, gy, tile_img, resistencia=0.8):
        """Agrega un nuevo AssetTile al grupo de sprites usando una imagen ya cargada."""
        tile = AssetTile(gx, gy, self._tile_size, img=tile_img, resistencia=resistencia)
        self.sprites.add(tile, layer=1)

    def remove_tile(self, gx, gy):
        """Elimina un tile del grupo si coincide su posición en la grilla."""
        for sprite in list(self.sprites):
            if isinstance(sprite, AssetTile) and sprite.grid_x == gx and sprite.grid_y == gy:
                self.sprites.remove(sprite)
                break

    def draw_grid(self, surface, camera):
        """Dibuja líneas de cuadrícula según la cámara."""
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
        """Actualiza la posición de todos los tiles y los dibuja."""
        for tile in self.sprites:
            tile.update_position(camera, self._tile_size)
        self.sprites.draw(surface)

    @property
    def tile_size(self):
        return self._tile_size

    @property
    def screen_size(self):
        return (self._screen_width, self._screen_height)
