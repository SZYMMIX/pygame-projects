from settings import *
from timer import Timer
from math import sin
from random import randint

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class Bullet(Sprite):
    def __init__(self, pos, surf, direction, groups, level_width):
        super().__init__(pos, surf, groups)

        self.image = pygame.transform.flip(self.image, direction == -1, False)

        self.level_width = level_width
        self.direction = direction
        self.speed = 800

    def update(self, dt):
        self.rect.x += self.direction * self.speed * dt 

        if self.rect.left > self.level_width + WINDOW_WIDTH or self.rect.right < 0:
            self.kill()

class Fire(Sprite):
    def __init__(self, pos, surf, groups, player):
        super().__init__(pos, surf, groups)
        self.player = player
        self.flip = player.flip
        self.timer = Timer(150, autostart = True, func = self.kill)
        self.y_offset = pygame.Vector2(0,8)

        if self.player.flip:
            self.rect.midright = self.player.rect.midleft + self.y_offset
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.rect.midleft = self.player.rect.midright + self.y_offset

    def update(self, dt):
        self.timer.update()

        if self.player.flip:
            self.rect.midright = self.player.rect.midleft + self.y_offset
            
        else:
            self.rect.midleft = self.player.rect.midright + self.y_offset

        if self.flip != self.player.flip:
            self.kill()

class AnimatedSprite(Sprite):
    def __init__(self, frames, pos, groups):
        self.frames, self.frame_index, self.animation_speed = frames, 0, 9
        super().__init__(pos, self.frames[self.frame_index], groups)

    def animate(self,dt):
        self.frame_index += self.animation_speed * dt

        self.image = self.frames[int(self.frame_index) % len(self.frames)]

class Enemy(AnimatedSprite):
    def __init__(self, frames, pos, groups):
        super().__init__(frames, pos, groups)
        self.death_timer = Timer(200, func= self.kill)

    def destroy(self):
        self.death_timer.activate()
        self.animation_speed = 0
        self.image = pygame.mask.from_surface(self.image).to_surface()
        self.image.set_colorkey('black')

    def update(self, dt):
        self.death_timer.update()
        if not self.death_timer:
            self.move(dt)
            self.animate(dt)
            self.constraint()


class Player(AnimatedSprite):
    def __init__(self, pos, groups, collision_sprites, frames, create_bullet):
        super().__init__(frames, pos, groups)
        self.flip = False
        self.create_bullet = create_bullet

        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2()
        self.speed = 400
        self.gravity = 50
        self.jump_speed = 18
        self.double_jump = True
        self.on_floor = False
        self.shoot_timer = Timer(500)

    def input(self):
        keys = pygame.key.get_pressed()
        input_just_pressed = pygame.key.get_just_pressed()
        
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])

        if input_just_pressed[pygame.K_UP] and self.on_floor == True :
            self.direction.y = -self.jump_speed
        elif input_just_pressed[pygame.K_UP] and self.double_jump:
            self.direction.y = -self.jump_speed
            self.double_jump = False

        if keys[pygame.K_SPACE] and not self.shoot_timer:
            self.create_bullet(self.rect.center, -1 if self.flip else 1)
            self.shoot_timer.activate()

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

        if bottom_rect.collidelist([sprite.rect for sprite in self.collision_sprites]) != -1:
            self.on_floor = True
            self.double_jump = True
        else:
            self.on_floor = False

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
        self.shoot_timer.update()
        self.check_floor()
        self.input()
        self.move(dt)
        self.animate(dt)

class Bee(Enemy):
    def __init__(self, frames, pos, groups, speed):
        super().__init__(frames, pos, groups)
    
        self.speed = speed
        self.amplitude = randint(300, 400)
        self.frequency = randint(300, 600)

    def move(self, dt):
        self.rect.x -= self.speed * dt
        self.rect.y += sin(pygame.time.get_ticks() / self.frequency) * self.amplitude * dt

    def constraint(self):
        if self.rect.right <= 0:
            self.kill()


class Worm(Enemy):
    def __init__(self, frames, rect, groups):
        super().__init__(frames, rect.topleft, groups)
        self.move_rect = rect
        self.rect.bottomleft = rect.bottomleft
        self.direction = 1
        self.speed = randint(140, 180)


    def move(self, dt):
        self.rect.x += self.direction * self.speed * dt

    def constraint(self):
        if not self.move_rect.contains(self.rect):
            self.direction *= -1
            self.frames = [pygame.transform.flip(frame, True, False) for frame in self.frames]
