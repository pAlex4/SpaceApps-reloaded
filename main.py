import pygame
from topbar import TopBar

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

topbar = TopBar(SCREEN_WIDTH)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        topbar.handle_event(event)

    screen.fill((0, 0, 0))
    topbar.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
