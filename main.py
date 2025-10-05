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

def draw_tiled_background(surface, image, camera=None):
    """Dibuja una imagen repetida para cubrir toda la superficie."""
    img_w, img_h = image.get_size()
    screen_w, screen_h = surface.get_size()

    # Si tienes cámara, usa su offset
    offset_x = int(camera.x % img_w) if camera else 0
    offset_y = int(camera.y % img_h) if camera else 0

    # Dibuja en patrón repetido
    for x in range(-img_w, screen_w + img_w, img_w):
        for y in range(-img_h, screen_h + img_h, img_h):
            surface.blit(image, (x - offset_x, y - offset_y))
background_tile = pygame.image.load("img/marsTerrain.png").convert()
background_tile = pygame.transform.scale(background_tile, (256, 256))

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
                index = topbar.dropdown.selected_index
                tile_name = topbar.dropdown.options[index]      # Ej: "Roca"
                tile_path = f"img/Habitat/{tile_name}.png"   
                print(tile_path)           # → "img/Roca.png"
                tile = pygame.image.load(tile_path).convert_alpha()  # carga la imagen con transparencia
                player.selected_tile_type = pygame.transform.scale(tile, (64, 64))
                player.execute_action(world, mouse_pos, event.button)


    draw_tiled_background(screen, background_tile, player.camera)

    keys = pygame.key.get_pressed()
    player.update_position(keys)
    player.update_hover(pygame.mouse.get_pos(), topbar.height)

 
    world.draw_grid(screen, player.camera)
    world.draw_tiles(screen, player.camera)
    player.draw(screen)

    topbar.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()

