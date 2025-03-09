import pygame
from code.fishes.fish_abstract import AbstractFish
import random
from code.constants import *
from code.utils import convert_to_y

frames_count = 6

class GlobeFish(AbstractFish):
    def __init__(self, plongeur):
        super().__init__(plongeur)
        self.images = [pygame.image.load(f"images/globe_fish/frame_{i}_delay-0.2s.png") for i in range(frames_count)]
        self.dim = random.randint(30,60)
        self.images = [pygame.transform.scale(img, (self.dim* 500 / 434, self.dim )) for img in self.images]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.speed = self.calcul_speed()
        self.profondeur = random.randint(MIN_DEPTH_GLOBEFISH, MAX_DEPTH_GLOBEFISH)
        self.rect.y = convert_to_y(self.profondeur, plongeur)
        if self.left:
            self.rect.x = screen_width() + 200
            self.images = [pygame.transform.flip(img, True, False) for img in self.images]
        else:
            self.rect.x = - 200
        self.real_x = self.rect.x
        self.image = self.images[0]


    def calcul_speed(self):
        normalized_size = (self.dim - 30) / (60 - 30)
        return 0.3 + normalized_size * (2 - 0.3)
    
    def update(self):
        if self.left:
            self.real_x -= self.speed
        else:
            self.real_x += self.speed
        self.rect.x = round(self.real_x)
        self.rect.y = convert_to_y(self.profondeur, self.plongeur)
        if self.change_frame > FPS * 0.2:
            self.image = self.images[(self.index_image + 1) % frames_count]
            self.index_image += 1
            self.change_frame = 0
        self.change_frame += 1


        

