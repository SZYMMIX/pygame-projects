from settings import *
from sprites import *
from groups import AllSprites

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.running = True

        self.hit_sound = pygame.mixer.Sound(join("Assets", "audio", "hit1.mp3"))
        self.hit_sound.set_volume(0.1)
        self.score_sound = pygame.mixer.Sound(join("Assets", "audio", "score.mp3"))
        self.score_sound.set_volume(0.1)

        self.all_sprites = AllSprites()
        self.paddle_sprites = pygame.sprite.Group()
        self.player = Player((self.all_sprites, self.paddle_sprites))
        self.ball = Ball(self.all_sprites, self.paddle_sprites, self.update_score, self.hit_sound, self.score_sound)
        Opponent((self.all_sprites, self.paddle_sprites), self.ball)


        self.score = {"player": 0, "opponent": 0}
        self.font = pygame.font.Font(join("Assets", "fonts", "PressStart2P-Regular.ttf"), 80)

        

    def display_score(self):
        player_surf = self.font.render(str(self.score["player"]), True, COLORS["bg detail"])
        player_rect = player_surf.get_frect(center = (WINDOW_WIDTH / 2 + 150, 200))
        self.display_surface.blit(player_surf, player_rect)

        opponent_surf = self.font.render(str(self.score["opponent"]), True, COLORS["bg detail"])
        opponent_rect = opponent_surf.get_frect(center = (WINDOW_WIDTH / 2 - 150, 200))
        self.display_surface.blit(opponent_surf, opponent_rect)

        dash_height = 20   
        gap = 15           
        x = WINDOW_WIDTH // 2
        y = 0

        while y < WINDOW_HEIGHT:
            pygame.draw.line(self.display_surface, COLORS["bg detail"], (x, y), (x, y + dash_height), 6)
            y += dash_height + gap

    def update_score(self, side):
        self.score[side] += 1

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
            self.all_sprites.update(dt)

            self.display_surface.fill(COLORS["bg"])
            self.display_score()
            self.all_sprites.draw()
            pygame.display.update()
        
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()