import pygame
from pygame.locals import *
import sys
import random

from pypy import Gun
 
pygame.init()
vec = pygame.math.Vector2 
mainClock = pygame.time.Clock()

 
HEIGHT = 800
WIDTH = 640
ACC = 0.85
FRIC = -0.2
FPS = 60

BLACK = ((0,0,0))
WHITE =((255,255,255))
RED = ((255,0,0))
GREEN = ((0,255,0))
BLUE = ((0,0,255))
YELLOW = ((255,255,0))
PINK = ((255,0,255))
SKYBLUE = ((0,255,255))
colours = [BLACK, WHITE, RED, GREEN, BLUE, YELLOW, PINK, SKYBLUE]


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
      
        
    
    def createMouse(self, surface):     
        pygame.mouse.set_visible(False)
        pygame.draw.circle(surface, (255,255,255), pygame.mouse.get_pos(), 4)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.drawLine(surface)
            self.score += 1
        
        
    def drawLine(self, surface):
        pygame.draw.line(surface, (255,255,255), (self.pos.x, self.pos.y - 15),pygame.mouse.get_pos(), 2)
        
    def checkBoXCollision(self, boxList):
        for boxes in boxList:
            if(self.rect.colliderect(boxes.rect)):
               self.hp -= 1
         
   

        
    def collision(self):
        self.rect.midbottom = self.pos
        if self.pos.x > WIDTH:
            self.pos.x = 0
            self.health =- 2
            
        if self.pos.x < 0:
            self.pos.x = WIDTH
            self.health =- 2
            
        if self.pos.y < 0:
            self.vel.y = 0
            self.health =- 2

        if self.pos.y > HEIGHT:
            self.vel.y = HEIGHT    
            self.health =- 2
        
class Box():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.pos = vec(x,y)

        self.rect = pygame.Rect(x,y, width, height)
        
   
        

    def draw(self,win,outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
      
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

 
class Game():
    def __init__(self, width, heigth):
        self.width = width
        self.heigth = heigth
        self.Main()
        
    def Main(self):
        print("Hej")
        
        
        
class GameCore():
    def __init__(self, player, surface):
        self.player = player
        self.surface = surface
        self.click = False
        self.mx, self.my = pygame.mouse.get_pos()
        
    def draw_text(self, displaySurface,text, font, color, x,y):
        textobject = font.render(text, 1, color)
        textrectangle = textobject.get_rect()
        textrectangle.topleft = (x , y)
        displaySurface.blit(self.textobject, self.textrectangle)
        
    
                
    def returnRandom(self):
        return random.randint(150, 650) 
    
    def gameOver(self, player):
        if player.hp <= 0:
            self.options()
            
    def options(self):
        while True:
            self.surface.fill((125,200,30))
            self.draw_text(self.surface, "Game Over", 200, WIDTH / 2, HEIGHT / 2)
            
            print("fis")
            
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
    boxList.append(Box(colours[random.randint(0,7)],  random.randint(40,WIDTH),random.randint(80, HEIGHT), random.randint(20,80), random.randint(20,80))) 

if __name__ == "__main__":
    Game(WIDTH, HEIGHT)
    
while True:
    displaysurface.fill((0,0,0)) 
      
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit
            
    for button in boxList:
        button.draw(displaysurface)
     
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        
        
    font = pygame.font.SysFont(None, 24)
    img = font.render('hello', True, (255,255,255))
    gameCore.draw_text(displaysurface, "User: " + gameCore.player.name,20, 40, 40)
    gameCore.draw_text(displaysurface, "Score: " + str(play1.score), 40, WIDTH / 2, 10)
    gameCore.gameOver(play1)
        
    play1.move()
    

   
    play1.createMouse(displaysurface)
    play1.checkBoXCollision(boxList)
  
    pygame.display.update()
    FramePerSec.tick(FPS)
        
        

    


