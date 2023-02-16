from math import sin, cos
import pygame
from pygame import sprite
from pygame.locals import *
import random

from common import Vector2
import os
os.chdir(str(__file__[:-8]))
import canvas
from boss import Boss
from bullet import Bullet
from mixer import Mixer
from player import Player
import keyboard_input
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


    def initialise_display(self) -> None:
        self.width = settings.display["width"]
        self.height = settings.display["height"]
        self.screen = pygame.display.set_mode((self.width, self.height))

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

        self.boss = Boss(
            Vector2(self.width/2, 144),
            (self.all_sprites, self.collider_group)
        )

        self.player = Player(
            Vector2(self.screen.get_rect().center),
            self.all_sprites
        )

        # draw everything on the canvas, then draw a part of it on the screen
        self.canvas = canvas.from_image(
            pygame.image.load("assets/art/bg/woods.jpg"),
            self.player
        )

        self.mixer = Mixer()

        self.bullet_cooldown = 0
        self.bullet_isready = True

        game.main_menu()

    def main_menu(self) -> None:
        menu_bg_colour = "#202020"
        text_colour = "#202020"
        button_colour = "pink"
        start_highlight = "green"
        temp_highlight = "blue"
        quit_highlight = "red"

        button_w = 320
        button_h = 100
        button_x = self.width/2 - button_w/2

        #jakamalla ruudun koko viidellä, saa suhdeluvun neljälle menunapille niin että ylä- ja alareunaan jää bufferialue
        y_ratio = self.height / 5
        s_button_y = y_ratio * 1
        small_button_y = y_ratio * 2
        big_button_y = y_ratio * 3
        q_button_y = y_ratio * 4

        start_button = Rect(button_x, s_button_y, button_w, button_h)
        small_button = Rect(button_x, small_button_y, button_w, button_h)
        big_button = Rect(button_x, big_button_y, button_w, button_h)
        quit_button = Rect(button_x, q_button_y, button_w, button_h)

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
                start_highlight if start_button.collidepoint(mouse_pos) \
                    else button_colour

            big_button_colour = \
                temp_highlight if big_button.collidepoint(mouse_pos) \
                    else button_colour
            
            small_button_colour = \
                temp_highlight if small_button.collidepoint(mouse_pos) \
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

                big_button_colour,
                big_button,
                border_radius=10
            )

            pygame.draw.rect(
                self.screen,
                small_button_colour,
                small_button,
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

                big_text,
                Vector2(big_button.center) - big_text.get_rect().center
            )

            self.screen.blit(
                small_text,
                Vector2(small_button.center) - small_text.get_rect().center
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
                    def resoChange(height, width):
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

                    if start_button.collidepoint(mouse_pos):
                        game.main_loop()

                    elif big_button.collidepoint(mouse_pos):
                        resoChange(720,1280)
                        game.main_menu()
                    elif small_button.collidepoint(mouse_pos):
                        resoChange(600,800)
                        game.main_menu()

                    elif quit_button.collidepoint(mouse_pos):
                        pygame.quit()

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
                pygame.quit()
                quit()


    def process_keyboard_input(self) -> None:

        keys = pygame.key.get_pressed()


        movement_direction = keyboard_input.movement_direction(keys)
        self.player.speed =  movement_direction * self.player.speed_multiplier


        if self.player.speed.x != 0 and self.player.speed.y != 0:
            # suhde taitaa olla 1.41.. hypotenuusan ja kannan välillä 45 asteessa,
            # ei toimi ykkösellä hajoaa niin pienistä nopeuksista.
            self.player.speed.scale_to_length(2.82)
            for sprite in self.all_sprites:
                sprite.rect.x -= round(self.player.speed.x)
                sprite.rect.y -= round(self.player.speed.y)
            self.player.rect.x += round(self.player.speed.x)
            self.player.rect.y += round(self.player.speed.y)
        else:
            for sprite in self.all_sprites:
                sprite.rect.x -= round(self.player.speed.x*2)
                sprite.rect.y -= round(self.player.speed.y*2)
            self.player.rect.x += round(self.player.speed.x*2)
            self.player.rect.y += round(self.player.speed.y*2)

        if keys[pygame.K_SPACE] and self.player.can_shoot():
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouseposvec=Vector2(mouse_x,mouse_y)
            self.mixer.playsfx(0)
            Bullet(
                mouseposvec,
                self.player.rect.center,
                (self.player_bullets, self.all_sprites),
            )


    def update(self) -> None:
        self.all_sprites.update()

        self.check_bullet_hits(self.boss, self.player_bullets)
        self.check_bullet_hits(self.player, self.enemy_bullets)
        self.check_game_over()
        self.bullet_timer()


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
                    quit()

    def keep_bounds(self) -> None:
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

        self.player.setmovestate(self.player.angle)
        self.all_sprites.draw(self.screen)
        self.player_bullets.draw(self.screen)

        self.canvas.draw(self.all_sprites)
        self.screen.blit(self.canvas.inner, (0,0), self.canvas.camera_view())


        pygame.display.update()
        
    def bullet_timer(self) -> None:
        self.bullet_cooldown += 1

        if self.bullet_cooldown >= 15:
            self.bullet_cooldown = 0
            self.bullet_isready = True


# runs when executed as a script but not when imported
if __name__ == "__main__":
    game = Game()
    game.start()
