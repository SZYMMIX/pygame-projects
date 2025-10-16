import pygame

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
running = True
pygame.display.set_caption('Space Shooter')

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    display_surface.fill("red")
    pygame.display.update()
pygame.quit()