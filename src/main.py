import pygame
import sys
from player import *
from world import *
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


tiles = {}  # {(x, y): color}

world = WorldGeneration()
player = Player(0, 0, tile_size=world.tile_size)

# --- Bucle principal ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # 1️⃣ Teclado → cambia acción
        if event.type == pygame.KEYDOWN:
            player.change_action(event.key)

        # 2️⃣ Mouse → ejecuta acción
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.execute_action(world, pygame.mouse.get_pos(), event.button)

    keys = pygame.key.get_pressed()
    player.update_position(keys)

    # --- Renderizado ---
    screen.fill((40, 40, 40))
    world.draw_grid(screen, player.camera)
    world.draw_tiles(screen, player.camera)
    player.draw(screen)

    pygame.display.flip()
    clock.tick(60)