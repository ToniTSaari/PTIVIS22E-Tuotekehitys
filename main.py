import pygame
vec2 = pygame.math.Vector2


class Game:
    def __init__(self):
        pygame.init()
        #set static screensize for pygame
        self.screen = pygame.display.set_mode((800,600))
        self.screen.fill("pink")
        self.gameover = False
        self.clock = pygame.time.Clock()
        self.framerate = 60
        self.pos = vec2(200, 200)

        self.player=pygame.image.load('player.png')

    def run(self):
        while not self.gameover:
            self.clock.tick(self.framerate)
            self.processInput()
            self.update()
            self.render()

    def processInput(self):
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit
                quit()


        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.pos.y -= 10
        if keys[pygame.K_s]:
            self.pos.y += 10
        if keys[pygame.K_d]:
            self.pos.x += 10
        if keys[pygame.K_a]:
            self.pos.x -= 10

    def update(self):
        pass

    def render(self):
        self.screen.blit(self.player, self.pos)
        pygame.display.update()


# runs when executed as a script but not when imported
if __name__ == "__main__":
    game = Game()
    game.run()
