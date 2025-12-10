from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class AnimatedSprite(Sprite):
    def __init__(self, frames, pos, groups):
        self.frames, self.frame_index, self.animation_speed = frames, 0, 9
        super().__init__(pos, self.frames[self.frame_index], groups)

    def animate(self,dt):
        self.frame_index += self.animation_speed * dt

        self.image = self.frames[int(self.frame_index) % len(self.frames)]

class Player(AnimatedSprite):
    def __init__(self, pos, groups, collision_sprites, frames):
        super().__init__(frames, pos, groups)
        self.flip = False

        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2()
        self.speed = 400
        self.gravity = 50
        self.jump_speed = 19
        self.on_floor = False

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])

        if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and self.on_floor == True:
            self.direction.y = -self.jump_speed

    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.collision("horizontal")
        self.direction.y += self.gravity * dt
        self.rect.y += self.direction.y
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
                    self.direction.y = 0


    def check_floor(self):
        bottom_rect = pygame.FRect((0,0), (self.rect.width, 2)).move_to(midtop = self.rect.midbottom)

        self.on_floor = True if bottom_rect.collidelist([sprite.rect for sprite in self.collision_sprites]) != -1 else False

    def animate(self, dt):
        if self.direction.x != 0:
            self.frame_index += self.animation_speed * dt
            self.flip = self.direction.x < 0
        else:
            self.frame_index = 0

        self.frame_index = 1 if not self.on_floor else self.frame_index

        self.image = self.frames[int(self.frame_index) % len(self.frames)]
        self.image = pygame.transform.flip(self.image, self.flip, False)

    def update(self, dt):
        self.check_floor()
        self.input()
        self.move(dt)
        self.animate(dt)

class Bee(AnimatedSprite):
    def __init__(self, frames, pos, groups):
        super().__init__(frames, pos, groups)
    
    def update(self, dt):
        self.animate(dt)

class Worm(AnimatedSprite):
    def __init__(self, frames, pos, groups):
        super().__init__(frames, pos, groups)

    def update(self, dt):
        self.animate(dt)