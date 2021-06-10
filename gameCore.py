import pygame
from pygame.locals import *
import sys
import random

from pypy import Gun
 
pygame.init()
vec = pygame.math.Vector2 
mainClock = pygame.time.Clock()

lead_x = 300
lead_y = 300

 
HEIGHT = 800
WIDTH = 640
ACC = 0.95
FRIC = -0.15
FPS = 60

BLACK = ((0,0,0))
WHITE =((255,255,255))
RED = ((255,0,0))
GREEN = ((0,255,0))
BLUE = ((0,0,255, 125))
YELLOW = ((255,255,0))
PINK = ((255,0,255))
SKYBLUE = ((0,255,255))
boxColours = [BLACK, WHITE, RED, GREEN,  YELLOW, PINK, SKYBLUE]


font = pygame.font.SysFont(None, 20)
 
FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D")
font_name = pygame.font.match_font('Adobe Arabic')

class Particle():
    def __init__(self):
        self.pos = vec(0,0)
        
    def setPos(self, player):
        self.pos = vec(player.playerMouseX, player.playerMouseY)

class Player(pygame.sprite.Sprite):
    def __init__(self, info):
        super().__init__()
        self.surf = pygame.Surface((30,30))
        self.surf.fill((128,255,40))
        self.rect = self.surf.get_rect(center = (WIDTH/2,HEIGHT/2))
        self.name = info    
        self.hp = 100
        self.score = 0
        self.isMoving = False
        self.playerMouseX, playerMouseY = pygame.mouse.get_pos()
        self.gunList = []
        
        self.pos = vec((10,385))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        
    def setScore(self, score):
        self.score = score
        
    def declareGun(self,surface):
        self.gun = Gun(self.pos.x, self.pos.y,surface)
        self.gunList.append(gun)
        
    def move(self):
        self.acc = vec(0,0)
        
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_a]:
            self.acc.x = - ACC
            self.isMoving = True
        if pressed_keys[K_d]:
            self.acc.x =  ACC
            self.isMoving = True
        if pressed_keys[K_w]:
            self.acc.y = - ACC
            self.isMoving = True
        if pressed_keys[K_s]:
            self.acc.y = ACC
            self.isMoving = True
        if pressed_keys[K_SPACE]:
            self.ACC = 0
            self.FRIC = 0
        if not pressed_keys:
            self.isMoving = False
     
        self.acc.x += self.vel.x * FRIC
        self.acc.y += self.vel.y * FRIC 
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.collision()
      
        
    
    def createMouse(self, surface, boxList):     
        pygame.mouse.set_visible(False)
        pygame.draw.circle(surface, (255,255,255), pygame.mouse.get_pos(), 4)
        if event.type == pygame.MOUSEBUTTONDOWN and self.isAiming(boxList):
            self.drawLine(surface)
            self.score += 1
        
        
        #LÖS SENARE  boxes.rect.center funkar ej 
    def isAiming(self, boxList):
        for boxes in boxList:
            if (boxes.rect.collidepoint(pygame.mouse.get_pos())):
                
                return True
    
    def drawLine(self, surface):
            pygame.draw.line(surface, boxColours[random.randint(0, 6)], (self.pos.x, self.pos.y - 15),pygame.mouse.get_pos(), random.randint(2,4))
            
    def checkBoXCollision(self, boxList):
        for boxes in boxList:
            if(self.rect.colliderect(boxes.rect)):
               self.hp -= 1
               
               return True
               
    
        
    def collision(self):
        self.rect.midbottom = self.pos
        if self.pos.x > WIDTH:
            self.pos.x = 0
            self.health =- 2
            
        if self.pos.x < 0:
            self.pos.x = WIDTH
            self.health =- 2
            
        if self.pos.y < 0:
            self.pos.y = HEIGHT
            self.health =- 2

        if self.pos.y > HEIGHT:
            self.pos.y = 0    
            self.health =- 2
        
