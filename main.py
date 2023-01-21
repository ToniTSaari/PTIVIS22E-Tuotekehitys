import pygame
import math


class Game:
    def __init__(self):
        pygame.init()
        #set static screensize for pygame
        self.screen = pygame.display.set_mode((800,600))
        self.screen.fill("pink")
        self.gameover = False
        self.clock = pygame.time.Clock()
        self.framerate = 60

    def run(self):
        while not self.gameover:
            self.clock.tick(self.framerate)
            self.processInput()
            self.update()
            self.render()

    def processInput(self):
        for events in pygame.event.get():
            keys = pygame.key.get_pressed()
            if events.type == pygame.QUIT:
                pygame.quit
                quit()

            if keys[pygame.K_w]:
                print("UP")
            if keys[pygame.K_s]:
                print("Down")
            if keys[pygame.K_d]:
                print("Right")
            if keys[pygame.K_a]:
                print("Left")

    def update(self):
        pass

    def render(self):
        pygame.display.update()


# runs when executed as a script but not when imported
if __name__ == "__main__":
    game = Game()
    game.run()
