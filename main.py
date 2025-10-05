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

size_map = {
    "1x1": (1, 1),
    "2x2": (2, 2),
    "3x1": (3, 1),
    "4x4": (4, 4)
}

cost_map = {
    (1, 1): 5,
    (2, 2): 10,
    (3, 1): 7,
    (4, 4): 20
}

money = 150  # initial money

world = WorldGeneration(screen_width=SCREEN_WIDTH,
                        screen_height=SCREEN_HEIGHT,
                        topbar_height=topbar_height,
                        grid_size=25)
player = Player(0, 0, tile_size=world.tile_size)

# Set default tile size dropdown to "4x4"
topbar.toggle_button.current_index = topbar.toggle_button.options.index("4x4")

def get_ui_rects():
    rects = [
        topbar.draw_remove_toggle.rect,
        topbar.type_dropdown.rect,
        topbar.toggle_button.rect,
    ]

    # Add dropdown open options rectangles if open
    if topbar.type_dropdown.is_open:
        for i in range(len(topbar.type_dropdown.options)):
            rect = pygame.Rect(
                topbar.type_dropdown.rect.x,
                topbar.type_dropdown.rect.y + topbar.type_dropdown.rect.height * (i + 1),
                topbar.type_dropdown.rect.width,
                topbar.type_dropdown.rect.height
            )
            rects.append(rect)

    if topbar.toggle_button.is_open:
        for i in range(len(topbar.toggle_button.options)):
            rect = pygame.Rect(
                topbar.toggle_button.rect.x,
                topbar.toggle_button.rect.y + topbar.toggle_button.rect.height * (i + 1),
                topbar.toggle_button.rect.width,
                topbar.toggle_button.rect.height
            )
            rects.append(rect)
    return rects

def click_on_ui(mouse_pos):
    for rect in get_ui_rects():
        if rect.collidepoint(mouse_pos):
            return True
    return False


running = True
while running:
    mouse_grid_pos = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        topbar.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if click_on_ui(mouse_pos):
                # Click was on UI or open dropdown options - skip tile placement
                pass
            else:
                if mouse_pos[1] > topbar_height:
                    wx = mouse_pos[0] + player.camera.x
                    wy = mouse_pos[1] - topbar_height + player.camera.y
                    grid_x = int(wx // world.tile_size)
                    grid_y = int(wy // world.tile_size)

                    if 0 <= grid_x < world.grid_size and 0 <= grid_y < world.grid_size:
                        current_action = topbar.draw_remove_toggle.get_current_option().lower() + "_tile"
                        player.action = current_action

                        selected_shape = topbar.toggle_button.get_current_option()
                        current_shape = size_map.get(selected_shape, (1, 1))
                        width, height = current_shape

                        cost = cost_map.get(current_shape, 5)
                        selected_type = topbar.type_dropdown.get_current_option()

                        if player.action == "draw_tile":
                            if money >= cost:
                                placed = world.add_tile_block(grid_x, grid_y, width, height, selected_type, cost)
                                if placed:
                                    money -= cost
                                else:
                                    print("Tile placement failed: overlapping tiles")
                            else:
                                print("Not enough money!")
                        elif player.action == "remove_tile":
                            block = world.get_block_at(grid_x, grid_y)
                            if block:
                                world.remove_tile_at(grid_x, grid_y)
                                money += cost_map.get((block.width, block.height), 5)

    selected_shape = topbar.toggle_button.get_current_option()
    current_shape = size_map.get(selected_shape, (1, 1))

    keys = pygame.key.get_pressed()
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

    # Draw hover preview covering block area
    if mouse_grid_pos:
        width, height = current_shape
        px = mouse_grid_pos[0] * world.tile_size
        py = mouse_grid_pos[1] * world.tile_size
        sx, sy = player.camera.transform_coordinate((px, py + topbar_height))
        hover_rect = pygame.Rect(sx, sy, width * world.tile_size, height * world.tile_size)
        hover_surface = pygame.Surface(hover_rect.size, pygame.SRCALPHA)
        hover_surface.fill((255, 255, 0, 100))  # semi-transparent yellow
        screen.blit(hover_surface, hover_rect.topleft)

    topbar.draw(screen, money)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
