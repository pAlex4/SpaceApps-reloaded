import pygame
import random

TILE_TYPES = [
    "private", "hygiene", "waste", "exercise", "food",
    "maintenance", "science", "medical", "social",
    "logistics", "airlock"
]

class TileBlock(pygame.sprite.Sprite):
    def __init__(self, gx, gy, width, height, tile_size):
        super().__init__()
        self.gx = gx
        self.gy = gy
        self.width = width
        self.height = height
        self.tile_size = tile_size

        self.color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255)
        )
        w_px = width * tile_size
        h_px = height * tile_size
        self.image = pygame.Surface((w_px, h_px))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=(gx * tile_size, gy * tile_size))

        self.type = random.choice(TILE_TYPES)
        self.masa = random.uniform(1, 100)
        self.volumen = random.uniform(1, 50)
        self.costo = random.uniform(100, 1000)
        self.limpieza = random.uniform(0, 1)
        self.permanencia = random.randint(1, 365)

        print(f"Placed TileBlock at ({self.gx}, {self.gy}), size ({self.width}x{self.height}): "
              f"type={self.type}, masa={self.masa:.2f}, volumen={self.volumen:.2f}, "
              f"costo={self.costo:.2f}, limpieza={self.limpieza:.2f}, permanencia={self.permanencia} days, "
              f"color={self.color}")

    def covers(self, gx, gy):
        return (self.gx <= gx < self.gx + self.width) and (self.gy <= gy < self.gy + self.height)
