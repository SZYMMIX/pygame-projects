import pygame
from random import randint, uniform
from os.path import join

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
PLAYER_SPEED = 300
LASER_SPEED = 400
LASER_COOLDOWN = 400
METEOR_SPEED_MIN = 200
METEOR_SPEED_MAX = 300
METEOR_ROTATION_MIN = 10
METEOR_ROTATION_MAX = 30
SCORE_COLOR = (200, 200, 200, 1)
BACKGROUND_COLOR = (6, 6, 33, 0.8)

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, create_laser):
        super().__init__(groups)
        self.image = pygame.image.load(join('Space Shooter', 'Assets', 'images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 1.2))
        self.speed = PLAYER_SPEED
        self.direction = pygame.math.Vector2()

        self.canShoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = LASER_COOLDOWN
        self.create_laser = create_laser
    
    def _laser_timer(self):
        if not self.canShoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.canShoot = True

    def _handle_input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT]) 
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])

        if pygame.key.get_just_pressed()[pygame.K_SPACE] and self.canShoot:
            self.create_laser(self.rect.midtop)
            self.canShoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

    def update(self, dt):

        self._handle_input()
        self._laser_timer()

        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt
        
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > WINDOW_WIDTH: self.rect.right = WINDOW_WIDTH
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > WINDOW_HEIGHT: self.rect.bottom = WINDOW_HEIGHT

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
        self.rect.centery -= LASER_SPEED * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.origin_image = surf
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(80, WINDOW_WIDTH-80), -40))
        self.drop_speed = randint(METEOR_SPEED_MIN, METEOR_SPEED_MAX)
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.rotation_speed = randint(METEOR_ROTATION_MIN, METEOR_ROTATION_MAX)
        self.rotation = 0
    
    def update(self, dt):
        self.rect.center += self.direction * self.drop_speed * dt
        
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()

        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.origin_image, self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center)

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center = pos)
 
    def update(self, dt):
        self.frame_index += 20 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Space Shooter')
        self.clock = pygame.time.Clock()
        self.running = True

        self._load_assets()

        self.all_sprites = pygame.sprite.Group()
        self.meteor_sprites = pygame.sprite.Group()
        self.laser_sprites = pygame.sprite.Group()

        for _ in range(20):
            Star(self.all_sprites, self.star_surf)
        
        self.player = Player(self.all_sprites, self.create_laser)

        self.meteor_event = pygame.event.custom_type()
        pygame.time.set_timer(self.meteor_event, 110)

        self.game_music.play(-1)
    
    def _load_assets(self):
        self.font = pygame.font.Font(join('Space Shooter', 'Assets', 'images', 'Oxanium-Bold.ttf'), 60)
        self.star_surf = pygame.image.load(join('Space Shooter', 'Assets', 'images', 'star.png')).convert_alpha()
        self.meteor_surf = pygame.image.load(join('Space Shooter', 'Assets', 'images', 'meteor.png')).convert_alpha()
        self.laser_surf = pygame.image.load(join('Space Shooter', 'Assets', 'images', 'laser.png')).convert_alpha()
        self.explosion_frames = [pygame.image.load(join('Space Shooter', 'Assets', 'images', 'explosion', f'{i}.png')).convert_alpha() for i in range(21)]

        self.laser_sound = pygame.mixer.Sound(join('Space Shooter', 'Assets', 'audio', 'laser.wav'))
        self.laser_sound.set_volume(0.07)
        self.explosion_sound = pygame.mixer.Sound(join('Space Shooter', 'Assets', 'audio', 'explosion.wav'))
        self.explosion_sound.set_volume(0.07)
        self.game_music = pygame.mixer.Sound(join('Space Shooter', 'Assets', 'audio', 'game_music.wav'))
        self.game_music.set_volume(0.04)

    def create_laser(self, pos):
        Laser((self.all_sprites, self.laser_sprites),self.laser_surf, pos)
        self.laser_sound.play()

    def display_score(self):
        score_text = str(pygame.time.get_ticks()//1000)
        text_surf = self.font.render(score_text, True, SCORE_COLOR)
        text_rect = text_surf.get_frect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, SCORE_COLOR, text_rect.inflate(35, 5).move(0, -10), 5, 10)

    def collision(self):

        if pygame.sprite.spritecollide(self.player, self.meteor_sprites, True, pygame.sprite.collide_mask):
            self.running = False
        
        for laser in self.laser_sprites:
            collided_sprites = pygame.sprite.spritecollide(laser, self.meteor_sprites, True)
            if collided_sprites:
                laser.kill()
                AnimatedExplosion(self.explosion_frames, laser.rect.midtop, self.all_sprites)
                self.explosion_sound.play()

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == self.meteor_event:
                    Meteor((self.all_sprites, self.meteor_sprites), self.meteor_surf)
            
            self.all_sprites.update(dt)
            self.collision()
            
            self.display_surface.fill(BACKGROUND_COLOR)
            self.display_score()
            self.all_sprites.draw(self.display_surface)
            pygame.display.update()
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
