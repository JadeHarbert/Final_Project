from Resources import *


class EraserSprite(pygame.sprite.Sprite):
    PW = None
    PH = None

    def __init__(self, loc):
        super().__init__()
        self.PW = eraserim.get_width()
        self.PH = eraserim.get_height()
        self.image = eraserim
        self.rect = self.image.get_rect()
        self.rect.center = loc
        self.rect.centery -= self.PH/2
        self.rect.centerx -= self.PW / 2
        self.mask = pygame.mask.from_surface(self.image)
        self.isTearSprite = False
        self.damage = 1

        self.isTearSprite = False

    def update(self, val):
        if val:
            self.rect.centery += 1
