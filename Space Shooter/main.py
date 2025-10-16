import pygame
import random
from os.path import join

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
running = True
pygame.display.set_caption('Space Shooter')
player_surf = pygame.image.load(join('Space Shooter', 'Assets', 'images', 'player.png')).convert_alpha()
player_rect = player_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
star_surf = pygame.image.load(join('Space Shooter', 'Assets', 'images', 'star.png')).convert_alpha()
star_positions = [(random.randint(0, 1180), random.randint(0, 620)) for _ in range(20)]

generated = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    display_surface.fill("darkgray")
    for star_pos in star_positions:
        display_surface.blit(star_surf, star_pos)
    player_rect.left += 0.1
    display_surface.blit(player_surf, player_rect)
    pygame.display.update()
pygame.quit()