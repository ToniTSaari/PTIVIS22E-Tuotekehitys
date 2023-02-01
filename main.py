import pygame
from pygame.locals import *
import keyboard_input
from player import Player
from bullet import Bullet
from common import Vector2
from common import current_time
from common import last_shot
from common import bullet_cooldown

class Game:
    def __init__(self) -> None:
        pygame.init()

        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill("pink")

        self.clock = pygame.time.Clock()
        self.framerate = 60

        self.player = Player()
        self.bullet = Bullet(300, 300)

        self.bullet_group = pygame.sprite.Group()
        
        self.current_time = pygame.time.get_ticks()

        self.last_shot = pygame.time.get_ticks()

        self.bullet_cooldown = 0
        self.bullet_isready = True

    def run(self) -> None:
        while True:
            self.clock.tick(self.framerate)
            self.process_input()
            self.update()
            self.render()


    def process_input(self) -> None:
        self.process_events()
        self.process_keyboard_input()

    def process_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()


    def process_keyboard_input(self) -> None:

        keys = pygame.key.get_pressed()


        movement_direction = keyboard_input.movement_direction(keys)
        self.player.speed =  movement_direction * self.player.speed_multiplier

        if keys[pygame.K_SPACE] and self.bullet_isready == True:
            bullet_a = Bullet(self.player.position.x + 100, self.player.position.y + 70)
            self.bullet_group.add(bullet_a)
            self.bullet_isready = False
           
            

    def update(self) -> None:
        self.player.move(self.player.speed)
        self.clamp_player_to_screen()
        self.bullet_timer()

    def clamp_player_to_screen(self) -> None:
        if self.player.top < 0:
            self.player.top = 0
        if self.player.bottom > self.height:
            self.player.bottom = self.height
        if self.player.right > self.width:
            self.player.right = self.width
        if self.player.left < 0:
            self.player.left = 0

 
    def render(self) -> None: 
        self.screen.fill("pink")
        self.screen.blit(self.player.sprite, self.player.position)
        self.bullet_group.draw(self.screen)

        pygame.display.update()
        self.bullet_group.update()

    
    def bullet_timer(self) ->None:
        self.bullet_cooldown += 1

        if self.bullet_cooldown >= 15:
            self.bullet_cooldown = 0
            self.bullet_isready = True
        
  

# runs when executed as a script but not when imported
if __name__ == "__main__":
    game = Game()
    game.run()
