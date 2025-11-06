from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, animations):
        super().__init__(groups)
        self.animations = animations
        self.status = 'down'
        self.frame_index = 0
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.math.Vector2()
        self.speed = 200
        self.animation_speed = 7

    def _handle_movement(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
        
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
        
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'

        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'

        else:
            self.direction.x = 0
    
    
    def _animate(self, dt):
        current_animation = self.animations[self.status]

        if self.direction:
            self.frame_index +=  self.animation_speed * dt
            
            if self.frame_index >= len(current_animation):
                self.frame_index = 0
        else:
            self.frame_index = 0
        
        self.image = current_animation[int(self.frame_index)]
        self.rect = self.image.get_frect(center = self.rect.center)


    def update(self, dt):
        self._handle_movement()

        self.direction = self.direction.normalize() if self.direction else self.direction

        self.rect.center += self.direction * dt * self.speed

        self._animate(dt)