import pygame
from code.fishes.fish_abstract import AbstractFish
import random
from code.constants import *
from code.utils import convert_to_y

frames_count = 4

class Fish(AbstractFish):
    def __init__(self, plongeur):
        super().__init__(plongeur)
        self.images = [pygame.image.load(f"images/fish/frame_{i}_delay-0.1s.png") for i in range(frames_count)]
        self.dim = random.randint(30,100)
        self.images = [pygame.transform.scale(img, (self.dim, self.dim)) for img in self.images]
        self.image = self.images[0]
        self.left = True
        self.rect = self.image.get_rect()
        self.speed = self.calcul_speed()
        self.profondeur = random.randint(MIN_DEPTH_FISH, MAX_DEPTH_FISH)
        self.rect.y = convert_to_y(self.profondeur, plongeur)
        if self.left:
            self.rect.x = screen_width() + 200
            self.images = [pygame.transform.flip(img, True, False) for img in self.images]
        else:
            self.rect.x = - 200
        self.real_x = self.rect.x
        self.image = self.images[0]


    def calcul_speed(self):
        normalized_size = (self.dim - 30) / (100 - 30)
        return 0.3 + normalized_size * (5 - 0.3)
    
    def update(self):
        if self.left:
            self.real_x -= self.speed
        else:
            self.real_x += self.speed
        self.rect.x = round(self.real_x)
        self.rect.y = convert_to_y(self.profondeur, self.plongeur)
        if self.change_frame > FPS * 0.1:
            self.image = self.images[(self.index_image + 1) % frames_count]
            self.index_image += 1
            self.change_frame = 0
        self.change_frame += 1


        

