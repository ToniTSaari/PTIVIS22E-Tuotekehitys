import pygame


class Game:
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode((800,600))
        self.screen.fill("pink")

        self.clock = pygame.time.Clock()
        self.framerate = 60

        self.gameover = False

        self.x = 200
        self.y = 200
        self.player = pygame.image.load('assets/art/player.png')

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

        if self.y > 0 and self.y < 800 and self.x > 0 and self.x < 600:
            if keys[pygame.K_w]:
                self.y = self.y - 1
                if self.y == 0:
                    self.y = 1
            if keys[pygame.K_s]:
                self.y = self.y + 1
                if self.y == 800:
                    self.y = 799
            if keys[pygame.K_d]:
                self.x = self.x + 1
                if self.x == 600:
                    self.x = 599
            if keys[pygame.K_a]:
                self.x = self.x - 1
                if self.x == 0:
                    self.x = 1                

    def update(self):
        pass

    def render(self):
        self.screen.fill("pink")
        self.screen.blit(self.player,(self.x,self.y))
        pygame.display.update()


# runs when executed as a script but not when imported
if __name__ == "__main__":
    game = Game()
    game.run()
