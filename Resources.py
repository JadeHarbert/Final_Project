import pygame
from GlobalVariables import *

resourcesS = 'resources//'
playerim = pygame.image.load(resourcesS + "playerimg.png")
enemyim = pygame.image.load(resourcesS + "scissors.png")
platformim = pygame.image.load(resourcesS + "platformimg.png")
jumpim = pygame.image.load(resourcesS + "jumpimg.png")
leftim = pygame.image.load(resourcesS + "leftimg.png")
rightim = pygame.image.load(resourcesS + "rightimg.png")
bulletim = pygame.image.load(resourcesS + "bulletimg.png")
holeim = pygame.image.load(resourcesS + "paperhole.png")
bossim = pygame.image.load(resourcesS + "ufoboss.png")
eraserim = pygame.image.load(resourcesS + "eraserimg.png")
lifeim = pygame.image.load(resourcesS + "heart.png")
background2 = pygame.image.load(resourcesS + "GameOver.png")
# background3 = pygame.image.load(resourcesS + "WinGame.png") Emily when you make the win screen you can put the name here
background_image_filename = resourcesS + 'backgroundimg.png'
win_image_filename = resourcesS + 'winscreen.png'
gameover_image_filename = resourcesS + 'GameOver.png'
splashscreen_image_filename = resourcesS + 'splashscreen.png'
sprite_image_filename = resourcesS + 'playerimg.png'
gameover_image_filename = resourcesS + "GameOver.png"
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREENW, SCREENH), 0, 32)
pygame.mixer.music.set_volume(0.25)
pygame.display.set_caption("Defeat the final boss to win the game")
jumpsound = pygame.mixer.Sound(resourcesS + "jump.wav")
shootsound = pygame.mixer.Sound(resourcesS + "shoot.wav")
hitsound = pygame.mixer.Sound(resourcesS + "hitsound.wav")
killsound = pygame.mixer.Sound(resourcesS + "hit.wav")
enemysound = pygame.mixer.Sound(resourcesS + "enemysound.wav")
winsound = pygame.mixer.Sound(resourcesS + "winsound.wav")
diesound = pygame.mixer.Sound(resourcesS + "gameover.wav")
lifesound = pygame.mixer.Sound(resourcesS + "lifesound.wav")
msg = "Lecture Survivor! Press Any Key to Play!"
my_font = pygame.font.Font(resourcesS + 'HeinWriting.ttf', 25)
splash = my_font.render(msg, True, (255, 0, 0), (0, 0, 0))
splashrect = splash.get_rect()
splashrect.center = (SCREENW / 2, SCREENH / 2)
background = pygame.image.load(background_image_filename).convert()
background2 = pygame.image.load(gameover_image_filename).convert()
background3 = pygame.image.load(win_image_filename).convert()
splashscreen = pygame.image.load(splashscreen_image_filename).convert()
spriteim = pygame.image.load(sprite_image_filename).convert_alpha()
gameoverim = pygame.image.load(gameover_image_filename).convert()
