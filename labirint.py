from pygame import *
from random import *
import time as tm
font.init()

windowWidth = 1280
windowHeight = 720

mainWindow = display.set_mode((windowWidth, windowHeight))
display.set_caption('lab')
mainWindow.fill((0, 0, 255))
background = transform.scale(image.load('bg_castle.png'), (windowWidth, windowHeight))

class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, width, height):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(img), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def show(self):
        mainWindow.blit(self.image, (self.rect.x, self.rect.y))

class Hero(GameSprite):
    def __init__(self, img, x, y, width, height, speed):
        GameSprite.__init__(self, img, y, x, width, height)
        self.speed = speed
        self.gravity = 15
        self.JumpCount = 4
        self.isJump = False
        self.standImage = transform.scale(image.load('alienYellow.png'), (width, height))
        self.jumpImage = transform.scale(image.load('alienYellow_jump.png'), (width, height))
        self.rightImage = transform.scale(image.load('alienYellow_walk1.png'), (width, height))
        self.leftImage = transform.flip(self.rightImage, True, False)
        self.doorOpen = False
        self.haveKey = False
        self.haveCoin = False
    def update(self):  # движение
        keys = key.get_pressed()
        if keys[K_d]:
            self.image = self.rightImage
            self.rect.x += self.speed
        if keys[K_a]:
            self.image = self.leftImage
            self.rect.x -= self.speed

    def jump(self):    # прыжок
        keys = key.get_pressed()
        if keys[K_SPACE] or keys[K_w]:
            self.isJump = True
            self.image = self.jumpImage
        if self.isJump:
            self.rect.y -= self.JumpCount ** 2.1
            self.JumpCount -= 0.2
            if self.JumpCount <= 0:
                self.isJump = False
                self.JumpCount = 4


    def falling(self): # падение
        if sprite.spritecollide(self, walls, False):
            platformsTouched = sprite.spritecollide(self, walls, False)
            for platform in platformsTouched:
                if platform.rect.top < self.rect.bottom:
                    self.gravity = 0
                    if self.isJump == False:
                        self.image = self.standImage
        else:
            if self.isJump == False:
                self.gravity = 15
    
    def topCollide(self):
        pass


class Enemy(GameSprite):
    def __init__(self, img, x, y, width, height, speed, pointLeft, pointRight):
        GameSprite.__init__(self, img, y, x, width, height)
        self.speed = speed
        self.pointLeft = pointLeft
        self.pointRight = pointRight
        self.direction = 'LEFT'

    def update(self):
        if self.rect.x <= self.pointLeft:
            self.direction = 'RIGHT'
        elif self.rect.x >= self.pointRight:
            self.direction = 'LEFT'
        
        if self.direction == 'LEFT':
            self.rect.x -= self.speed
        elif self.direction == 'RIGHT':
            self.rect.x += self.speed




player = Hero('alienYellow.png', 515, 100, 66, 82, 7)
spider1 = Enemy('spider.png', 350, 800, 71, 82, 5, 650, 900)
spider2 = Enemy('spider.png', 245, 400, 71, 82, 5, 210, 400)
door = GameSprite('door_closedMid.png', 20, 120, 70, 70)
point = GameSprite('hud_keyYellow.png', 1200, 350, 44, 40)
coin = GameSprite('hud_coins.png', 1200, 500, 47, 47)
#платформы
walls = sprite.Group()

platformX = 0
for i in range (19):
    wall = GameSprite('beamBoltsHoles.png', platformX, 570, 70, 60) #70, 70
    walls.add(wall)
    platformX += 70 #70

platformX = 640
for i in range (10):
    wall = GameSprite('beamBoltsHoles.png', platformX, 425, 70, 60) #70, 70
    walls.add(wall)
    platformX += 70 #70

platformX = 200
for i in range (4):
    wall = GameSprite('beamBoltsHoles.png', platformX, 325, 70, 60) #70, 70
    walls.add(wall)
    platformX += 70 #70

platformX = 10
for i in range (2):
    wall = GameSprite('beamBoltsHoles.png', platformX, 185, 70, 60) #70, 70
    walls.add(wall)
    platformX += 70 #70

platformX = 300
for i in range (10):
    wall = GameSprite('beamBoltsHoles.png', platformX, 100, 70, 60) #70, 70
    walls.add(wall)
    platformX += 70 #70

fps = 60
clock = time.Clock()

game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    mainWindow.blit(background, (0, 0))   
    door.show()
    point.show()
    player.show()
    player.falling()
    player.jump()
    player.update()

    spider1.show()
    spider1.update()
    spider2.show()
    spider2.update()
    coin.show()
    player.rect.y += player.gravity
    walls.draw(mainWindow)

    if sprite.collide_rect(player, point):
        player.haveKey = True
    if player.haveKey:
        if point.rect.y > 10:
            point.rect.y -= 10
            point.rect.x += 1
    if sprite.collide_rect(player, coin):
        player.haveCoin = True
    if player.haveCoin:
        if coin.rect.y > 10:
            coin.rect.y -= 10
            coin.rect.x -= 0.51

    if sprite.collide_rect(player, door):
        if player.haveKey:
            player.doorOpen = True
    if player.doorOpen:
        door.image = image.load('door_openMid.png')
        if sprite.collide_rect(player, door):
            exitText = font.SysFont('Verdana', 25).render('press E', True, (255, 255, 255))
            mainWindow.blit(exitText, (door.rect.left, door.rect.top - 50))

    if sprite.collide_rect(player, spider1) or sprite.collide_rect(player, spider2):
        player.rect.x = 50
        player.rect.y = 400
        
    display.update()
    clock.tick(fps)