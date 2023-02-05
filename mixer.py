import pygame
import settings
from enum import Enum

class Mixer():

    def __init__(self) -> None:

        self.backgroundambient = Enum ("Ambient",['SWAMPMENU','BOSSFIGHT1'])
        self.sfx = Enum ("Sfx",["SHOOT,HIT"])

    def loadmusic(self,track) -> None:
        self.backgroundambient = track
        pygame.mixer.music.load(settings.ambientm[str(self.backgroundambient)])
        pygame.mixer.music.play(-1)
        pygame.mixer.music.pause()
    
    def playambient(self) -> None:
        pygame.mixer.music.unpause()

    def setambientvolume(self,floatlevel) -> None:
        pygame.mixer.music.set_volume(floatlevel)

    def playsfx(self,track) -> None:
        if pygame.mixer.find_channel() == None:
            pygame.mixer.set_num_channels(pygame.mixer.get_num_channels() + 1)
        
        self.sfx = track
        pygame.mixer.find_channel().play(pygame.mixer.Sound(settings.sfxm[str(self.sfx)]))