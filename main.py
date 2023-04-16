# standardise working directory because it can be inconsistent
import os
os.chdir(str(__file__[:-8]))


from math import sin, cos
import pygame
from pygame import sprite
from pygame.locals import *
import random

import canvas
from common import Vector2
import keyboard_input
from player import Player
from boss import Boss
from bullet import Bullet
from mixer import Mixer
import settings


class Game:
    def __init__(self) -> None:
        '''Create a game and set up the window, environment, etc.'''
        pygame.mixer.pre_init(44100,-16,4,1024)#Frequecy,size,channels,buffer
        pygame.init()
        settings.init()

        self.initialise_display()

        self.clock = pygame.time.Clock()
        self.framerate = 60

        # load the image used for the player's hearts
        # couldn't think of a more fitting place for this, feel free to move it
        self.heart_image = pygame.image.load("assets/art/heart.png")


    def initialise_display(self) -> None:
        self.width = settings.display["width"]
        self.height = settings.display["height"]
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("WoodHack: Root of Evil")

    def fullscreen_display(self) -> None:
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

    def change_display(self, wh) -> None:
        self.width = wh[0]
        self.height = wh[1]
        self.screen = pygame.display.set_mode((self.width, self.height))


    def start(self) -> None:
        '''Create any necessary game entities and start the game.'''
        # sprite groups for conveniently updating and rendering game entities
        self.all_sprites = sprite.LayeredUpdates()
        self.collider_group = sprite.LayeredUpdates() 
        self.enemy_group = sprite.LayeredUpdates()  # TODO NOT IN USE
        self.player_bullets = sprite.Group()
        self.enemy_bullets = sprite.Group()

        bg_woods = pygame.image.load("assets/art/bg/woods.jpg")

        self.boss = Boss(
            # place the boss in the middle of the arena
            Vector2(
                bg_woods.get_width()/2,
                bg_woods.get_height()/2
            ),
            (self.all_sprites, self.collider_group)
        )

        self.player = Player(
            # place the player a bit above the bottom centre of the arena
            Vector2(
                bg_woods.get_width()/2,
                bg_woods.get_height() * 3/4
            ),
            self.all_sprites
        )

        # draw everything on the canvas, then draw a part of it on the screen
        self.canvas = canvas.from_image(
            bg_woods,
            self.player
        )

        self.mixer = Mixer()

        game.main_menu()

    def main_menu(self) -> None:
        menu_bg_colour = "#202020"
        text_colour = "#202020"
        button_colour = "pink"
        start_highlight = "green"
        temp_highlight = "blue"
        quit_highlight = "red"

        self.set_button_layout()

        arial = pygame.font.Font(None, 100)

        self.mixer.loadmusic(0)
        self.mixer.playambient()

        while True:
            mouse_pos = pygame.mouse.get_pos()

            self.screen.fill(menu_bg_colour)

            start_text = arial.render("Start", True, text_colour)

            big_text = arial.render("1280:720", True, text_colour)
            small_text = arial.render("800:600", True, text_colour)

            quit_text = arial.render("Quit", True, text_colour)

            start_button_colour = \
                start_highlight if self.start_button.collidepoint(mouse_pos) \
                    else button_colour

            big_button_colour = \
                temp_highlight if self.big_button.collidepoint(mouse_pos) \
                    else button_colour
            
            small_button_colour = \
                temp_highlight if self.small_button.collidepoint(mouse_pos) \
                    else button_colour
            
            quit_button_colour = \
                quit_highlight if self.quit_button.collidepoint(mouse_pos) \
                    else button_colour

            pygame.draw.rect(
                self.screen,
                start_button_colour,
                self.start_button,
                border_radius=10
            )

            pygame.draw.rect(
                self.screen,

                big_button_colour,
                self.big_button,
                border_radius=10
            )

            pygame.draw.rect(
                self.screen,
                small_button_colour,
                self.small_button,
                border_radius=10
            )

            pygame.draw.rect(
                self.screen,

                quit_button_colour,
                self.quit_button,
                border_radius=10
            )

            self.screen.blit(
                start_text,
                Vector2(self.start_button.center) - start_text.get_rect().center
            )

            self.screen.blit(

                big_text,
                Vector2(self.big_button.center) - big_text.get_rect().center
            )

            self.screen.blit(
                small_text,
                Vector2(self.small_button.center) - small_text.get_rect().center
            )

            self.screen.blit(

                quit_text,
                Vector2(self.quit_button.center) - quit_text.get_rect().center
            )

            pygame.display.update()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if self.start_button.collidepoint(mouse_pos):
                        game.main_loop()

                    elif self.big_button.collidepoint(mouse_pos):
                        self.resoChange(720,1280)
                        self.set_button_layout()
                        
                    elif self.small_button.collidepoint(mouse_pos):
                        self.resoChange(600,800)
                        self.set_button_layout()

                    elif self.quit_button.collidepoint(mouse_pos):
                        exit()

    def set_button_layout(self):
        self.button_w = 320
        self.button_h = 100
        button_x = self.width/2 - self.button_w/2

        #jakamalla ruudun koko viidellä, saa suhdeluvun neljälle menunapille niin että ylä- ja alareunaan jää bufferialue
        y_ratio = self.height / 5
        s_button_y = y_ratio * 1
        small_button_y = y_ratio * 2
        big_button_y = y_ratio * 3
        q_button_y = y_ratio * 4

        self.start_button = Rect(
            button_x, s_button_y, self.button_w, self.button_h
        )
        self.small_button = Rect(
            button_x, small_button_y, self.button_w, self.button_h
        )
        self.big_button = Rect(
            button_x, big_button_y, self.button_w, self.button_h
        )
        self.quit_button = Rect(
            button_x, q_button_y, self.button_w, self.button_h
        )

    def resoChange(self, height, width):
        #asetetaan halutut resoluutiot .height ja .width muutujiin ja asetetaan resoluuto näiden muutujien mukaiseksi
        self.height = height
        self.width = width
        self.screen = pygame.display.set_mode((self.width, self.height))

        #haetaan display dict-muutujaan JSONista tiedot settings.all kautta
        display = settings.all["display"]

        #haetaan dict-muutujaan .height ja .width arvot
        display["height"] = self.height
        display["width"] = self.width

        #talletetaan muutokset JSON tiedostoon, "display" osioon ja lähetetään ne .write aliohjelmalle
        settings.all["display"] = display
        settings.write(settings.all)

    def main_loop(self) -> None:
        self.mixer.loadmusic(1)
        self.mixer.playambient()
        self.mixer.setambientvolume(0.5)
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
                exit()


    def process_keyboard_input(self) -> None:

        keys = pygame.key.get_pressed()


        movement_direction = keyboard_input.movement_direction(keys)
        self.player.speed =  movement_direction * self.player.speed_multiplier

        if keys[pygame.K_SPACE] and self.player.can_shoot():
            self.mixer.playsfx(0)

            # calculate where the mouse is on the canvas relative to the player
            # based on where it is relative to the centre of the screen
            display_centre_x = settings.display["width"] / 2
            display_centre_y = settings.display["height"] / 2
            display_centre = Vector2(display_centre_x, display_centre_y)

            mouse_pos = Vector2(pygame.mouse.get_pos())
            mouse_rel_to_centre = display_centre - mouse_pos
            mouse_rel_to_player = self.player.rect.center - mouse_rel_to_centre
            
            # shoot a bullet towards the point specified above
            #TODO: construct bullets from a direction, not a point
            Bullet(
                mouse_rel_to_player,
                self.player.rect.center,
                (self.player_bullets, self.all_sprites),
            )

            self.player.shot_cooldown = self.player.default_shot_cooldown


    def update(self) -> None:
        self.all_sprites.update()
        self.keep_player_in_bounds()

        self.boss_attack()

        self.check_bullet_hits(self.boss, self.player_bullets)
        self.check_bullet_hits(self.player, self.enemy_bullets)

        self.check_game_over()

    def boss_attack(self) -> None:
        if self.boss.can_shoot():
            bullets_per_shot = 13
            shot_angle = 360 / bullets_per_shot
            starting_angle = random.uniform(0, shot_angle)
            base_vector = Vector2(cos(starting_angle), sin(starting_angle))
            vectors = [
                base_vector.rotate(shot_angle * i) + self.boss.rect.center
                for i in range(bullets_per_shot)
            ]
            for v in vectors:
                Bullet(
                    v,
                    self.boss.rect.center,
                    (self.enemy_bullets, self.all_sprites),
                )

           
    def check_bullet_hits(
        self,
        target: sprite.Sprite,
        bullet_group: sprite.AbstractGroup
    ) -> None:
        '''
        Check if any bullets in `bullet_group` hit `target`.
        
        The target takes 1 damage for every bullet that hits it
        (must have a method called `take_damage()` that receives an int)
        and any bullets that hit the target are removed.
        '''
        if sprite.spritecollideany(
            target,
            bullet_group
        ):
            for _ in sprite.spritecollide(
                target,
                bullet_group,
                True,
                sprite.collide_mask
            ):
                target.take_damage(1)

    def check_game_over(self) -> None:
        if self.boss.hp == 0:
            self.game_over_win()
        elif self.player.hp == 0:
            self.game_over_lose()


    def game_over_win(self) -> None:
        self.screen.fill("green")
        self.screen.blit(*(self.make_end_text("VICTORY")))
        pygame.display.update()
        self.press_any_button_to_quit()
    
    def game_over_lose(self) -> None:
        self.screen.fill("red")
        self.screen.blit(*(self.make_end_text("DEFEAT")))
        pygame.display.update()
        self.press_any_button_to_quit()
    
    
    def make_end_text(self, text: str):
        font = pygame.font.Font(None, 350)
        text_colour = "#202020"
        text_image = font.render(text, True, text_colour)
        text_rect = text_image.get_rect()
        text_rect.center = self.screen.get_rect().center

        return (text_image, text_rect.topleft)

    def press_any_button_to_quit(self) -> None:
        pygame.mixer.music.pause()
        pygame.time.wait(2000) # wait 2 seconds to avoid accidents
        pygame.event.get() # clear the event queue for the same reason
        while True:
            for event in pygame.event.get():
                if event.type in [QUIT, MOUSEBUTTONDOWN, KEYDOWN]:
                    exit()


    def keep_player_in_bounds(self) -> None:
        if self.player.top < 0:
            self.player.top = 0
        if self.player.bottom > self.canvas.inner.get_height():
            self.player.bottom = self.canvas.inner.get_height()
        if self.player.right > self.canvas.inner.get_width():
            self.player.right = self.canvas.inner.get_width()
        if self.player.left < 0:
            self.player.left = 0


    def render(self) -> None:
        self.screen.fill("#202020")

        self.canvas.draw(self.all_sprites)
        self.screen.blit(self.canvas.inner, (0,0), self.canvas.camera_view())

        self.draw_hud()

        pygame.display.update()

    def draw_hud(self) -> None:
        self.draw_player_health()
        self.draw_boss_health()

    def draw_player_health(self) -> None:
        # margins for the entire player health bar from the edges of the window
        top_margin = 30
        left_margin = 30

        heart_width = self.heart_image.get_width()
        # empty space between hearts
        hearts_offset = 10

        # show a heart for each point of hp the player has
        for i in range(self.player.hp):
            x_offset = i * (hearts_offset + heart_width) + left_margin
            self.screen.blit(self.heart_image, (x_offset, top_margin))


    def draw_boss_health(self) -> None:
        # 2 bars: one for the actual health display, another for its background
        bar_colour = "#202020"
        inner_bar_colour = "red"

        bottom_margin = 30
        bar_width = int(settings.display["width"] / 3)
        bar_height = 14
        bar_padding = 2

        inner_bar_height = bar_height - 2 * bar_padding
        inner_bar_max_width = bar_width - 2 * bar_padding
        inner_bar_width = inner_bar_max_width * self.boss.hp / self.boss.max_hp
        
        bar_x = (settings.display["width"] - bar_width) / 2
        bar_y = settings.display["height"] - bottom_margin - bar_height
        inner_bar_x = bar_x + bar_padding
        inner_bar_y = bar_y + bar_padding

        pygame.draw.rect(
            self.screen,
            bar_colour,
            (bar_x, bar_y, bar_width, bar_height)
        )

        pygame.draw.rect(
            self.screen,
            inner_bar_colour,
            (inner_bar_x, inner_bar_y, inner_bar_width, inner_bar_height)
        )


# runs when executed as a script but not when imported
if __name__ == "__main__":
    game = Game()
    game.start()
