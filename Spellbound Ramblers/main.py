from settings import *
from player import Player
from sprites import *
from random import randint

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
        for _ in range(randint(1,5)):
            CollisionSprite(self.all_sprites, (randint(200, WINDOW_WIDTH - 200), randint(200, WINDOW_HEIGHT - 200)), (randint(50, 200), randint(100, 200)))

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