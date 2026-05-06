from enum import Enum
import pygame

class GameState(Enum):
    QUIT = -1
    MAIN_MENU = 0
    NEW_GAME = 1