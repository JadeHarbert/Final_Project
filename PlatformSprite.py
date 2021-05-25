import pygame


class PlatformSprite(pygame.sprite.Sprite):
    PW = None
    PH = None

    def __init__(self, loc, im):
        super().__init__()
        self.PW = im.get_width()
        self.PH = im.get_height()
        self.image = im
        self.rect = self.image.get_rect()
        self.rect.center = loc
        self.rect.centery -= self.PH / 2 + 4
        self.rect.centerx -= self.PW / 2 + 4
        self.mask = pygame.mask.from_surface(self.image)

        self.damage = 1

    def update(self, val):
        if val:
            self.rect.centery += 1
