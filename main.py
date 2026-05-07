import pygame
import sys
import time
from objects.player import Player
from objects.asteroid import Asteroid
from objects.shot import Shot
from objects.bomb import Bomb
from objects.asteroidfield import AsteroidField
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from objects.logger import log_state, log_event
from objects.button import Button
from objects.gamestate import GameState

page = "game"

pygame.init()
pygame.font.init()

my_font = pygame.font.SysFont("Comic Sans MS", 30)
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
    center_position=((SCREEN_WIDTH/2), SCREEN_HEIGHT/2+150),
    font_size=30,
    bg_rgb=(0,0,0),
    text_rgb=(255,255,255),
    text="New Game",
    action= GameState.NEW_GAME
)
quit = Button(
    center_position=((SCREEN_WIDTH/2), SCREEN_HEIGHT/2+185),
    font_size=30,
    bg_rgb=(0,0,0),
    text_rgb=(255,255,255),
    text="Quit",
    action= GameState.QUIT
)
start = Button(
    center_position=((SCREEN_WIDTH/2), SCREEN_HEIGHT/2+150),
    font_size=30,
    bg_rgb=(0,0,0),
    text_rgb=(255,255,255),
    text="Start",
    action= GameState.START
)

def main():
    """
        Main Game loop with starting, playing, and ending logic
    """
    page = "start"
    score = 0
    time = 0 
    pause = 0
    
    
    while True:
        screen.fill("black")
        drawable.clear(screen, pygame.Rect(0,0,SCREEN_WIDTH,SCREEN_HEIGHT))
        updatable.clear(screen, pygame.Rect(0,0,SCREEN_WIDTH,SCREEN_HEIGHT))
        
        mouse_up=False
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:  
                    mouse_up = True
                    
        if page == "start":
            start_message = my_font.render("Welcome to Asteroid", True,(255,255,255))
            screen.blit(start_message,(SCREEN_WIDTH/2-start_message.get_size()[0]//2,SCREEN_HEIGHT/2))
            start.draw(screen)
            start_action = start.update(pygame.mouse.get_pos(),mouse_up)
            if start_action == GameState.START:
                page = 'game'

        if page == 'game':
            text_score = my_font.render(str(score),True,(255,255,255))
            time = pygame.time.get_ticks()//1000-pause
            screen.blit(my_font.render(str(time),True, (255,255,255)), (10,10))
            screen.blit(text_score, (SCREEN_WIDTH-text_score.get_size()[0]-10, 10))
            
            log_state()
            
            deltaTime = clock.tick(60) / 1000
            updatable.update(deltaTime)

            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    log_event("player_hit")            
                    page = "end"
                    pause += time

                for shot in shots:
                    if asteroid.collides_with(shot):
                        log_event("asteroid_shot")
                        asteroid.split()
                        shot.kill()
                        score+=1
                        
                for bomb in bombs:
                    if bomb.hit(asteroid):
                        log_event("asteroid_shot")
                        asteroid.kill()
                        bomb.growth=True
                        score+=1
                        bomb.velocity=pygame.Vector2(0,0)
                for item in drawable:
                    item.draw(screen)
            
            
        if page == 'end':
            game_over = my_font.render('Game Over', True, "White")
            player_score = my_font.render(f'Score: {score}', True, "White")
            screen.blit(game_over,(SCREEN_WIDTH/2-game_over.get_size()[0]//2,SCREEN_HEIGHT/2))
            screen.blit(player_score, (SCREEN_WIDTH/2-player_score.get_size()[0]//2,SCREEN_HEIGHT/2+35))

            restart.draw(screen)
            quit.draw(screen)

            restart_action = restart.update(pygame.mouse.get_pos(), mouse_up)
            quit_action = quit.update(pygame.mouse.get_pos(),mouse_up)

            if restart_action == GameState.NEW_GAME:
                log_event("restart_game")
                for asteroid in asteroids:
                    asteroid.kill()
                score = 0
                page = "game"
                time = 0
                
            if quit_action == GameState.QUIT:
                log_event("game_ended")
                return
            
        pygame.display.flip()
            
if __name__ == "__main__":
    main()
