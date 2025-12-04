from settings import *
from random import choice, uniform

class Paddle(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        self.image = pygame.Surface(SIZE["paddle"])
        pygame.draw.rect(self.image, COLORS["paddle"], pygame.FRect((0,0), SIZE["paddle"]), 0, 2)

        self.rect = self.image.get_frect(center = POS["player"])
        self.old_rect = self.rect.copy()
        self.direction = 0
        self.speed = SPEED["paddle"]

    def move(self, dt):
        self.rect.centery += self.direction * self.speed * dt
        self.rect.top = 0 if self.rect.top <= 0 else self.rect.top
        self.rect.bottom = WINDOW_HEIGHT if self.rect.bottom >= WINDOW_HEIGHT else self.rect.bottom

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.get_direction()
        self.move(dt)

class Player(Paddle):
    def __init__(self, groups):
        super().__init__(groups)

    def get_direction(self):
        keys = pygame.key.get_pressed()
        self.direction = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])

class Opponent(Paddle):
    def __init__(self, groups, ball):
        super().__init__(groups)
        self.ball = ball
        self.rect = self.image.get_frect(center = POS["opponent"])

    def get_direction(self):
        self.direction = 1 if self.rect.centery < self.ball.rect.centery else -1 



class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, paddle_sprites, update_score):
        super().__init__(groups)
        self.paddle_sprites = paddle_sprites
        self.update_score = update_score

        self.image = pygame.Surface(SIZE["ball"])
        self.image.fill(COLORS["ball"])
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        self.old_rect = self.rect.copy()
        self.direction = pygame.Vector2(choice((1,-1)), uniform(0.7, 0.8) * choice((1,-1)))
        self.speed = SPEED["ball"]

    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')


    def collision(self, direction):
        for sprite in self.paddle_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                        self.direction.x *= -1

                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                        self.direction.x *= -1
                
                else:
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.direction.y *= -1

                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        self.direction.y *= -1

                if self.speed < 1000: self.speed += 35

    def wall_collision(self):
        if self.rect.bottom >= WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
            self.direction.y *= -1

        if self.rect.top <= 0:
            self.rect.top = 0
            self.direction.y *= -1

        if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH:
            if self.rect.left <= 0: self.update_score('player')
            else: self.update_score('opponent')
            self.rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
            self.direction = pygame.Vector2(choice((1,-1)), uniform(0.7,0.8)*choice((1,-1)))
            self.speed = SPEED["paddle"]

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.move(dt)
        self.wall_collision()
