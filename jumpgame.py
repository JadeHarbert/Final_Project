import pygame
from pygame.locals import *
from random import randint
from sys import exit
from PlayerSprite import *
from AstroidSprite import *
from PlatformSprite import *
from Resources import *
from GlobalVariables import *
from BossSprite import *
from TearSprite import *

screen.blit(splash, splashrect.topleft)
clock = pygame.time.Clock()
paddle_group = pygame.sprite.Group()
paddle_group.add()

font = pygame.font.Font(resourcesS + 'Baby Party.ttf', 32)

showSplash = True
while showSplash:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == MOUSEBUTTONDOWN:
            showSplash = False
    pygame.display.update()


def show_gm_screen():
    screen.blit(background2, (0, 0))
    screen.blit(font.render(("Score: " + str(SCORE)), False, (0, 0, 0)), (SCREENW / 2 - 60, SCREENH / 2))
    screen.blit(font.render(("GAME OVER!" + str()), False, (0, 0, 0)), (SCREENW / 2 - 100, SCREENH / 2 - 80))
    screen.blit(font.render(("Click to play again" + str()), False, (0, 0, 0)), (SCREENW / 2 - 145, SCREENH / 2 + 80))

def show_win_screen():
    screen.blit(background2, (0, 0))
    screen.blit(font.render(("Score: " + str(SCORE)), False, (0, 0, 0)), (SCREENW / 2 - 60, SCREENH / 2))
    screen.blit(font.render(("GAME WIN!" + str()), False, (0, 0, 0)), (SCREENW / 2 - 100, SCREENH / 2 - 80))
    screen.blit(font.render(("Click to play again" + str()), False, (0, 0, 0)), (SCREENW / 2 - 145, SCREENH / 2 + 80))

screen.blit(background, (0, 0))

Fullscreen = False
loop = True

gameloop = True
gameover = False
while loop:
    # initialization:
    enemy_sprites = pygame.sprite.Group()
    screen.blit(background, (0, 0))

    platform_group = pygame.sprite.Group()
    test = randint(0, SCREENW)

    platform = PlatformSprite((SCREENW / 2, SCREENH), platformim)
    platform_group.add(platform)

    layer = SCREENH - 75
    for x in range(0, 9):
        platform = PlatformSprite((randint(0, SCREENW), randint(layer, layer + 75)), platformim)
        platform_group.add(platform)
        layer -= 75

    player = PlayerSprite((SCREENW / 2, SCREENH - platform.PH))
    player_group = pygame.sprite.Group()
    player_group.add(player)
    spawnAstroid = True

    bullet_group = pygame.sprite.Group()
    enemy_bullet_group = pygame.sprite.Group()

    boss1 = BossSprite()
    boss_group = pygame.sprite.Group()
    boss_group.add(boss1)

    spawnTear = True

    global SCORE
    SCORE = 0

    lose = False
    win = False
    while gameloop:
        screen.blit(background, (0, 0))
        if player.life <= 0:
            gameloop = False
            gameover = True
            lose = True
        if boss1.dead():
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
            if event.type == pygame.MOUSEBUTTONUP:
                bullet = BulletSprite(player.rect.center)
                bullet_group.add(bullet)
                shootsound.play()

        testcollision = False
        bottom = False
        for plat in platform_group:
            if plat.rect.centery == SCREENH:
                platform_group.add(PlatformSprite((randint(0, SCREENH), randint(layer, layer + 75)), platformim))
                platform_group.remove(plat)
            if pygame.sprite.collide_mask(plat, player):
                testcollision = True
                bottom = player.rect.bottom + 5 >= plat.rect.top and player.rect.bottom <= plat.rect.top + 5
                break

        player.colliding(testcollision, bottom)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.moveLeft()
        if keys[pygame.K_RIGHT]:
            player.moveRight()
        if keys[pygame.K_UP]:
            if bottom:
                player.jump()
                if player.addpoint:
                    SCORE += 1
                if SCORE % 5 == 0 and spawnAstroid:
                    for x in range(int(SCORE / 5)):
                        enemy_sprites.add(AstroidSprite((randint(0, SCREENW), -enemyim.get_height() - 75), enemyim))
                    spawnAstroid = False
                elif SCORE % 6 == 0:
                    spawnAstroid = True
                if SCORE % 10 == 0 and spawnTear:
                    enemy_sprites.add(TearSprite((randint(0, SCREENW), -holeim.get_height() - 75)))
                    spawnTear = False
                elif SCORE % 11 == 0:
                    spawnTear = True

        time_passed = clock.tick(120)
        time_passed_seconds = time_passed / 1000.0

        screen.blit(font.render(("Score: " + str(SCORE)), False, (0, 0, 0)), (0, 0))
        screen.blit(font.render(("Lives: " + str(player.life)), False, (0, 0, 0)), (SCREENW - 125, 0))

        for enemy in enemy_sprites:
            if pygame.sprite.collide_mask(enemy, player):
                hitsound.play()
                enemy_sprites.remove(enemy)
                player.life -= 1
            for bullets in bullet_group:
                if pygame.sprite.collide_mask(bullets, enemy):
                    killsound.play()
                    enemy_sprites.remove(enemy)
                if bullets.rect.centery < 0:
                    bullet_group.remove(bullets)
                if bullets.rect.centery > SCREENH:
                    bullet_group.remove(bullets)


        for bullets in bullet_group:
            if pygame.sprite.collide_mask(bullets, boss1) and boss1.spawn:
                boss1.hit(player.damage)
                bullet_group.remove(bullets)

        enemy_bullet_group.update()
        enemy_bullet_group.draw(screen)

        if SCORE >= 50 and not boss1.dead():
            boss1.spawnBoss()
            boss_group.update()
            boss_group.draw(screen)

        for enemybullets in boss1.getBullets():
            if pygame.sprite.collide_mask(enemybullets, player):
                player.life -= 1
                boss1.removeBullet(enemybullets)
                break
            if enemybullets.rect.centery >= SCREENH:
                boss1.removeBullet(enemybullets)
                break

        enemy_bullet_group = boss1.getBullets()
        print(len(enemy_bullet_group))
        player.update()
        player_group.draw(screen)
        platform_group.update(player.jumped)
        platform_group.draw(screen)
        enemy_sprites.update(player.jumped)
        enemy_sprites.draw(screen)
        bullet_group.update()
        bullet_group.draw(screen)
        pygame.display.update()
        playsound = True

    while gameover:
        while lose:
            if playsound:
                diesound.play()
                playsound = False
            show_gm_screen()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                elif event.type == MOUSEBUTTONDOWN:
                    gameover = False
                    gameloop = True
                    lose = False
            pygame.display.update()
        while win:
            if playsound:
                diesound.play()
                playsound = False
            show_win_screen()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                elif event.type == MOUSEBUTTONDOWN:
                    gameover = False
                    gameloop = True
                    win = False
            pygame.display.update()