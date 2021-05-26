import pygame


class AstroidSprite(pygame.sprite.Sprite):
    PW = None
    PH = None

    def __init__(self, loc, im):
        super().__init__()
        self.PW = im.get_width()
        self.PH = im.get_height()
        self.image = im
        self.rect = self.image.get_rect()
        self.rect.center = loc
        self.mask = pygame.mask.from_surface(self.image)
        self.isTearSprite = False

        self.isTearSprite = False

    def update(self, val):
        self.rect.centery += 2
