import pygame
from code.Fishes.FishAbstract import AbstractFish
import random
from code.constants import *
from code.utils import convert_to_y

fish_image = pygame.image.load('images/fish.png')
fish_image = pygame.transform.scale(fish_image, (100, 100))
fish_image = pygame.transform.rotate(fish_image, -20)

class FishUnanimated(AbstractFish):
    def __init__(self, plongeur):
        super().__init__(plongeur)
        self.image = fish_image
        self.dim = random.randint(50,150)
        self.image = pygame.transform.scale(self.image, (self.dim, self.dim))
        self.rect = self.image.get_rect()
        self.speed = self.dim // 50 + 1
        self.profondeur = random.randint(MIN_DEPTH_FISH, MAX_DEPTH_FISH)
        self.rect.y = convert_to_y(self.profondeur, plongeur)
        if self.left:
            self.rect.x = screen_width() + 200
        else:
            self.image  = pygame.transform.flip(self.image, True, False)
            self.rect.x = - 200
        
    def update(self):
        if self.left:
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
        self.rect.y = convert_to_y(self.profondeur, self.plongeur)


        

