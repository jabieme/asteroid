import pygame
import sys
import time
from player import Player
from asteroid import Asteroid
from shot import Shot
from bomb import Bomb
from asteroidfield import AsteroidField
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from button import Button
from timer import Timer
from gamestate import GameState

page = "game"

pygame.init()
pygame.font.init()

my_font = pygame.font.SysFont("Comic Sans MS", 30)
text_surface = my_font.render('Game Over', False, "White")
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

restart = Button(
    center_position=((SCREEN_WIDTH/2), SCREEN_HEIGHT/2+100),
    font_size=30,
    bg_rgb=(0,0,0),
    text_rgb=(255,255,255),
    text="New Game",
    action= GameState.NEW_GAME
)
quit = Button(
    center_position=((SCREEN_WIDTH/2), SCREEN_HEIGHT/2+150),
    font_size=30,
    bg_rgb=(0,0,0),
    text_rgb=(255,255,255),
    text="Quit",
    action= GameState.QUIT
)
# timer = Timer(
#     center_position=(10,10),
#     font_size=24,
#     bg_rgb=(0,0,0),
#     text_rgb=(255,255,255),
#     text=str(pygame.time.get_ticks() //1000)
# )

def main():
    page = "end"
    
    while True:
        #timer.update(str(pygame.time.get_ticks() //1000))
        #timer.draw(screen)
        mouse_up=False
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:  
                    mouse_up = True
        
        if page == 'game':
            log_state()
            
            screen.fill("black")
            
            deltaTime = clock.tick(60) / 1000
            updatable.update(deltaTime)
            
            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    log_event("player_hit")
                    page = "end"
                for shot in shots:
                    if asteroid.collides_with(shot):
                        log_event("asteroid_shot")
                        asteroid.split()
                        shot.kill()
                        
                for bomb in bombs:
                    if bomb.hit(asteroid):
                        log_event("asteroid_shot")
                        asteroid.kill()
                        bomb.growth=True
                        bomb.velocity=pygame.Vector2(0,0)
                        
            for item in drawable:
                item.draw(screen)
            pygame.display.flip()
            
        elif page == 'end':
            screen.blit(text_surface,(SCREEN_WIDTH/2-75,SCREEN_HEIGHT/2))
            restart_action = restart.update(pygame.mouse.get_pos(), mouse_up)
            quit_action = quit.update(pygame.mouse.get_pos(),mouse_up)
            
            if restart_action == GameState.NEW_GAME:
                log_event("restart_game")
                page = "game"
            if quit_action == GameState.QUIT:
                log_event("game_ended")
                return
            restart.draw(screen)
            quit.draw(screen)
            pygame.display.flip()
            
if __name__ == "__main__":
    main()
