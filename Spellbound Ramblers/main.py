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
    


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Spellbound Ramblers")
        self.clock = pygame.time.Clock()
        self.running = True

        self._load_assets()

        self.all_sprites = pygame.sprite.Group()

        self.player = Player(self.all_sprites, self.player_animations)

    def _load_assets(self):
        self.player_animations = {'down': [], 'left': [], 'right': [], 'up': []}

        for status in self.player_animations.keys():
            path = join('Spellbound Ramblers', 'Assets', 'images', 'player', status)

            self.player_animations[status] = [pygame.image.load(join(path, f'{i}.png')).convert_alpha() for i in range(4)]

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.all_sprites.update(dt)
            self.display_surface.fill(BACKGROUND_COLOR)
            self.all_sprites.draw(self.display_surface)
            pygame.display.update()
        
        pygame.quit()



if __name__ == '__main__':
    game = Game()
    game.run()