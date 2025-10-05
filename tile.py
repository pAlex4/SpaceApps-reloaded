import pygame
import random

TILE_TYPES = [
    "private", "hygiene", "waste", "exercise", "food",
    "maintenance", "science", "medical", "social",
    "logistics", "airlock"
]

TYPE_COLORS = {
    "private": (255, 0, 0),       # red
    "hygiene": (0, 255, 255),     # cyan
    "waste": (105, 105, 105),     # dim gray
    "exercise": (0, 255, 0),      # green
    "food": (255, 165, 0),        # orange
    "maintenance": (128, 0, 128), # purple
    "science": (0, 0, 255),       # blue
    "medical": (255, 192, 203),   # pink
    "social": (255, 255, 0),      # yellow
    "logistics": (139, 69, 19),   # brown
    "airlock": (192, 192, 192),   # silver
}

class TileBlock(pygame.sprite.Sprite):
    def __init__(self, gx, gy, width, height, tile_size, type_override=None, cost=0):
        super().__init__()
        self.gx = gx
        self.gy = gy
        self.width = width
        self.height = height
        self.tile_size = tile_size

        self.type = type_override if type_override else random.choice(TILE_TYPES)
        self.color = TYPE_COLORS.get(self.type, (255, 255, 255))  # white default

        w_px = width * tile_size
        h_px = height * tile_size
        self.image = pygame.Surface((w_px, h_px))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=(gx * tile_size, gy * tile_size))

        self.costo = cost  # Explicit assigned cost value

        self.masa = random.uniform(1, 100)
        self.volumen = random.uniform(1, 50)
        self.limpieza = random.uniform(0, 1)
        self.permanencia = random.randint(1, 365)

        print(f"Placed TileBlock at grid position ({self.gx}, {self.gy}), "
              f"size ({self.width}x{self.height}): type={self.type}, "
              f"masa={self.masa:.2f}, volumen={self.volumen:.2f}, costo=${self.costo:.2f}, "
              f"limpieza={self.limpieza:.2f}, permanencia={self.permanencia} days, "
              f"color={self.color}")

    def covers(self, gx, gy):
        return (self.gx <= gx < self.gx + self.width) and (self.gy <= gy < self.gy + self.height)
