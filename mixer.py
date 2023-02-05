import pygame
import settings
from enum import Enum

class Mixer():

    def __init__(self) -> None:

        self.backgroundambient = Enum ("Ambient",['SWAMPMENU','BOSSFIGHT1'])

    def loadmusic(self,track) -> None:
        self.backgroundambient = track
        pygame.mixer.music.load(settings.ambientm[str(self.backgroundambient)])
        pygame.mixer.music.play(-1)
        pygame.mixer.music.pause()
    
    def playambient(self) -> None:
        pygame.mixer.music.unpause()