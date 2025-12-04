from settings import * 

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    def draw(self):
        for sprite in self:
            if hasattr(sprite, "glow_surf"):
                glow_rect = sprite.glow_surf.get_rect(center=sprite.rect.center)
                self.display_surface.blit(sprite.glow_surf, glow_rect)

            self.display_surface.blit(sprite.image, sprite.rect)