import pygame
import sys
from player import Player
from asteroid import Asteroid
from shot import Shot
from bomb import Bomb
from asteroidfield import AsteroidField
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    clock = pygame.time.Clock()
    deltaTime = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    bombs = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, drawable, updatable)
    Bomb.containers = (bombs, drawable, updatable)

    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    asteroidField = AsteroidField()

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")

        deltaTime = clock.tick(60) / 1000
        
        updatable.update(deltaTime)
        
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game Over!")
                sys.exit(1)
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    asteroid.split()
                    
            for bomb in bombs:
                if bomb.collides_with(asteroid):
                    log_event("asteroid_shot")
                    asteroid.kill()
                    bomb.velocity=pygame.Vector2(0,0)
                    bomb.grow()
                    
        for item in drawable:
            item.draw(screen)

        pygame.display.flip()
        
        print(deltaTime)

if __name__ == "__main__":
    main()
