import pygame
from os.path import join

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
running = True
pygame.display.set_caption('Space Shooter')
path = join('Space Shooter', 'Assets', 'images', 'player.png')
player_surf = pygame.image.load(path).convert_alpha()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    display_surface.fill("darkgray")
    display_surface.blit(player_surf, (100, 100))
    pygame.display.update()
pygame.quit()