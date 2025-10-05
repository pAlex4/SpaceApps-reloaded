import pygame
import sys
from player import *
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

player = Player(0, 0)
tiles = {}  # {(x, y): color}


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Colocar o quitar tiles con el mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            wx, wy = mx + player.camera.x, my + player.camera.y
            gx, gy = int(wx // TILE_SIZE), int(wy // TILE_SIZE)

            if event.button == 1:  # Click izquierdo -> colocar tile
                tiles[(gx, gy)] = (200, 100, 50)
            elif event.button == 3:  # Click derecho -> quitar tile
                tiles.pop((gx, gy), None)

    # --- Movimiento de cámara controlado por el jugador ---
    keys = pygame.key.get_pressed()
    player.update_player_position(keys)

    # --- Dibujado ---
    screen.fill(DARK_GRAY)
    draw_grid(screen, player.camera)
    draw_tiles(screen, player.camera, tiles)
    player.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)