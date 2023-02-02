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

    def main_menu(self) -> None:
        menu_bg_colour = "#202020"
        text_colour = "#202020"
        button_colour = "pink"
        start_highlight = "green"
        quit_highlight = "red"

        button_w = 250
        button_h = 100
        button_x = self.width/2 - button_w/2

        s_button_y = (self.height - button_h) / 4
        q_button_y = self.height - (s_button_y + button_h)

        start_button = Rect(button_x, s_button_y, button_w, button_h)
        quit_button = Rect(button_x, q_button_y, button_w, button_h)

        arial = pygame.font.Font(None, 100)

        while self.mmenurunning:
            mouse_pos = pygame.mouse.get_pos()

            self.screen.fill(menu_bg_colour)

            start_text = arial.render("Start", True, text_colour)
            quit_text = arial.render("Quit", True, text_colour)

            start_button_colour = \
                start_highlight if start_button.collidepoint(mouse_pos) \
                    else button_colour

            quit_button_colour = \
                quit_highlight if quit_button.collidepoint(mouse_pos) \
                    else button_colour

            pygame.draw.rect(
                self.screen,
                start_button_colour,
                start_button,
                border_radius=10
            )

            pygame.draw.rect(
                self.screen,
                quit_button_colour,
                quit_button,
                border_radius=10
            )

            self.screen.blit(
                start_text,
                Vector2(start_button.center) - start_text.get_rect().center
            )

            self.screen.blit(
                quit_text,
                Vector2(quit_button.center) - quit_text.get_rect().center
            )

            pygame.display.update()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.collidepoint(mouse_pos):
                        self.mmenurunning = False
                        game.run()
                    elif quit_button.collidepoint(mouse_pos):
                        return


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
    #game.run()
