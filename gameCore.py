import pygame
from pygame.locals import *
import sys
import random
 
pygame.init()
vec = pygame.math.Vector2 
 
HEIGHT = 800
WIDTH = 640
ACC = 0.85
FRIC = -0.1
FPS = 60
 
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
        self.name = "Dennis"
        self.isMoving = False
        self.playerMouseX, playerMouseY = pygame.mouse.get_pos()
        
        
        self.pos = vec((10,385))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.particles = []
          
   
    def setScore(self, score):
        self.score = score
        
    def createParticles(self):
        self.particles.append([[200,200 ], [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 6)])
        for particle in self.particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.1
            particle[1][1] += 0.1
            pygame.draw.circle(displaysurface, (255, 255, 255), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
            if particle[2] <= 0:
                self.particles.remove(particle)
        
        
    def move(self):
        self.acc = vec(0,0)
        
        pressed_keys = pygame.key.get_pressed()
        
        if pressed_keys[K_a]:
            self.acc.x = - ACC
            isMoving = True
        if pressed_keys[K_d]:
            self.acc.x =  ACC
            isMoving = True
        if pressed_keys[K_w]:
            self.acc.y = - ACC
            isMoving = True
        if pressed_keys[K_s]:
            self.acc.y = ACC
            isMoving = True
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
            self.createParticles()
            self.score += 1
        
        
    def drawLine(self, surface):
        pygame.draw.line(surface, (255,0,0), (self.pos.x, self.pos.y - 15),pygame.mouse.get_pos(), 2)
        
    def checkCollision(self, obstacles):
        obstaclePoints = []
        for obst in obstacles:
            obstaclePoints.append(obst.pos.x)
            

        
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
        
  
        

 
 
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((20, 20))
        self.surf.fill((random.random(),0,0))
        self.rect = self.surf.get_rect(center = (300 - 50,250))
        self.pos = vec((0,0))
    
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        
    def move(self, player):
        self.acc = vec(0,0.5)
        if(player.isMoving):
            self.acc.x =-5
            
        
    def setCenter(self,  x, y):
        self.rect = self.surf.get_rect(center = (x, y))
        
        
        
class GameCore():
    def __init__(self, Player, Surface):
        self.Player = Player
        self.Surface = Surface
    
    def scrolling(self, obstacles):
        pass
    
    
    def draw_text(self, Surface, text, size, x, y):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, (0,0,0))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        Surface.blit(text_surface, text_rect)
    
#creating objects  

play1 = Player("Dennis")

gameCore = GameCore(play1, displaysurface)


obstacles = []





for i in range(10):
    obstacles.append(Obstacle())
    obstacles[i].setCenter(100 * random.randint(0,8), 100 * random.randint(0,5))


all_sprites = pygame.sprite.Group()
all_sprites.add(play1)

all_sprites.add(obstacles)
platforms = pygame.sprite.Group()



    


        
while True:
    
    displaysurface.fill((20,0,255))
  
    
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
    gameCore.draw_text(displaysurface, "Score " + str(play1.score), 40, WIDTH / 2, 10)
        
    play1.move()

    play1.collision()
    play1.checkCollision(obstacles)
    play1.createMouse(displaysurface)
    
    gameCore.scrolling(obstacles)
    
    for obstacle in obstacles:
        obstacle.move(play1)
       
 
    pygame.display.update()
    FramePerSec.tick(FPS)
        
        


            
        