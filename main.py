import pygame
import json
from pygame.locals import *

import keyboard_input
from player import Player
from object import Object

class Game:
    def __init__(self) -> None:
        pygame.init()

        with open('settings.json', 'r') as file:
            data = file.read()

        self.gamelooprunning = None

        settings = json.loads(data)
        display = settings["display"]

        self.width = display["width"]
        self.height = display["height"]
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill("pink")

        # contain all sprites enemies walls player ect for updates layering
        self.spritegroup = pygame.sprite.LayeredUpdates()
        self.collidergroup = pygame.sprite.LayeredUpdates() 
        self.enemygroup = pygame.sprite.LayeredUpdates()  # TODO NOT IN USE

        self.clock = pygame.time.Clock()
        self.framerate = 60

        self.object = Object()
        self.player = Player()

        self.playercollider = pygame.sprite.GroupSingle(self.player)

    def new(self)-> None:

        pygame.sprite.Sprite.__init__(self.player, self.spritegroup)
        pygame.sprite.Sprite.__init__(self.object, self.spritegroup)
        # TODO ALL OBJECTS ITERATE TO SPRITE GROUP AND OTHER GROUPS LATER
        pygame.sprite.Sprite.__init__(self.object, self.collidergroup)

        game.run()

    def run(self) -> None:
        self.gamelooprunning = True
        while self.gamelooprunning:
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

        if self.player.speed.x != 0 and self.player.speed.y != 0:
            # suhde taitaa olla 1.41.. hypotenuusan ja kannan välillä 45 asteessa, ei toimi ykkösellä hajoaa niin pienistä nopeuksista.
            self.player.speed.scale_to_length(2.82)
            for sprite in self.spritegroup:
                sprite.rect.x -= round(self.player.speed.x)
                sprite.rect.y -= round(self.player.speed.y)
            self.player.rect.x += round(self.player.speed.x)
            self.player.rect.y += round(self.player.speed.y)
        else:
            for sprite in self.spritegroup:
                sprite.rect.x -= round(self.player.speed.x*2)
                sprite.rect.y -= round(self.player.speed.y*2)
            self.player.rect.x += round(self.player.speed.x*2)
            self.player.rect.y += round(self.player.speed.y*2)


    def update(self) -> None:
        self.spritegroup.update()
        #self.playergroup.update()  # Basically resets speed back to 0
        #self.clamp_player_to_screen()
        
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
        #self.screen.fill("pink")

        #collision
        if pygame.sprite.spritecollide(self.playercollider.sprite,self.collidergroup,False):
            if pygame.sprite.spritecollide(self.playercollider.sprite,self.collidergroup,False,pygame.sprite.collide_mask):
                self.screen.fill("red")
            else:
                self.screen.fill("pink")
        else: self.screen.fill("pink")


        self.player.setmovestate(self.player.angle)
        self.spritegroup.draw(self.screen)  # Draw all sprites


        pygame.display.update()


# runs when executed as a script but not when imported
if __name__ == "__main__":
    game = Game()
    game.new()
