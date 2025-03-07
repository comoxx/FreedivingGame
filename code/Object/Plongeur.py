import pygame
from code.constants import *
from code.utils import convert_to_depth, convert_to_y
frames_count = 7


class Plongeur(pygame.sprite.Sprite):
    def __init__(self, mod):
        super().__init__()
        self.mod = mod
        self.index_image = 0
        self.change_frame = 0
        self.plongeur_images = [pygame.image.load(f"images/diver/frame_{i}_delay-0.1s.png") for i in range(frames_count)]
        self.plongeur_images = [pygame.transform.rotate(i, -100) for i in self.plongeur_images]
        self.image = self.plongeur_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width() // 2, screen_height() * HEIGHT_POSITION)
        self.vitesse = 0
        self.profondeur = 0
        self.descente = True
        self.start = False
        self.total_time = 0
        self.sous_eau = True  
        self.profondeur_max = 0  
        self.energie = 30
        self.air = 200
        self.last_palming = 1000 #time in frames
        self.space_time = 0 


    def archimede(self):
        density = WEIGHT / (INCOMPRESSIBLE_VOLUME + LUNGS_VOLUME/(1 + self.profondeur/10)) * 1000
        force = (density - WATER_DENSITY) *  INCOMPRESSIBLE_VOLUME / 1000 * G 
        return force

    def friction(self):
        if self.vitesse > 0 :
            return - WATER_DENSITY/100 * self.vitesse**2
        return WATER_DENSITY /100 * self.vitesse**2
    
    def palm(self):
        if self.energie > 0 :
            if self.descente:
                return PALM_FORCE
            return -PALM_FORCE
        return 0
    
    def speed_calcul(self):
        if not self.start:
            return 0
        if self.last_palming == 0:
            if self.mod == "Explore":
                self.air -= 1
            total_forces = self.archimede() + self.friction() + self.palm()
        else:
            total_forces = self.archimede() + self.friction()
        return total_forces / (WEIGHT * FPS)


    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN] and self.last_palming > FPS /2 and self.energie>0: #We can palm every 0.5 seconds
            # if self.profondeur == 0:
            #     self.profondeur = 0.1
            self.start = True
            self.last_palming = 0
            self.energie -= 1
        if keys[pygame.K_SPACE] and self.space_time > FPS / 2 and self.start:
            self.descente = not self.descente
            self.vitesse = 0
            self.space_time = 0
            self.plongeur_images = [pygame.transform.rotate(i, 180) for i in self.plongeur_images] 
            self.image = self.plongeur_images[self.index_image % frames_count]

        # if self.sous_eau:
        if self.last_palming < FPS and self.change_frame > FPS * 0.1:
            self.image = self.plongeur_images[(self.index_image + 1) % frames_count]
            self.index_image += 1
            self.change_frame = 0
        if self.last_palming == FPS:
            self.image = self.plongeur_images[2]
            self.index_image = 2
        if self.mod == "Explore" and self.profondeur > 0:
            self.air -= 0.05
        self.vitesse += self.speed_calcul()
        self.profondeur = max(0, self.profondeur + self.vitesse / FPS)
        if self.profondeur > self.profondeur_max:
            self.profondeur_max = self.profondeur
        # else:
        #     self.vitesse = 0
        
        if self.profondeur <= 0:
            self.sous_eau = False
        
        if self.profondeur >= MAX_DEPTH:
            self.profondeur = MAX_DEPTH
            self.vitesse = 0
        if self.profondeur > MAX_DEPTH_PARRALAX:
            self.rect.center = (screen_width() // 2, convert_to_y(self.profondeur, self))

        if self.start:
            self.total_time += 1
        self.space_time += 1
        self.last_palming += 1 
        self.change_frame += 1            

