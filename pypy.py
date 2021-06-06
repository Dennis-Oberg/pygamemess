import pygame
from pygame.locals import *

class Gun():
    def __init__(self, x, y, width):
        self.pos = ((x,y))
        
        print("hej")        
        
    def createGun(self, surface):
        pygame.draw.circle(surface, (255,255,255), self.x, self.y, self.width)
        
        
        