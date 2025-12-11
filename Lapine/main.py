from settings import * 
from sprites import *
from groups import *
from support import *
from timer import Timer
from random import randint

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Lapine')
        self.clock = pygame.time.Clock()
        self.running = True

        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        self.load_assets()
        self.setup()

        self.bee_timer = Timer(2000, func = self.create_bee, autostart = True, repeat = True)

    def create_bee(self):
        Bee(frames = self.bee_frames, pos = (self.level_width + WINDOW_WIDTH, randint(50, self.level_height - 50)), groups = (self.all_sprites, self.enemy_sprites), speed = randint(200, 350))

    def create_bullet(self, pos, direction):
        x = pos[0] + direction * 34 if direction == 1 else pos[0] + direction * 34 - self.bullet_surf.get_width()
        Bullet((x, pos[1]), self.bullet_surf, direction, (self.all_sprites, self.bullet_sprites), self.level_width)
        Fire(pos, self.fire_surf, self.all_sprites, self.player)
        self.audio['shoot'].play()


    def load_assets(self):
        self.player_frames = import_folder("Assets", "images", "player")

        self.bullet_surf = import_image("Assets", "images", "gun", "bullet")
        self.fire_surf = import_image("Assets", "images", "gun", "fire")
        self.bee_frames = import_folder("Assets", "images", "enemies", "bee")
        self.worm_frames = import_folder("Assets", "images", "enemies", "worm")

        self.audio = audio_importer("Assets", "audio")

    def setup(self):
        map = load_pygame(join("Assets", "data", "maps", "world.tmx"))
        self.level_width = map.width * TILE_SIZE
        self.level_height = map.height * TILE_SIZE

        for x, y, image in map.get_layer_by_name('Main').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, (self.all_sprites, self.collision_sprites))

        for x, y, image in map.get_layer_by_name('Decoration').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

        for marker in map.get_layer_by_name('Entities'):
            if marker.name == 'Player':
                self.player = Player((marker.x, marker.y), self.all_sprites, self.collision_sprites, self.player_frames, self.create_bullet)

            if marker.name == 'Worm':
                Worm(self.worm_frames, pygame.FRect(marker.x, marker.y, marker.width, marker.height), (self.all_sprites, self.enemy_sprites))
        
        self.audio['music'].set_volume(0.04)
        self.audio['music'].play(-1)
        self.audio['shoot'].set_volume(0.04)
        self.audio['impact'].set_volume(0.04)

    def collision(self):
        for bullet in self.bullet_sprites:
            sprite_collision = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False, pygame.sprite.collide_mask)
            if sprite_collision:
                self.audio['impact'].play()
                bullet.kill()
                for sprite in sprite_collision:
                    sprite.destroy()

        if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
            self.running = False

    def run(self):
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False 
            
            self.bee_timer.update()
            self.all_sprites.update(dt)
            self.collision()

            self.display_surface.fill(BG_COLOR)
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()
        
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run() 