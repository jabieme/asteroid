import pygame
from circleshape import CircleShape
from logger import log_event
from constants import *
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            log_event("asteroid_split")
            angle = random.uniform(20, 50)
            split_velocity_1 = self.velocity.rotate(angle)
            split_velocity_2 = self.velocity.rotate(-angle)
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            asteroid1 = Asteroid(self.position[0], self.position[1], new_radius)
            asteroid2 = Asteroid(self.position[0], self.position[1], new_radius)
            asteroid1.velocity = split_velocity_1*ASTEROID_SPLIT_SPEED
            asteroid2.velocity = split_velocity_2*ASTEROID_SPLIT_SPEED

        
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)
    
    def update(self, dt):
        self.position += self.velocity * dt
