import pygame
import sys

# --- Configuración general ---
TILE_SIZE = 64
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

# --- Colores ---
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
DARK_GRAY = (40, 40, 40)
GREEN = (50, 200, 100)

# --- Inicialización de Pygame ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Grid infinito con cámara y Player")
clock = pygame.time.Clock()


# --- Clase Camera ---
class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = 10

    def move(self, keys):
        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed
        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed

    def transform_coordinate(self, pos):
        """Transforma coordenadas del mundo a pantalla"""
        world_x, world_y = pos
        return world_x - self.x, world_y - self.y


# --- Clase Player ---
class Player:
    def __init__(self, x, y, color=GREEN):
        self.grid_pos = [x, y]
        self.color = color
        self.camera = Camera()  # ✅ Cámara integrada en el jugador

    def update_player_position(self, keys):
        """Actualiza el movimiento de cámara (WASD)"""
        self.camera.move(keys)

    def get_world_position(self):
        """Convierte posición del grid a coordenadas del mundo"""
        return self.grid_pos[0] * TILE_SIZE, self.grid_pos[1] * TILE_SIZE

    def draw(self, surface):
        x, y = self.get_world_position()
        x, y = self.camera.transform_coordinate((x, y))
        rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(surface, self.color, rect)


# --- Función para dibujar el grid visible ---
def draw_grid(surface, camera):
    start_x = int(camera.x // TILE_SIZE) - 1
    end_x = int((camera.x + SCREEN_WIDTH) // TILE_SIZE) + 2
    start_y = int(camera.y // TILE_SIZE) - 1
    end_y = int((camera.y + SCREEN_HEIGHT) // TILE_SIZE) + 2

    for gx in range(start_x, end_x):
        for gy in range(start_y, end_y):
            wx = gx * TILE_SIZE
            wy = gy * TILE_SIZE
            sx, sy = camera.transform_coordinate((wx, wy))
            rect = pygame.Rect(sx, sy, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(surface, GRAY, rect, 1)


# --- Función para colocar tiles en el grid ---
def draw_tiles(surface, camera, tiles):
    for (gx, gy), color in tiles.items():
        wx, wy = gx * TILE_SIZE, gy * TILE_SIZE
        sx, sy = camera.transform_coordinate((wx, wy))
        rect = pygame.Rect(sx, sy, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(surface, color, rect)
