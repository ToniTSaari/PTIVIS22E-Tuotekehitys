import pygame
import json
from pygame.locals import *

import keyboard_input
from player import Player

class Game:
    def __init__(self) -> None:
        pygame.init()

        with open('settings.json', 'r') as file:
            data = file.read()

        settings = json.loads(data)
        display = settings["display"]

        self.width = display["width"]
        self.height = display["height"]
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill("pink")

        self.clock = pygame.time.Clock()
        self.framerate = 60

        self.player = Player()


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

<<<<<<< HEAD
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
=======
    def process_keyboard_input(self) -> None:
        keys = pygame.key.get_pressed()
>>>>>>> c7d5343314c602aa31eebbbca261bcf1ddb7a2f4

        movement_direction = keyboard_input.movement_direction(keys)
        self.player.speed =  movement_direction * self.player.speed_multiplier


    def update(self) -> None:
        self.player.move(self.player.speed)
        self.keepBounds()
        
    def keepBounds(self) -> None:
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
        pygame.display.update()


# runs when executed as a script but not when imported
if __name__ == "__main__":
    game = Game()
    game.run()
