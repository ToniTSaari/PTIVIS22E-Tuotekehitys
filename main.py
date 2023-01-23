import pygame
from player import Player


class Game:
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode((800,600))
        self.screen.fill("pink")

        self.clock = pygame.time.Clock()
        self.framerate = 60

        self.gameover = False

        self.player = Player()

    def run(self):
        while not self.gameover:
            self.clock.tick(self.framerate)
            self.processInput()
            self.update()
            self.render()

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
                quit()

        keys = pygame.key.get_pressed()

        if self.player.rect.y > 0 \
        and self.player.rect.y < 800 \
        and self.player.rect.x > 0 \
        and self.player.rect.x < 600:
            if keys[pygame.K_w]:
                self.player.rect.y -= 1
                if self.player.rect.y == 0:
                    self.player.rect.y = 1
            if keys[pygame.K_s]:
                self.player.rect.y += 1
                if self.player.rect.y == 800:
                    self.player.rect.y = 799
            if keys[pygame.K_d]:
                self.player.rect.x += 1
                if self.player.rect.x == 600:
                    self.player.rect.x = 599
            if keys[pygame.K_a]:
                self.player.rect.x -= 1
                if self.player.rect.x == 0:
                    self.player.rect.x = 1                

    def update(self):
        pass

    def render(self):
        self.screen.fill("pink")
        self.screen.blit(self.player.sprite, self.player.rect)
        pygame.display.update()


# runs when executed as a script but not when imported
if __name__ == "__main__":
    game = Game()
    game.run()
