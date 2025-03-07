from abc import ABC, abstractmethod
import pygame
import random
from code.constants import *

class AbstractFish(pygame.sprite.Sprite):
    def __init__(self, plongeur):
        super().__init__()
        self.plongeur = plongeur
        self.left = random.choice([True, False])
        self.index_image = 0
        self.change_frame = 0


    @abstractmethod
    def update(self):
        pass

