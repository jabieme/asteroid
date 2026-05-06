from circleshape import CircleShape
import pygame
from constants import *

class Bomb(CircleShape):
    def __init__(self, x,y):
        super().__init__(x,y,BOMB_RADIUS)
        self.bomb = None
        self.collision = None
        self.growth = False

    def hit(self, other):
        self.collision = self.collides_with(other)
        return self.collision
        
    def draw(self, screen):
        self.bomb = pygame.draw.circle(screen, "orange", self.position, int(self.radius), LINE_WIDTH)
        return self.bomb
    def grow(self):
        self.radius+=BOMB_INCREASE_SPEED
    
    def update(self, dt):
        self.position += self.velocity * dt
        if self.radius <= 110:
            if self.growth:
                self.grow()
        else:
            self.kill()
        