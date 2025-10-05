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

class Player:
    def __init__(self, x, y, tile_size, color=(50, 200, 100)):
        self.grid_pos = [x, y]
        self.color = color
        self.camera = Camera()
        self._tile_size = tile_size
        self._actions = {
            113: "add_tile",     # tecla Q
            101: "remove_tile"   # tecla E
        }
        self.action = "add_tile"  # acción inicial

        self.image = pygame.Surface((self._tile_size, self._tile_size))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

    # --- 1️⃣ Función: cambiar la acción según la tecla presionada ---
    def change_action(self, key_pressed):
        """Cambia la acción actual del jugador dependiendo de la tecla presionada."""
        if key_pressed in self._actions:
            self.action = self._actions[key_pressed]
            print(f"Acción actual cambiada a: {self.action}")

    # --- 2️⃣ Función: ejecutar la acción cuando se presiona el mouse ---
    def execute_action(self, world, mouse_pos, mouse_button):
        """Ejecuta la acción actual del jugador sobre el mundo al hacer clic."""
        wx, wy = mouse_pos[0] + self.camera.x, mouse_pos[1] + self.camera.y
        gx, gy = int(wx // world.tile_size), int(wy // world.tile_size)

        # Solo usar click izquierdo (1)
        if mouse_button == 1:
            if self.action == "add_tile":
                world.add_tile(gx, gy)
            elif self.action == "remove_tile":
                world.remove_tile(gx, gy)

    # --- Movimiento y renderizado ---
    def update_position(self, keys):
        self.camera.move(keys)

    def get_world_position(self):
        return self.grid_pos[0] * self._tile_size, self.grid_pos[1] * self._tile_size

    def draw(self, surface):
        x, y = self.get_world_position()
        x, y = self.camera.transform_coordinate((x, y))
        rect = pygame.Rect(x, y, self._tile_size, self._tile_size)
        pygame.draw.rect(surface, self.color, rect)
