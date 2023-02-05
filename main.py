import pygame
from pygame.locals import *

from common import Vector2
import keyboard_input
from player import Player
from boss import Boss
from bullet import Bullet
from common import Vector2
import keyboard_input
from player import Player
from mixer import Mixer
import settings
import pygame_menu


class Game:
    def __init__(self) -> None:
        '''Create a game and set up the window, environment, etc.'''
        pygame.mixer.pre_init(44100,16,4,1024)#Frequecy,size,channels,buffer
        pygame.init()
        settings.init()

        self.initialise_display()

        self.clock = pygame.time.Clock()
        self.framerate = 60


    def initialise_display(self) -> None:
        self.width = settings.display["width"]
        self.height = settings.display["height"]
        self.screen = pygame.display.set_mode((self.width, self.height))


    def start(self) -> None:
        '''Create any necessary game entities and start the game.'''
        # sprite groups for conveniently updating and rendering game entities
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.collider_group = pygame.sprite.LayeredUpdates() 
        self.enemy_group = pygame.sprite.LayeredUpdates()  # TODO NOT IN USE
        self.bullet_group = pygame.sprite.Group()

        self.boss = Boss(
            Vector2(self.width/2, 144),
            (self.all_sprites, self.collider_group)
        )

        self.player = Player(
            Vector2(self.screen.get_rect().center),
            self.all_sprites
        )

        self.mixer = Mixer()

        
        # set up shooting cooldown tracking
        self.bullet_cooldown = 0
        self.bullet_isready = True

        game.main_menu1()

    def main_menu1(self) -> None:
        menu = pygame_menu.Menu('Menu', settings.display["width"], settings.display["height"], theme=pygame_menu.themes.THEME_BLUE)
        menu.add.button('Play', game.main_loop)
        menu.add.button('Quit', pygame_menu.events.EXIT)
        menu.mainloop(self.screen)

    def main_menu2(self) -> None:
        menu_bg_colour = "#202020"
        text_colour = "#202020"
        button_colour = "pink"
        start_highlight = "green"
        temp_highlight = "blue"
        quit_highlight = "red"

        button_w = 250
        button_h = 100
        button_x = self.width/2 - button_w/2

        s_button_y = (self.height - button_h) / 4
        q_button_y = self.height - (s_button_y + button_h)
        t_button_y = self.height - (((s_button_y + q_button_y) / 2) + button_h)

        start_button = Rect(button_x, s_button_y, button_w, button_h)
        temp_button = Rect(button_x, t_button_y, button_w, button_h)
        quit_button = Rect(button_x, q_button_y, button_w, button_h)

        arial = pygame.font.Font(None, 100)

        self.mixer.loadmusic(0)
        self.mixer.playambient()

        while True:
            mouse_pos = pygame.mouse.get_pos()

            self.screen.fill(menu_bg_colour)

            start_text = arial.render("Start", True, text_colour)
            temp_text = arial.render("temp", True, text_colour)
            quit_text = arial.render("Quit", True, text_colour)

            start_button_colour = \
                start_highlight if start_button.collidepoint(mouse_pos) \
                    else button_colour

            temp_button_colour = \
                temp_highlight if temp_button.collidepoint(mouse_pos) \
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
                temp_button_colour,
                temp_button,
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
                temp_text,
                Vector2(temp_button.center) - temp_text.get_rect().center
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
                        game.main_loop()
                    elif temp_button.collidepoint(mouse_pos):
                        self.height = 600
                        self.width = 800
                        self.screen = pygame.display.set_mode((self.width, self.height))
                        game.main_loop()
                    elif quit_button.collidepoint(mouse_pos):
                        return

    def main_loop(self) -> None:
        self.mixer.loadmusic(1)
        self.mixer.playambient()
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

        if keys[pygame.K_SPACE] and self.bullet_isready:
            Bullet(
                (self.player.rect.midright),
                (self.bullet_group, self.all_sprites)
            )
            self.bullet_isready = False


    def update(self) -> None:
        self.all_sprites.update()
        self.bullet_timer()
           
            

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
        # visualise collision by changing the background colour
        if pygame.sprite.spritecollide( # check rough collision by sprite rects
            self.player,
            self.collider_group,
            False
        ) \
        and pygame.sprite.spritecollide( # pixel-perfect check if rects collide
            self.player,
            self.collider_group,
            False,
            pygame.sprite.collide_mask
        ):
            self.screen.fill("red")
        else:
            self.screen.fill("pink")


        self.player.setmovestate(self.player.angle)
        self.all_sprites.draw(self.screen)
        self.bullet_group.draw(self.screen)

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
