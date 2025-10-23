import pygame
import random
from os.path import join

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
running = True
clock = pygame.time.Clock()

pygame.display.set_caption('Space Shooter')
player_surf = pygame.image.load(join('Space Shooter', 'Assets', 'images', 'player.png')).convert_alpha()
player_rect = player_surf.get_frect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 30))
player_direction = pygame.math.Vector2()
player_speed = 300
star_surf = pygame.image.load(join('Space Shooter', 'Assets', 'images', 'star.png')).convert_alpha()
star_positions = [(random.randint(0, 1180), random.randint(0, 620)) for _ in range(20)]

meteor_surf = pygame.image.load(join('Space Shooter', 'Assets', 'images', 'meteor.png')).convert_alpha()
meteor_rect = meteor_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

laser_surf = pygame.image.load(join('Space Shooter', 'Assets', 'images', 'laser.png')).convert_alpha()
laser_rect = laser_surf.get_frect(bottomleft = (20, WINDOW_HEIGHT - 20))


while running:
    dt = clock.tick() / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player_direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT]) 
    player_direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP]) 
    player_direction = player_direction.normalize() if player_direction else player_direction

    display_surface.fill("darkgray")

    for star_pos in star_positions:
        display_surface.blit(star_surf, star_pos)

    player_rect.center += player_direction * player_speed * dt

    display_surface.blit(meteor_surf, meteor_rect)
    display_surface.blit(laser_surf, laser_rect)
    display_surface.blit(player_surf, player_rect)
    pygame.display.update()
pygame.quit()