class Box(pygame.sprite.Sprite):
    def __init__(self, color, x,y,width,height, text=''):
        super().__init__()
        self.surf = pygame.Surface((random.randint(15, 60),random.randint(10, 80)))
        self.surf.fill(boxColours[random.randint(0,6)])
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.pos = vec(x,y)
        self.speed = 6
        self.min_dist = 200
        self.lead_x_change = 0
        self.lead_y_change = 0
        self.lead_x = 10
        self.lead_y = 10

        self.rect = pygame.Rect(x,y, width, height)
        
   
    def boxFollowPlayer(self, player, boxList):
        if player.checkBoXCollision(boxList):
            player.hp +=1
        else:
            self.lead_x += self.lead_x_change
            self.lead_y += self.lead_y_change

            delta_x = player.pos.x - self.pos.x
            delta_y = player.pos.y - self.pos.y

            if abs(delta_x) <= self.min_dist and abs(delta_y) <= self.min_dist:
                enemy_move_x = abs(delta_x) > abs(delta_y)
                if abs(delta_x) > self.speed and abs(delta_x) > self.speed:
                    enemy_move_x = random.random() < 0.5
                if enemy_move_x:
                    self.x += min(delta_x, self.speed) if delta_x > 0 else max(delta_x, -self.speed)
                else:
                    self.y += min(delta_y, self.speed) if delta_y > 0 else max(delta_y, -self.speed)
    
    def boxBehaviour(self, player):
        if(self.rect.colliderect(player.rect)):
           #self.rect.update((30, 30), (200,200))
            pass
   

    

 

        
        
class GameCore():
    def __init__(self, player, surface):
        self.player = player
        self.surface = surface
        self.click = False
        self.mx, self.my = pygame.mouse.get_pos()
        self.move_speed = 5
        
      
        
    def draw_text(self, displaySurface,text, font, color, x,y):
        textobject = font.render(text, 1, color)
        textrectangle = textobject.get_rect()
        textrectangle.topleft = (x , y)
        displaySurface.blit(self.textobject, self.textrectangle)
        
    def defineGrid(self):
        blockSize = 80 #Set the size of the grid block
        for x in range(0, WIDTH, blockSize):
            for y in range(0, HEIGHT, blockSize):
                rect = pygame.Rect(x, y, blockSize, blockSize)
                pygame.draw.rect(self.surface, Color(63, 63, 63, 0), rect, 1)
                self.updateGrid(rect)
                
    
    def updateGrid(self, rect):
        rect.y += self.move_speed
    
    def returnRandom(self):
        return random.randint(150, 650) 
    
    def gameOver(self, player):
        if player.hp <= 0:
            self.main_menu(self.surface)
    
            
    def main_menu(self, displaySurface):
        
        while True:
            self.surface.fill((125,200,30))
            self.draw_text(self.surface, "Game Over", 200, WIDTH / 2, HEIGHT / 2)
            
            
            
            button_1 = pygame.Rect(50, 100, 200, 50)
            button_2 = pygame.Rect(50, 200, 200, 50)
            if button_1.collidepoint((self.mx, self.my)):
                if self.click:
                   pass
            if button_2.collidepoint((self.mx, self.my)):
                if self.click:
                    pass
            pygame.draw.rect(self.surface, (255, 0, 0), button_1)
            pygame.draw.rect(self.surface, (255, 0, 0), button_2)
    
            click = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
 
        pygame.display.update()
        mainClock.tick(60)
        
    def warning(self, displaSurface):
        pass
            
    def draw_text(self, Surface, text, size, x, y):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, (255,255,255))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        Surface.blit(text_surface, text_rect)
        
      
    
#creating objects  

play1 = Player("Dennis")

gameCore = GameCore(play1, displaysurface)



all_sprites = pygame.sprite.Group()
all_sprites.add(play1)

platforms = pygame.sprite.Group()


boxList = []
for randomObst in range(6):
    boxList.append(Box(boxColours[random.randint(0,6)],  random.randint(40,WIDTH),random.randint(80, HEIGHT), random.randint(20,80), random.randint(20,80))) 
    platforms.add(boxList)


while True:
    displaysurface.fill(BLUE) 
    gameCore.defineGrid()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit
            
   
        
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        
    for boxes in platforms:
        displaysurface.blit(boxes.surf, boxes.rect)
        boxes.boxFollowPlayer(play1, boxList)
        boxes.boxBehaviour(play1)
        
        
    font = pygame.font.SysFont(None, 24)
    img = font.render('hello', True, (255,255,255))
    gameCore.draw_text(displaysurface, "User: " + gameCore.player.name,30, 80, 10)
    gameCore.draw_text(displaysurface, "Score: " + str(gameCore.player.score), 40, WIDTH / 2, 10)
    gameCore.draw_text(displaysurface, "HP: " + str(gameCore.player.hp), 40, WIDTH -55, 10)

   #gameCore.gameOver(play1)
    play1.isAiming(boxList)
        
    play1.move()
    play1.checkBoXCollision(boxList)
    play1.createMouse(displaysurface, boxList)

    pygame.display.update()
    FramePerSec.tick(FPS)
        
            

    


