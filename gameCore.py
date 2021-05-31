import pygame
from pygame.locals import *
import sys
import random
 
pygame.init()
vec = pygame.math.Vector2 
 
HEIGHT = 860
WIDTH = 600
ACC = 0.85
FRIC = -0.1
FPS = 60
 
FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D")


class Player(pygame.sprite.Sprite):
   
   
    def __init__(self, info):
        super().__init__()
        self.surf = pygame.Surface((30,30))
        self.surf.fill((128,255,40))
        self.rect = self.surf.get_rect(center = (WIDTH/2,HEIGHT/2))
        self.name = info    
        self.hp = 100
        self.score = 0
        
        
        self.pos = vec((10,385))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
          
    def getName(self):
        return self.name
    
    def getScore(self):
        return self.score
    
    def setScore(self, score):
        self.score = score
        
        
    def move(self):
        self.acc = vec(0,0)
        
        pressed_keys = pygame.key.get_pressed()
        
        if pressed_keys[K_a]:
            self.acc.x = - ACC
        if pressed_keys[K_d]:
            self.acc.x =  ACC
        if pressed_keys[K_w]:
            self.acc.y = - ACC
        if pressed_keys[K_s]:
            self.acc.y = ACC
        if pressed_keys[K_SPACE]:
            self.ACC = 0
            self.FRIC = 0
     
        self.acc.x += self.vel.x * FRIC
        self.acc.y += self.vel.y * FRIC 
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        
    
    def createMouse(self, surface):     
        pygame.mouse.set_visible(False)
        pygame.draw.circle(surface, (0,0,0), pygame.mouse.get_pos(), 4)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.drawLine(surface)
        
        
    def drawLine(self, surface):
        pygame.draw.line(surface, (255,0,0), (self.pos.x, self.pos.y - 15),pygame.mouse.get_pos(), 2)
        
        
       
      
    def update(self):
        hits = pygame.sprite.spritecollide(play1 , platform, False)
        if hits:
            self.pos.y = hits[0].rect.top + 1
            self.vel.y = 0
        
    def collision(self):
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
        self.rect.midbottom = self.pos
        
  
        
class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((WIDTH, 20))
        self.surf.fill((0,0,0))
        self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))
 
 
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((20, 20))
        self.surf.fill((255,0,0))
        self.rect = self.surf.get_rect(center = (300 - 50,250))
        
        
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        
    def move(self):
        self.acc = vec(0,0.5)
        
    def setCenter(self,  x, y):
        self.rect = self.surf.get_rect(center = (x, y))
        
        
    

class GameCore():
    def __init__(self):
        self.player = play1
        self.score = score
    def printInfo(self):
        text = play1.getName  + "Score: " + score
    



        
platform = platform()
play1 = Player("Dennis")


obstacles = []



ob1 = Obstacle()
ob2 = Obstacle()
ob3 = Obstacle()

obstacles.append(ob1)
obstacles.append(ob2)
obstacles.append(ob3)

for obstacle in obstacles:
    obstacle.setCenter(random(10,500), random(100,600))


all_sprites = pygame.sprite.Group()
all_sprites.add(play1)
all_sprites.add(ob1)
all_sprites.add(ob2)
all_sprites.add(ob3)



        
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit
     
     
    displaysurface.fill((20,0,255))

    
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        
    play1.move()

    play1.collision()
    play1.createMouse(displaysurface)
    
    for obstacle in obstacles:
        obstacle.move()
        


 
    pygame.display.update()
    FramePerSec.tick(FPS)
        
        
            

            
        