import pygame
import random
from code.constants import *
from math import log1p
FPS = 60

frames_count = 5

class Bubbles(pygame.sprite.Sprite):
    def __init__(self, screen, bubbles_behind, bubbles_infront):
        super().__init__()
        self.image = pygame.image.load(f"images/background/bubble.png")
        self.dim = random.randint(20,150)
        self.image = pygame.transform.scale(self.image, (self.dim, self.dim))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width())
        self.rect.y = screen_height() + 10
        self.finished = False
        self.speed = self.dim // 30 + 1
        if self.dim > 100:
            self.infront = True
        else:
            self.infront = False


    def update(self):
        self.rect.y -= self.speed
        self.image = pygame.transform.scale(self.image, (self.dim, self.dim))
        if self.rect.y < - self.dim:
            self.finished = True

   