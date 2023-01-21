# Importaa pygame ja math
import pygame
import math

#intialize pygame
pygame.init()
gameover = False
#set static screensize for pygame
screen = pygame.display.set_mode((800,600))
screen.fill("pink")

#poistetaan toi while true ei varmaan oo paras
#joku listener ?
while gameover != True:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            pygame.quit
            quit()
    pygame.display.update()