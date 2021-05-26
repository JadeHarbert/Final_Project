from Resources import *
from PlayerSprite import *

class ChasingSprite(pygame.sprite.Sprite):
    PW = None
    PH = None

    def __init__(self, loc, player=PlayerSprite):
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
        self.player = player

        self.isTearSprite = False

    def follow(self):
        if self.player.rect.x > self.rect.x:
            self.rect.x += 1
        else:
            self.rect.x -= 1
        if self.player.rect.y > self.rect.y:
            self.rect.y += 1.25
        else:
            self.rect.y -= 1


    def update(self, val):
        if val:
            self.rect.centery += 1
        self.follow()
