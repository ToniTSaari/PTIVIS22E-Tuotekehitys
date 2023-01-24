import pygame

from player import Player


class Game:
    def __init__(self) -> None:
        pygame.init()
        
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill("pink")

        self.clock = pygame.time.Clock()
        self.framerate = 60

        self.gameover = False

        self.player = Player()


    def run(self) -> None:
        while not self.gameover:
            self.clock.tick(self.framerate)
            self.process_input()
            self.update()
            self.render()


    def process_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
                quit()

        keys = pygame.key.get_pressed()

        self.player.speed.x = self.player.speed.y = 0

        if keys[pygame.K_w]:
            self.player.speed.y -= self.player.speed_multiplier
        if keys[pygame.K_s]:
            self.player.speed.y += self.player.speed_multiplier
        if keys[pygame.K_d]:
            self.player.speed.x += self.player.speed_multiplier
        if keys[pygame.K_a]:
            self.player.speed.x -= self.player.speed_multiplier


    def update(self) -> None:
        self.player.rect.move_ip(self.player.speed)
        
        if self.player.rect.top < 0:
            self.player.rect.top = 0
        if self.player.rect.bottom > self.height:
            self.player.rect.bottom = self.height
        if self.player.rect.right > self.width:
            self.player.rect.right = self.width
        if self.player.rect.left < 0:
            self.player.rect.left = 0


    def render(self) -> None:
        self.screen.fill("pink")
        self.screen.blit(self.player.sprite, self.player.rect)
        pygame.display.update()


# runs when executed as a script but not when imported
if __name__ == "__main__":
    game = Game()
    game.run()
