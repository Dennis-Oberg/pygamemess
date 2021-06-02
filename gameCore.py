import pygame
from pygame.locals import *
import sys
import random
 
pygame.init()
vec = pygame.math.Vector2 
 
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
        
        
        self.pos = vec((10,385))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        
    def setScore(self, score):
        self.score = score
        
        
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
        
    
    def createMouse(self, surface):     
        pygame.mouse.set_visible(False)
        pygame.draw.circle(surface, (255,255,255), pygame.mouse.get_pos(), 4)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.drawLine(surface)
            self.score += 1
        
        
    def drawLine(self, surface):
        pygame.draw.line(surface, (255,255,255), (self.pos.x, self.pos.y - 15),pygame.mouse.get_pos(), 2)
        
    def checkCollision(self, obstacles):
        obstaclePoints = []
        for obst in obstacles:
            obstaclePoints.append(obst.pos.x)
            

        
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
        
class Button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

 
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((20, 20))
        self.surf.fill((random.random(),0,0))
        self.rect = self.surf.get_rect(center = (300 - 50,250))
        self.pos = vec((0,0))
        self.surf.fill((255,255,255))
    
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        
    def move(self, player):
        self.acc = vec(0,0.5)
        if(player.isMoving):
            self.acc.x =- ACC
            
        self.acc.x += self.vel.x * FRIC
        self.acc.y += self.vel.y * FRIC 
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
    
    def returnPos(self):
        return self.pos
            
        
    def setCenter(self,  x, y):
        self.rect = self.surf.get_rect(center = (x, y))
        
        
        
        
class GameCore():
    def __init__(self, player, surface, ):
        self.player = player
        self.surface = surface
    
    
            
    
    def draw_text(self, Surface, text, size, x, y):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, (255,255,255))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        Surface.blit(text_surface, text_rect)
    
#creating objects  

play1 = Player("Dennis")

gameCore = GameCore(play1, displaysurface)


obstacles = []

for i in range(10):
    obstacles.append(Obstacle())
    obstacles[i].setCenter((i+7 ) * random.randint(10,20), 100 * random.randint(0,5))


all_sprites = pygame.sprite.Group()
all_sprites.add(play1)

all_sprites.add(obstacles)
platforms = pygame.sprite.Group()


buttonList = []
mainButton = Button(RED, WIDTH/2, HEIGHT/2, 200,50, "Welcome") 
buttonList.append(mainButton)
    
while True:
    displaysurface.fill((0,0,0)) 
      
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit
     
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        
        
    font = pygame.font.SysFont(None, 24)
    img = font.render('hello', True, (255,255,255))
    gameCore.draw_text(displaysurface, "User: " + gameCore.player.name,20, 40, 40)
    gameCore.draw_text(displaysurface, "Score: " + str(play1.score), 40, WIDTH / 2, 10)
        
    play1.move()

    play1.collision()
    play1.checkCollision(obstacles)
    play1.createMouse(displaysurface)
    
    for obstacle in obstacles:
        obstacle.move(play1)
    
  
    for button in buttonList:
        button.draw(displaysurface)
   
 
    pygame.display.update()
    FramePerSec.tick(FPS)
        
        

    

            
        