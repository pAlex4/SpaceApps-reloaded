import pygame
import sys

from player import Player
from world import WorldGeneration
from topbar import TopBar

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

DARK_GRAY = (40, 40, 40)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Grid infinito con cámara y Player + Menu")
clock = pygame.time.Clock()

topbar = TopBar(SCREEN_WIDTH)
topbar_height = topbar.height

world = WorldGeneration(screen_width=SCREEN_WIDTH,
                        screen_height=SCREEN_HEIGHT,
                        topbar_height=topbar_height,
                        grid_size=25)
player = Player(0, 0, tile_size=world.tile_size)

# Define tile shapes: width x height in tiles
tile_shapes = {
    '1': (1, 1),  # single tile - default
    '2': (2, 2),  # 2x2 block
    '3': (3, 1),  # 3x1 horizontal strip
    '4': (4, 4)   # 4x4 block
}
current_shape = tile_shapes['1']

running = True
while running:
    mouse_grid_pos = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        topbar.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[1] > topbar_height:
                wx = mouse_pos[0] + player.camera.x
                wy = mouse_pos[1] - topbar_height + player.camera.y
                grid_x = int(wx // world.tile_size)
                grid_y = int(wy // world.tile_size)

                if 0 <= grid_x < world.grid_size and 0 <= grid_y < world.grid_size:
                    current_action = topbar.toggle_button.get_current_option()
                    player.action = "add_tile" if current_action == "draw" else "remove_tile"

                    width, height = current_shape
                    for dx in range(width):
                        for dy in range(height):
                            tx, ty = grid_x + dx, grid_y + dy
                            if 0 <= tx < world.grid_size and 0 <= ty < world.grid_size:
                                if player.action == "add_tile":
                                    world.add_tile(tx, ty)
                                else:
                                    world.remove_tile(tx, ty)

    # Handle tile shape selection keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_1]:
        current_shape = tile_shapes['1']
    elif keys[pygame.K_2]:
        current_shape = tile_shapes['2']
    elif keys[pygame.K_3]:
        current_shape = tile_shapes['3']
    elif keys[pygame.K_4]:
        current_shape = tile_shapes['4']

    player.update_position(keys)

    mx, my = pygame.mouse.get_pos()
    if my > topbar_height:
        wx = mx + player.camera.x
        wy = my - topbar_height + player.camera.y
        grid_x = int(wx // world.tile_size)
        grid_y = int(wy // world.tile_size)
        if 0 <= grid_x < world.grid_size and 0 <= grid_y < world.grid_size:
            mouse_grid_pos = (grid_x, grid_y)

    screen.fill(DARK_GRAY)
    world.draw_grid(screen, player.camera, topbar_height)
    world.draw_tiles(screen, player.camera, topbar_height)
    player.draw(screen)

    # Draw hover preview for entire current shape area
    if mouse_grid_pos:
        width, height = current_shape
        for dx in range(width):
            for dy in range(height):
                px = (mouse_grid_pos[0] + dx) * world.tile_size
                py = (mouse_grid_pos[1] + dy) * world.tile_size
                sx, sy = player.camera.transform_coordinate((px, py + topbar_height))  # Add topbar for alignment
                hover_rect = pygame.Rect(sx, sy, world.tile_size, world.tile_size)
                hover_surface = pygame.Surface((world.tile_size, world.tile_size), pygame.SRCALPHA)
                hover_surface.fill((255, 255, 0, 100))  # Semi-transparent yellow
                screen.blit(hover_surface, hover_rect.topleft)

    topbar.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
