from Resources import *


class DragonSprite(pygame.sprite.Sprite):
    PW = None
    PH = None

    def __init__(self):
        super().__init__()
        self.PW = dragonim.get_width()
        self.PH = dragonim.get_height()
        self.image = dragonim
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREENW / 2
        self.rect.centery = self.PH / 2
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

    def spawnBoss2(self):
        self.spawn = True

    def getBullets(self):
        fire_bullet_group = pygame.sprite.Group()
        for firebullets in self.bulletList:
            fire_bullet_group.add(firebullets)
        return fire_bullet_group

    def removeBullet(self, bullet):
        for firebullets in self.bulletList:
            if firebullets == bullet:
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
        self.PW = dragonim.get_width()
        self.PH = dragonim.get_height()
        self.image = fireim
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
