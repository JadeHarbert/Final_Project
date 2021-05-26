import pygame
from Resources import *
from GlobalVariables import *


class PlayerSprite(pygame.sprite.Sprite):
    PW = None
    PH = None
    jumped = False

    def __init__(self, loc):
        super().__init__()
        self.PW = playerim.get_width()
        self.PH = playerim.get_height()
        self.image = playerim
        self.rect = self.image.get_rect()
        self.rect.center = loc
        self.rect.centery -= self.PH/2
        self.rect.centerx -= self.PW / 2
        self.mask = pygame.mask.from_surface(self.image)
        self.movingLeft = True
        self.x = loc[0]
        self.y = loc[1]
        self.jumpheight = 250
        self.jumpnow = 0
        self.fell = False
        self.collide = False
        self.addpoint = False
        self.life = 5
        self.bottom = False
        self.damage = 1
        self.landed = False

    def moveRight(self):
        if self.rect.centerx == SCREENW:
            self.rect.centerx = 0
        self.rect.centerx += 1
        self.image = rightim

    def moveLeft(self):
        if self.rect.centerx == 0:
            self.rect.centerx = SCREENW
        self.rect.centerx -= 1
        self.image = leftim

    def moveDown(self):
        if self.rect.centery == 0:
            self.rect.centery = SCREENH
        self.rect.centery += 1
        self.image = jumpim

    def update(self):
        if self.jumped == False and not self.bottom:
            self.rect.centery += 1
        if self.jumped == True:
            self.rect.centery -= 1
            self.jumpnow += 1.25
        if self.jumpheight <= self.jumpnow:
            self.jumped = False
            self.jumpnow = 0
        if self.rect.centery >= SCREENH:
            self.life = 0

    def landing(self):
        self.landed = False
        self.test2 = False

    def colliding(self, val, bot):
        self.collide = val
        self.bottom = bot
        self.test2 = False
        if self.collide and self.bottom:
            self.image = playerim
            self.test2 = True

    def jump(self):
        if self.collide and self.bottom and self.jumpnow == 0:
            self.jumped = True
            jumpsound.play()
            self.image = jumpim
            self.landed = True


class BulletSprite(pygame.sprite.Sprite):
    PW = None
    PH = None
    jumped = False

    def __init__(self, loc, leftDiag, rightDiag):
        super().__init__()
        self.PW = bulletim.get_width()
        self.PH = bulletim.get_height()
        self.image = bulletim
        self.rect = self.image.get_rect()
        self.rect.center = loc
        self.rect.centery -= self.PH / 2
        self.rect.centerx -= self.PW / 2
        self.mask = pygame.mask.from_surface(self.image)
        self.m = 0
        self.leftDiag = leftDiag
        self.rightDiag = rightDiag

    def update(self):
        if not self.leftDiag and not self.rightDiag:
            self.rect.centery -= 2
        elif self.leftDiag:
            self.rect.centery -= 2
            self.rect.centerx -= 1
        else:
            self.rect.centery -= 2
            self.rect.centerx += 1
