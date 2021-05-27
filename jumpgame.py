from random import randint
from sys import exit

import pygame.time
from pygame.locals import *

from AstroidSprite import *
from BossSprite import *
from EraserSprite import *
from LifeSprite import *
from PlatformSprite import *
from PlayerSprite import *
from TearSprite import *
from DragonSprite import *
from ChasingSprite import *
from SpiderSprite import *
from HoleSprite import *

screen.blit(splash, splashrect.topleft)
clock = pygame.time.Clock()

font = pygame.font.Font(resourcesS + 'HeinWriting.ttf', 32)

showSplash = True
while showSplash:
    keys = pygame.key.get_pressed()
    screen.blit(splashscreen, (0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            showSplash = False
    pygame.display.update()


def show_gm_screen():
    screen.blit(background2, (0, 0))
    screen.blit(font.render(("Score: " + str(SCORE)), False, (0, 0, 0)), (SCREENW / 2 - 60, SCREENH / 4 - 45))


def show_win_screen():
    screen.blit(background3, (0, 0))
    screen.blit(font.render(("Score: " + str(SCORE)), False, (0, 0, 0)), (SCREENW / 2 - 60, SCREENH / 4 - 45))


screen.blit(background, (0, 0))

Fullscreen = False
loop = True

gameloop = True
gameover = False
while loop:
    # initialization:
    enemy_sprites = pygame.sprite.Group()
    life_sprites = pygame.sprite.Group()
    hole_sprites = pygame.sprite.Group()
    screen.blit(background, (0, 0))

    platform_group = pygame.sprite.Group()
    test = randint(0, SCREENW)

    platform = PlatformSprite((SCREENW / 2, SCREENH), platformim)
    platform_group.add(platform)

    layer = SCREENH - 30
    for x in range(0, 9):
        platform = PlatformSprite((randint(0, SCREENW), randint(layer, layer + 60)), platformim)
        platform_group.add(platform)
        layer -= 60

    player = PlayerSprite((SCREENW / 2, SCREENH - platform.PH))
    player_group = pygame.sprite.Group()
    player_group.add(player)
    spawnAstroid = True

    bullet_group = pygame.sprite.Group()
    enemy_bullet_group = pygame.sprite.Group()
    fire_bullet_group = pygame.sprite.Group()
    web_bullet_group = pygame.sprite.Group()

    boss1 = BossSprite()
    boss2 = DragonSprite()
    boss3 = SpiderSprite()
    boss_group = pygame.sprite.Group()
    boss_group.add(boss1)
    dragon_group = pygame.sprite.Group()
    dragon_group.add(boss2)
    spider_group = pygame.sprite.Group()
    spider_group.add(boss3)

    spawnTear = True

    spawnEraser = True

    spawnLife = True

    spawnChaser = True

    last_update = 0
    spawnHole = True

    # global SCORE
    SCORE = 1

    lose = False
    win = False
    while gameloop:
        screen.blit(background, (0, 0))
        if player.life <= 0:
            gameloop = False
            gameover = True
            lose = True
        if boss3.dead():
            gameloop = False
            gameover = True
            win = True
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.mixer.quit()
                loop = False
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.mixer.quit()
                    pygame.quit()
                if Fullscreen:
                    screen = pygame.display.set_mode((640, 400), 0, 32)
                if event.key == K_f and (event.mod & pygame.KMOD_SHIFT):
                    Fullscreen = not Fullscreen
                    if Fullscreen:
                        screen = pygame.display.set_mode((640, 500), FULLSCREEN, 32)
                    else:
                        screen = pygame.display.set_mode((640, 500), 0, 32)
                if event.key == pygame.K_SPACE:
                    bullet = BulletSprite(player.rect.center, False, False)
                    bullet_group.add(bullet)
                    shootsound.play()
                if event.key == pygame.K_q:
                    bullet = BulletSprite(player.rect.center, True, False)
                    bullet_group.add(bullet)
                    shootsound.play()
                if event.key == pygame.K_e:
                    bullet = BulletSprite(player.rect.center, False, True)
                    bullet_group.add(bullet)
                    shootsound.play()


        now = pygame.time.get_ticks()
        testcollision = False
        bottom = False
        for plat in platform_group:
            if plat.rect.centery == SCREENH:
                platform_group.add(PlatformSprite((randint(25, SCREENH - 25), randint(layer, layer + 65)), platformim))
                platform_group.remove(plat)
            if pygame.sprite.collide_mask(plat, player):
                testcollision = True
                bottom = player.rect.bottom + 5 >= plat.rect.top and player.rect.bottom <= plat.rect.top + 5
                break

        player.colliding(testcollision, bottom)

        if player.landed and player.test2 and player.jumpnow == 0:
            SCORE += 1
            player.landing()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player.moveLeft()
        if keys[pygame.K_d]:
            player.moveRight()
        if keys[pygame.K_w]:
            if bottom:
                player.jump()
                if SCORE % 5 == 0 and spawnAstroid:
                    for x in range(int(SCORE / 5)):
                        enemy_sprites.add(AstroidSprite((randint(enemyim.get_width() // 2, SCREENW),
                                                         -enemyim.get_height() - 75), enemyim))
                    spawnAstroid = False
                elif SCORE % 6 == 0:
                    spawnAstroid = True
                if SCORE % 12 == 0 and spawnHole:
                    for x in range(int(SCORE / 12)):
                        hole_sprites.add(HoleSprite((randint(holeim.get_width() // 2, SCREENW), -holeim.get_height()
                                                     - 75), holeim))
                    spawnHole = False
                elif SCORE % 13 == 0:
                    spawnHole = True
                if SCORE % 8 == 0 and spawnTear:
                    enemy_sprites.add(TearSprite((randint(holeim.get_width() // 2, SCREENW),
                                                  -holeim.get_height() - 75)))
                    spawnTear = False
                elif SCORE % 9 == 0:
                    spawnTear = True
                if SCORE % 7 == 0 and spawnEraser:
                    enemy_sprites.add(EraserSprite((
                        randint(eraserim.get_width() // 2, SCREENW), -eraserim.get_height() - 75)))
                    spawnEraser = False
                elif SCORE % 8 == 0:
                    spawnEraser = True
                if SCORE % 10 == 0 and spawnLife:
                    life_sprites.add(LifeSprite((
                        randint(lifeim.get_width() // 2, SCREENW), -lifeim.get_height() - 75)))
                    spawnLife = False
                elif SCORE % 11 == 0:
                    spawnLife = True
                if SCORE % 14 == 0 and spawnChaser:
                    enemy_sprites.add(ChasingSprite((
                        randint(eraserim.get_width() // 2, SCREENW), -eraserim.get_height() - 75), player))
                    spawnChaser = False
                elif SCORE % 15 == 0:
                    spawnChaser = True

        time_passed = clock.tick(120)
        time_passed_seconds = time_passed / 1000.0

        screen.blit(font.render(("Score: " + str(SCORE)), False, (0, 0, 0)), (0, 0))
        screen.blit(font.render(("Lives: " + str(player.life)), False, (0, 0, 0)), (SCREENW - 125, 0))

        for enemy in enemy_sprites:
            if pygame.sprite.collide_mask(enemy, player):
                if enemy.isTearSprite:
                    hitsound.play()
                    SCORE += 1
                    enemy_sprites.remove(enemy)
                    player.life = 0
                else:
                    hitsound.play()
                    enemy_sprites.remove(enemy)
                    player.life -= 1
            for bullets in bullet_group:
                if pygame.sprite.collide_mask(bullets, enemy):
                    if not enemy.isTearSprite:
                        killsound.play()
                        SCORE += 1
                        enemy_sprites.remove(enemy)
                    else:
                        bullet_group.remove(bullets)
                if bullets.rect.centery < -250:
                    bullet_group.remove(bullets)
                if bullets.rect.centery > SCREENH:
                    bullet_group.remove(bullets)

        for life in life_sprites:
            if pygame.sprite.collide_mask(life, player):
                lifesound.play()
                life_sprites.remove(life)
                player.life += 1

        for hole in hole_sprites:
            if pygame.sprite.collide_mask(hole, player):
                lifesound.play()
                life_sprites.remove(hole)
                player.life = 0

        for web in web_bullet_group:
            if pygame.sprite.collide_mask(web, player):
                hitsound.play()
                player.life -= 1
                web_bullet_group.remove(web)

        for bullets in bullet_group:
            if pygame.sprite.collide_mask(bullets, boss1) and boss1.spawn and boss1.health >= 0:
                enemysound.play()
                boss1.hit(player.damage)
                bullet_group.remove(bullets)
            if pygame.sprite.collide_mask(bullets, boss2) and boss2.spawn and boss2.health >= 0:
                enemysound.play()
                boss2.hit(player.damage)
                bullet_group.remove(bullets)
            if pygame.sprite.collide_mask(bullets, boss3) and boss3.spawn:
                enemysound.play()
                boss3.hit(player.damage)
                bullet_group.remove(bullets)

        enemy_bullet_group.update()
        enemy_bullet_group.draw(screen)
        fire_bullet_group.update()
        fire_bullet_group.draw(screen)
        web_bullet_group.update()
        web_bullet_group.draw(screen)

        if SCORE >= 5 and not boss1.dead():
            boss1.spawnBoss()
            boss_group.update()
            boss_group.draw(screen)
        if SCORE >= 10 and not boss2.dead():
            boss2.spawnBoss2()
            dragon_group.update()
            dragon_group.draw(screen)
        if SCORE >= 15 and not boss3.dead():
            boss3.spawnBoss3()
            spider_group.update()
            spider_group.draw(screen)

        for enemybullets in boss1.getBullets():
            if pygame.sprite.collide_mask(enemybullets, player):
                player.life -= 1
                boss1.removeBullet(enemybullets)
                break
            if enemybullets.rect.centery >= SCREENH:
                boss1.removeBullet(enemybullets)
                break

        for firebullets in boss2.getBullets():
            if pygame.sprite.collide_mask(firebullets, player):
                player.life -= 2
                boss2.removeBullet(firebullets)
            if firebullets.rect.centery >= SCREENH:
                boss2.removeBullet(firebullets)
                break

        for webbullets in boss3.getBullets():
            if pygame.sprite.collide_mask(webbullets, player):
                player.webbed = True
                player.life -= 1
                boss3.removeBullet(webbullets)
                last_update = now
                print("webbed")
            if webbullets.rect.centery >= SCREENH:
                boss3.removeBullet(webbullets)
                break

        if player.webbed and now - last_update > 50000:
            player.webbed = False
            print("unwebbed")

        enemy_bullet_group = boss1.getBullets()
        fire_bullet_group = boss2.getBullets()
        web_bullet_group = boss3.getBullets()
        player.update()
        player_group.draw(screen)
        platform_group.update(player.jumped)
        platform_group.draw(screen)
        enemy_sprites.update(player.jumped)
        enemy_sprites.draw(screen)
        hole_sprites.update(player.jumped)
        hole_sprites.draw(screen)
        life_sprites.update(player.jumped)
        life_sprites.draw(screen)
        bullet_group.update()
        bullet_group.draw(screen)
        pygame.display.update()
        playsound = True

    while gameover:
        while lose:
            keys = pygame.key.get_pressed()
            if playsound:
                diesound.play()
                playsound = False
            show_gm_screen()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    gameover = False
                    gameloop = True
                    lose = False
            pygame.display.update()
        while win:
            keys = pygame.key.get_pressed()
            if playsound:
                winsound.play()
                playsound = False
            show_win_screen()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    gameover = False
                    gameloop = True
                    win = False
            pygame.display.update()
