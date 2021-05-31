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

font3 = pygame.font.SysFont('Bauhaus 93', 36)

class Player(pygame.sprite.Sprite):
   
   
    def __init__(self, info):
        super().__init__()
        self.surf = pygame.Surface((30,30))
        self.surf.fill((128,255,40))
        self.rect = self.surf.get_rect(center = (10,420))
        self.name = info    
        
        
        self.pos = vec((10,385))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
          
    def getName(self):
        return self.name
        
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
        pygame.draw.circle(surface, (0,125,255), pygame.mouse.get_pos(), 10)
       
      
    def update(self):
        hits = pygame.sprite.spritecollide(play1 , platform, False)
        if hits:
            self.pos.y = hits[0].rect.top + 1
            self.vel.y = 0
        
    def collision(self):
        if self.pos.x > WIDTH:
            self.pos.x = 0
            
        if self.pos.x < 0:
            self.pos.x = WIDTH
            
        if self.pos.y < 0:
            self.vel.y = 0
            

        if self.pos.y > HEIGHT:
            self.vel.y = HEIGHT    
     
        self.rect.midbottom = self.pos
        
  
        
class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((WIDTH, 20))
        self.surf.fill((255,0,0))
        self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))
 
 
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((30, 20))
        self.surf.fill((255,0,0))
        self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))
        



        
platform = platform()
play1 = Player("Dennis")


obstacles = list()
for i in range (10):
    obstacles.append(Obstacle())


print(obstacles)    


all_sprites = pygame.sprite.Group()
all_sprites.add(platform)
all_sprites.add(play1)



text = font3.render('Hello world', True, (0, 0, 0))


        
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit
     
    displaysurface.fill((0,0,0))
    displaysurface.blit(text, (100,100))

    
        
    
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        
    play1.move()

    play1.collision()
    play1.createMouse(displaysurface)
    
    
 
    pygame.display.update()
    FramePerSec.tick(FPS)
        
        
            

            
        