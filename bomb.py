from circleshape import CircleShape
import pygame
from constants import *

class Bomb(CircleShape):
    def __init__(self, x,y):
        super().__init__(x,y,BOMB_RADIUS)
        self.bomb = None
    
    def blast_radius(self):
        self.velocity=pygame.Vector2(0,0)
        growth = pygame.Vector2(1,1)
        while self.radius < 100:
            self.radius
        self.kill()
        
    def draw(self, screen):
        self.bomb = pygame.draw.circle(screen, "white", self.position, int(self.radius), LINE_WIDTH)
        return self.bomb
    def grow(self):
        self.radius+=BOMB_INCREASE_SPEED
    
    def update(self, dt):
        self.position += self.velocity * dt