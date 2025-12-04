from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.ground = True

class Player(Sprite):
    def __init__(self, pos, groups, collision_sprites):
        surf = pygame.Surface((40,70))
        super().__init__(pos, surf, groups)
        
        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2()
        self.speed = 400

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.collision("horizontal")
        self.rect.y += self.direction.y * self.speed * dt
        self.collision("vertical")

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == "horizontal":
                    if self.direction.x > 0: self.rect.right = sprite.rect.left
                    else: self.rect.left = sprite.rect.right
                else:
                    if self.direction.y > 0: self.rect.bottom = sprite.rect.top
                    else: self.rect.top = sprite.rect.bottom


    def update(self, dt):
        self.input()
        self.move(dt)

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, groups, pos, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)