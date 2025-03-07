import pygame
import random
import math
from code.constants import *
import os
from code.utils import * 

frames_count = 8
class Dashboard:
    def __init__(self, screen, plongeur, mod):
        self.screen = screen
        self.mod = mod
        self.plongeur = plongeur
        self.font = pygame.font.Font("Font/04B_03__.TTF", 20)        
        self.ocean_images = [pygame.image.load(f"images/ocean.png") for i in range(frames_count)]
        self.ocean_images = [pygame.transform.scale(img, (screen_width(), screen_height() * HEIGHT_POSITION + 25)) for img in self.ocean_images]
        self.ocean_image = self.ocean_images[0]
        self.index_image = 0
        self.change_frame = 0
        self.ocean_anchor = convert_to_depth(0, plongeur)
        self.image_fore1, self.image_fore2, self.image_far, self.image_sand, self.hauteur_image_background = self.init_background()
        self.far_init_y = screen_height() - 0.2 * self.hauteur_image_background
        self.sand_init_y = screen_height()
        self.fore_init_y = 1.3 * screen_height()
        self.max_back = screen_height() - self.hauteur_image_background


    def init_background(self):
        image_far = pygame.image.load("images/Background/far.png").convert_alpha()
        image_sand = pygame.image.load("images/Background/sand.png").convert_alpha()
        image_fore1 = pygame.image.load("images/Background/foreground-1.png").convert_alpha()
        image_fore2 = pygame.image.load("images/Background/foreground-2.png").convert_alpha()
        rect = image_sand.get_rect()
        hauteur_image = rect.height #192
        largeur_image = rect.width #256
        new_hauteur = hauteur_image * screen_width() / (3 * largeur_image)

        image_far = pygame.transform.scale(image_far, (screen_width() / 3, new_hauteur))
        image_sand = pygame.transform.scale(image_sand, (screen_width() / 3, new_hauteur))

        image_fore1 = pygame.transform.scale(image_fore1, (screen_width() / 3, new_hauteur))
        image_fore2 = pygame.transform.scale(image_fore2, (screen_width() / 3, new_hauteur))

        return image_fore1, image_fore2, image_far, image_sand, new_hauteur

    def y_far(self):
        return min(self.plongeur.profondeur / MAX_DEPTH_PARRALAX, 1) * (self.max_back - self.far_init_y) + self.far_init_y
    
    def draw_far(self):
        y = min(self.plongeur.profondeur / MAX_DEPTH_PARRALAX, 1) * (self.max_back - self.far_init_y) + self.far_init_y
        for i in range(3):
            self.screen.blit(self.image_far, (screen_width() * i / 3, y))
    
    def draw_sand(self):
        y = min(self.plongeur.profondeur / MAX_DEPTH_PARRALAX, 1) * (self.max_back - self.sand_init_y) + self.sand_init_y
        for i in range(3):
            self.screen.blit(self.image_sand, (screen_width() * i / 3, y))
        
    def draw_foreground(self):
        y = min(self.plongeur.profondeur / MAX_DEPTH_PARRALAX, 1) * (self.max_back - self.fore_init_y) + self.fore_init_y
        self.screen.blit(self.image_fore1, (0, y))
        self.screen.blit(self.image_fore2, (screen_width() / 3, y))
        self.screen.blit(self.image_fore1, (2 * screen_width() / 3, y))

    def warning(self):
        if self.change_frame < FPS:
            if self.plongeur.air < 50: #Oxygen issue
                red_color = (255, 0, 0, 128) 
                border_thickness = 5
                frame_surface = pygame.Surface((screen_width(), screen_height()), pygame.SRCALPHA)
                pygame.draw.rect(frame_surface, red_color, (0, 0, screen_width(), border_thickness))  # Haut
                pygame.draw.rect(frame_surface, red_color, (0, 0, border_thickness, screen_height()))  # Gauche
                pygame.draw.rect(frame_surface, red_color, (0, screen_height() - border_thickness, screen_width(), border_thickness))  # Bas
                pygame.draw.rect(frame_surface, red_color, (screen_width() - border_thickness, 0, border_thickness, screen_height()))  # Droite
                self.screen.blit(frame_surface, (0, 0))

            elif self.plongeur.energie < 7: #Energy issue
                border_thickness = 5
                frame_surface = pygame.Surface((screen_width(), screen_height()), pygame.SRCALPHA)
                pygame.draw.rect(frame_surface, YELLOW, (0, 0, screen_width(), border_thickness))  # Haut
                pygame.draw.rect(frame_surface, YELLOW, (0, 0, border_thickness, screen_height()))  # Gauche
                pygame.draw.rect(frame_surface, YELLOW, (0, screen_height() - border_thickness, screen_width(), border_thickness))  # Bas
                pygame.draw.rect(frame_surface, YELLOW, (screen_width() - border_thickness, 0, border_thickness, screen_height()))  # Droite
                self.screen.blit(frame_surface, (0, 0))

        if self.change_frame > 2*FPS:
            self.change_frame = 0
        self.change_frame += 1



    def update(self):
        pass
        

    def draw_background(self):
        anchor_y = convert_to_y(self.ocean_anchor, self.plongeur)
        debut = anchor_y + screen_height() * HEIGHT_POSITION + 25
        fin = self.y_far()
        ecart = fin - debut
        for y in range(max(0,int(debut)), int(fin)):
            color = (
                OCEAN_IMAGE_COLOR[0] + (WATER_BOTTOM_COLOR[0] - OCEAN_IMAGE_COLOR[0]) * (y-debut) / ecart,
                OCEAN_IMAGE_COLOR[1] + (WATER_BOTTOM_COLOR[1] - OCEAN_IMAGE_COLOR[1]) * (y-debut) / ecart,
                OCEAN_IMAGE_COLOR[2] + (WATER_BOTTOM_COLOR[2] - OCEAN_IMAGE_COLOR[2]) * (y-debut) / ecart
            )

            pygame.draw.line(self.screen, color, (0, y), (screen_width(), y))
        self.screen.blit(self.ocean_image, (0,  anchor_y))

        self.draw_far()
        self.draw_sand()


    def draw_info(self):
        pygame.draw.rect(self.screen, (100, 100, 100), (10, 10, 202, 352), 2)
        pygame.draw.rect(self.screen, (200,200,200), (12, 12, 198, 348))

        if self.mod == "Play":
            # pygame.draw.rect(self.screen, BLACK, (100, 100, 20, 204), 2)
            # pygame.draw.rect(self.screen, YELLOW, (102, 302 - self.plongeur.energie * 200/30, 16, self.plongeur.energie * 200/30))
            self.draw_text("Energy bar", (50, 180))
            if self.plongeur.energie == 0:
                pygame.draw.rect(self.screen, RED , (20, 210, 180, 20), 2)
            else:
                pygame.draw.rect(self.screen, BLACK, (20, 210, 180, 20), 2)
            pygame.draw.rect(self.screen, YELLOW, (22, 212, self.plongeur.energie * 176/30, 16))
            with open("records/record_play.txt", "r") as fichier:
                record = float(fichier.read())
            self.draw_text("Record: {} m".format(record), (20,20))
            self.draw_text("Speed: {} m/s".format(round(self.plongeur.vitesse, 1)), (20, 80))
            self.draw_text("Depth: {} m".format(round(self.plongeur.profondeur, 1)), (20, 120))


        else:
            with open("records/record_explore.txt", "r") as fichier:
                record = float(fichier.read())
            self.draw_text("Record: {} m".format(record), (20,20))
            self.draw_text("Speed: {} m/s".format(round(self.plongeur.vitesse, 1)), (20, 60))
            self.draw_text("Depth: {} m".format(round(self.plongeur.profondeur, 1)), (20, 100))


            self.draw_text("Oxygen bar", (50, 150))
            if self.plongeur.air <= 1 :
                pygame.draw.rect(self.screen, RED, (20, 180, 180, 20), 2)
            else:
                pygame.draw.rect(self.screen, BLACK, (20, 180, 180, 20), 2)
            pygame.draw.rect(self.screen, BLUE, (22, 182, self.plongeur.air * 176/200, 16))

            #Energy bar
            # pygame.draw.rect(self.screen, BLACK, (130, 100, 20, 204), 2)
            # pygame.draw.rect(self.screen, YELLOW, (132, 302 - self.plongeur.energie * 200/30, 16, self.plongeur.energie * 200/30))
            self.draw_text("Energy bar", (50, 220))
            if self.plongeur.energie == 0:
                pygame.draw.rect(self.screen, RED, (20, 250, 180, 20), 2)
            else:
                pygame.draw.rect(self.screen, BLACK, (20, 250, 180, 20), 2)
            pygame.draw.rect(self.screen, YELLOW, (22, 252, self.plongeur.energie * 176/30, 16))

        self.draw_text("Enter = Palm", (20, 310))
        self.draw_text("Space = Turn ", (20, 330))


        depth_interval = 10  # Intervalle de profondeur à dessiner
        for depth in range(0, 200, depth_interval):
            y_depth = convert_to_y(depth, self.plongeur)
            self.draw_text(f"{depth} meters", (screen_width() * 14 / 16, y_depth + 15))
            pygame.draw.line(self.screen, BLACK, (screen_width() * 7 / 8 , y_depth), (screen_width(), y_depth))

    def draw_time(self, time):
        if self.mod=="Play":
            self.draw_text(f"Time : {round(time,1)} sec", (20, 260))
        if self.mod =="Explore":
            self.draw_text(f"Time : {round(time,1)} sec", (20, 280))

    def draw_text(self, text, position):
        text_surface = self.font.render(text, True, BLACK)  # Utiliser du texte noir pour une meilleure lisibilité
        self.screen.blit(text_surface, position)
