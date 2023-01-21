# Importaa pygame ja math
import pygame
import math

def init():
    #intialize some specific modules in pygame/ not needed
    pygame.init()
    #set static screensize for pygame
    screen = pygame.display.set_mode((800,600))
    screen.fill("pink")

def run():
    init()
    gameover = False

    while gameover != True:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit
                quit()
        pygame.display.update()
run()

