from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.image.load(join('Spellbound Ramblers', 'Assets', 'images', 'player', 'down', '0.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.hitbox_rect = self.rect.inflate(-60, 0)

        self.direction = pygame.math.Vector2()
        self.speed = 400
        self.collision_sprites = collision_sprites

    def _handle_movement(self):
        keys = pygame.key.get_pressed()
        
        self.direction.y =  keys[pygame.K_DOWN] - keys[pygame.K_UP]
        self.direction.x =  keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
    def _move(self, dt):
        self.direction = self.direction.normalize() if self.direction else self.direction

        self.hitbox_rect.x += self.direction.x * dt * self.speed
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * dt * self.speed
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    def update(self, dt):
        self._handle_movement()
        self._move(dt)
        

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
            
