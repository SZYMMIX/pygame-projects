import pygame
from random import randint, uniform
from os.path import join

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('Space Shooter', 'Assets', 'images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 1.2))
        self.speed = 300
        self.direction = pygame.math.Vector2()

        self.canShoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400
    
    def laser_timer(self):
        if not self.canShoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.canShoot = True


    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT]) 
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP]) 
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.canShoot:
            Laser((all_sprites, laser_sprites), laser_surf, self.rect.midtop)
            self.canShoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

        
        self.laser_timer()

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, groups, surf, pos):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)

    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(80, WINDOW_WIDTH-80), -40))
        # self.drop_speed = randint(100, 150)
        self.drop_speed = randint(200, 300)
        # self.direction = pygame.Vector2(uniform(-0.15, 0.15), 1)
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
    
    def update(self, dt):
        self.rect.center += self.direction * self.drop_speed * dt
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()

def display_score():
    current_time = pygame.time.get_ticks()//1000
    text_time_surf = font.render(str(current_time), True, (200, 200, 200, 1))
    text_rect = text_time_surf.get_frect(midbottom = (WINDOW_WIDTH // 2, WINDOW_HEIGHT ))
    display_surface.blit(text_time_surf, text_rect)

def collision():
    global running
    # possible future update:
    # global counter
    # global text_destroyed_surf
    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, dokill=True)
    collision_lasers = pygame.sprite.groupcollide(laser_sprites, meteor_sprites, dokilla=True, dokillb=True)

    if collision_sprites:
        running = False
    
    # if collision_lasers:
    #     counter += 1
        # text_destroyed_surf = font.render(f"{counter}", True, (200, 200, 200, 1))

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
running = True
clock = pygame.time.Clock()
pygame.display.set_caption('Space Shooter')
font = pygame.font.Font(join('Space Shooter', 'Assets', 'images', 'Oxanium-Bold.ttf'), 80)
counter = 0
star_surf = pygame.image.load(join('Space Shooter', 'Assets', 'images', 'star.png')).convert_alpha()
meteor_surf = pygame.image.load(join('Space Shooter', 'Assets', 'images', 'meteor.png')).convert_alpha()
laser_surf = pygame.image.load(join('Space Shooter', 'Assets', 'images', 'laser.png')).convert_alpha()

all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
for _ in range(20):
    Star(all_sprites, star_surf)
player = Player(all_sprites)


meteor_event = pygame.event.custom_type()
# pygame.time.set_timer(meteor_event,   1000)
pygame.time.set_timer(meteor_event, 110)


while running:
    dt = clock.tick() / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == meteor_event:
            Meteor((all_sprites, meteor_sprites), meteor_surf)
    
    all_sprites.update(dt)
    collision()
    
    display_surface.fill((49, 8, 80, 1))
    display_score()
    all_sprites.draw(display_surface)
    pygame.display.update()

pygame.quit()