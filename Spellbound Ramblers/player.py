from settings import *
from math import sin

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, collision_sprites, pos):
        super().__init__(groups)
        self.load_images()
        self.state = 'down'
        self.frame_index = 0
        self.image = pygame.image.load(join('Assets', 'images', 'player', 'down', '0.png')).convert_alpha()
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-60, -80)

        self.lifes = 3
        self.is_vulnerable = True
        self.hit_time = 0
        self.invulnerability_duration = 700

        self.direction = pygame.math.Vector2()
        self.speed = 400
        self.collision_sprites = collision_sprites
    
    def load_images(self):
        self.frames = {'left': [], 'right': [], 'up': [], 'down': []}

        for state in self.frames.keys():
            for folder_path, sub_folders, file_names in walk(join('Assets', 'images', 'player', state)):
                if file_names:
                    for file_name in sorted(file_names, key= lambda name: int(name.split('.')[0])):
                        full_path = join(folder_path, file_name)
                        surf = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surf)

    def _handle_movement(self):
        keys = pygame.key.get_pressed()
        
        self.direction.y =  int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])
        self.direction.x =  int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])

    def _move(self, dt):
        self.direction = self.direction.normalize() if self.direction else self.direction

        self.hitbox_rect.x += self.direction.x * dt * self.speed
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * dt * self.speed
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    def animate(self, dt):
        

        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'
        
        if self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'

        self.frame_index = self.frame_index + 6 * dt if self.direction else 0
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]

    def update(self, dt):
        self._handle_movement()
        self._move(dt)
        self.animate(dt)

        self.check_vulnerability()
        self.blink()
        
    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.hitbox_rect.right = sprite.rect.left
                    else:
                        self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y > 0:
                        self.hitbox_rect.bottom = sprite.rect.top
                    else:
                        self.hitbox_rect.top = sprite.rect.bottom
    
    def damage(self):
        if self.is_vulnerable:
            self.is_vulnerable = False
            self.lifes -= 1
            self.hit_time = pygame.time.get_ticks()

    def blink(self):
        if not self.is_vulnerable:
            alpha = (sin(pygame.time.get_ticks() / 20) * 127.5) + 127.5
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def check_vulnerability(self):
        if not self.is_vulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.hit_time >= self.invulnerability_duration:
                self.is_vulnerable = True