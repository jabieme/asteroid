import pygame 
from circleshape import CircleShape
from shot import Shot
from bomb import Bomb
import constants

class Player(CircleShape):
    def __init__(self, x, y ):
        super().__init__(x, y, constants.PLAYER_RADIUS)
        self.__rotation = 0
        self.__shot_cooldown = 0
        self.__bomb_cooldown = 0 

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.__rotation)
        right = pygame.Vector2(0,1).rotate(self.__rotation + 90) * self.radius
        a = self.position+forward*self.radius
        b = self.position-forward*self.radius-right
        c = self.position-forward*self.radius+right
        return [a,b,c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), constants.LINE_WIDTH)

    def move(self, dt):
        unit_vector = pygame.Vector2(0,1)
        rotated_vector = unit_vector.rotate(self.__rotation)
        rotated_with_speed_vector = rotated_vector * constants.PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self):
        shot = Shot(self.position[0], self.position[1])
        shot.velocity = pygame.Vector2(0,1).rotate(self.__rotation) * constants.PLAYER_SHOOT_SPEED

    def bomb(self):
        bomb = Bomb(self.position[0], self.position[1])
        bomb.velocity = pygame.Vector2(0,1).rotate(self.__rotation)*constants.PLAYER_SHOOT_SPEED

    def rotate(self, dt):
        self.__rotation += constants.PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.__shot_cooldown -= dt
        self.__bomb_cooldown -= dt
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_SPACE]:
            while self.__shot_cooldown <= 0:
                self.shoot()
                self.__shot_cooldown = constants.PLAYER_SHOOT_COOLDOWN_SECONDS
        if keys[pygame.K_b]:
            while self.__bomb_cooldown <= 0:
                self.bomb()
                self.__bomb_cooldown= constants.PLAYER_BOMB_COOLDOWN_SECONDS
