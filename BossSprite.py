import pygame
from Resources import *
from GlobalVariables import *

class BossSprite(pygame.sprite.Sprite):
    PW = None
    PH = None

    def __init__(self):
        super().__init__()
        self.PW = bossim.get_width()
        self.PH = bossim.get_height()
        self.image = bossim
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREENW/2
        self.rect.centery = self.PH/2
        self.mask = pygame.mask.from_surface(self.image)
        self.health = 10
        self.spawn = False
        self.bulletList = []
        self.timer = 0
        self.timermax = 100
        self.direction = "right"
        self.isTearSprite = False

        self.isTearSprite = False

    def update(self):
        if self.direction == "right":
            self.rect.centerx += 1
        if self.rect.right >= SCREENW:
            self.direction = 'left'
        if self.direction == "left":
            self.rect.centerx -= 1
        if self.rect.left <= 0:
            self.direction = "right"

        if self.timer == self.timermax:
            self.bulletList.append(BossBullet(self.rect.center))
            self.bulletList.append(BossBullet(self.rect.topleft))
            self.bulletList.append(BossBullet(self.rect.topright))
            self.timer = 0
        self.timer += 1

    def spawnBoss(self):
        self.spawn = True

    def getBullets(self):
        enemy_bullet_group = pygame.sprite.Group()
        for enemybullets in self.bulletList:
            enemy_bullet_group.add(enemybullets)
        return enemy_bullet_group

    def removeBullet(self, bullet):
        for enemybullets in self.bulletList:
            if enemybullets == bullet:
                self.bulletList.remove(bullet)
                break

    def hit(self, hit):
        if self.spawn:
            self.health -= hit

    def dead(self):
        return self.health < 0

class BossBullet(pygame.sprite.Sprite):
    PW = None
    PH = None

    def __init__(self, loc):
        super().__init__()
        self.PW = bossim.get_width()
        self.PH = bossim.get_height()
        self.image = bulletim
        self.rect = self.image.get_rect()
        self.rect.center = loc
        self.mask = pygame.mask.from_surface(self.image)
        self.health = 10
        self.spawn = False
        self.delete = False

    def update(self):
        self.rect.centery += 2

    def deleted(self):
        self.delete = True