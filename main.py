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

world = WorldGeneration(screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT, topbar_height=topbar_height, grid_size=25)
player = Player(0, 0, tile_size=world.tile_size)

running = True
while running:
    # Compute the mouse's grid position consistently using camera offset and topbar height
    mouse_grid_pos = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        topbar.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[1] > topbar_height:
                # Mouse to world coordinate with topbar height subtracted
                wx = mouse_pos[0] + player.camera.x
                wy = mouse_pos[1] + player.camera.y - topbar_height
                grid_x = int(wx // world.tile_size)
                grid_y = int(wy // world.tile_size)
                if 0 <= grid_x < world.grid_size and 0 <= grid_y < world.grid_size:
                    current_action = topbar.toggle_button.get_current_option()
                    player.action = "add_tile" if current_action == "draw" else "remove_tile"
                    player.execute_action(world, (grid_x, grid_y), event.button)  # Pass properly converted grid pos

    mx, my = pygame.mouse.get_pos()
    if my > topbar_height:
        wx = mx + player.camera.x
        wy = my + player.camera.y - topbar_height
        grid_x = int(wx // world.tile_size)
        grid_y = int(wy // world.tile_size)
        if 0 <= grid_x < world.grid_size and 0 <= grid_y < world.grid_size:
            mouse_grid_pos = (grid_x, grid_y)

    keys = pygame.key.get_pressed()
    player.update_position(keys)

    screen.fill(DARK_GRAY)
    world.draw_grid(screen, player.camera, topbar_height)
    world.draw_tiles(screen, player.camera, topbar_height)
    player.draw(screen)

    # Draw hover preview at transformed tile position (no topbar offset here, camera handles it)
    if mouse_grid_pos:
        px = mouse_grid_pos[0] * world.tile_size
        py = mouse_grid_pos[1] * world.tile_size
        sx, sy = player.camera.transform_coordinate((px, py + topbar_height))
        hover_rect = pygame.Rect(sx, sy, world.tile_size, world.tile_size)
        hover_surface = pygame.Surface((world.tile_size, world.tile_size), pygame.SRCALPHA)
        hover_surface.fill((255, 255, 0, 100))  # Yellow transparent preview
        screen.blit(hover_surface, hover_rect.topleft)

    topbar.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
