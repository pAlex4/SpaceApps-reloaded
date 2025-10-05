import pygame
import sys

from player import Player
from world import WorldGeneration
from topbar import TopBar

# --- Configuración general ---
TILE_SIZE = 64
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

DARK_GRAY = (40, 40, 40)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Grid infinito con cámara y Player + Menu")
clock = pygame.time.Clock()

world = WorldGeneration()
player = Player(0, 0, tile_size=world.tile_size)

topbar = TopBar(SCREEN_WIDTH)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        topbar.handle_event(event)

        if event.type == pygame.KEYDOWN:
            player.change_action(event.key)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[1] > topbar.height:
                player.execute_action(world, mouse_pos, event.button)

    keys = pygame.key.get_pressed()
    player.update_position(keys)

    screen.fill(DARK_GRAY)
    world.draw_grid(screen, player.camera)
    world.draw_tiles(screen, player.camera)
    player.draw(screen)

    topbar.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
