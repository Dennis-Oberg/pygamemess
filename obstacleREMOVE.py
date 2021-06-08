import pygame
from pygame.locals import *

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
        
        
for i in range(10):
    obstacles.append(Obstacle())
    obstacles[i].setCenter((i+7 ) * random.randint(10,20), 100 * random.randint(0,5))
    
    all_sprites.add(obstacles)
  for obstacle in obstacles:
        obstacle.move(play1)
            play1.checkCollision(obstacles)
        
        