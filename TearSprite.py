from Resources import *


class TearSprite(pygame.sprite.Sprite):
    PW = None
    PH = None

    def __init__(self, loc):
        super().__init__()
        self.PW = holeim.get_width()
        self.PH = holeim.get_height()
        self.image = holeim
        self.rect = self.image.get_rect()
        self.rect.center = loc
        self.rect.centery -= self.PH/2
        self.rect.centerx -= self.PW / 2
        self.mask = pygame.mask.from_surface(self.image)

        self.damage = 1

        self.isTearSprite = True

    def update(self, val):
        if val:
            self.rect.centery += 1
