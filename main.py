import pygame
from topbar import TopBar

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Initialize the TopBar
topbar = TopBar(SCREEN_WIDTH)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # Clear screen
    
    # Draw the topbar
    topbar.draw(screen)

    # Game logic and drawing would be here

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
