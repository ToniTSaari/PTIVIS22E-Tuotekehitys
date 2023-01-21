# Importaa pygame ja math
import pygame
import math

def init():
    #intialize some specific modules in pygame/ not needed
    pygame.init()
    #set static screensize for pygame
    screen = pygame.display.set_mode((800,600))
    screen.fill("pink")

#short explanation for __name__==__main__
#It Allows You to Execute Code When the File Runs as a Script,
# but Not When It’s Imported as a Module
if __name__ == "__main__":
    init()
    gameover = False

    while gameover != True:
        for events in pygame.event.get():
            keys = pygame.key.get_pressed()
            if events.type == pygame.QUIT:
                pygame.quit
                quit()

            if keys[pygame.K_w]:
                print("UP")
            if keys[pygame.K_a]:
                print("Down")
            if keys[pygame.K_d]:
                print("Right")
            if keys[pygame.K_a]:
                print("Left")
        
        
        pygame.display.update()
#run()

