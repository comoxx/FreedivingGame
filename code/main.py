import pygame
import sys
import os
from code.constants import *
from code.dashboard import Dashboard
from code.objects.plongeur import Plongeur
from code.fishes.fish import Fish
import random
from code.fishes.big_fish import BigFish
from code.fishes.dart_fish import DartFish
from code.fishes.globe_fish import GlobeFish
from code.begginning_screen import beginning, square_breath, countdown, menu, selection, credits
from code.fishes.shark import Shark



def init():
    pygame.init()
    screen_info = pygame.display.Info()
    screen = pygame.display.set_mode((screen_width(), screen_height()), pygame.FULLSCREEN)
    pygame.display.set_caption("FreeDiving")
    pygame.mixer.music.load("sounds/watery_cave_loop.ogg")
    pygame.mixer.music.play(-1)
    return screen


def draw_text(surface, text, font, color, x=None, y=None):
    """Fonction pour dessiner du texte sur une surface"""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if x==None:
        text_rect.centerx = surface.get_width() // 2
    else:
        text_rect.centerx = x 
    if y==None:
        text_rect.centery = surface.get_height() // 2
    else:
        text_rect.centery = y 
    surface.blit(text_surface, text_rect)

def run_game(screen):
    Diver = pygame.sprite.Group()
    mod = selection(screen)
    if mod =="Credits":
        info = credits(screen)
        if info=="SELECTION":
            return "Play"
        if info =="QUIT":
            sys.exit()
    if mod == "Play":
        info = beginning(screen, mod)
        if info == "QUIT":
            sys.exit()
        info = square_breath(screen)
        if info == "QUIT":
            sys.exit()
        info = countdown(screen)
        if info == "QUIT":
            sys.exit()
        plongeur = Plongeur("Play")
    if mod == "Explore":
        info = beginning(screen, mod)
        if info == "QUIT":
            sys.exit()
        plongeur = Plongeur("Explore")
    if mod == "QUIT":
        sys.exit()

    running = True
    Diver.add(plongeur)
    fish_infront = pygame.sprite.Group()
    fish_behind = pygame.sprite.Group()
    dashboard = Dashboard(screen, plongeur, mod)
    while running:
    # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    sys.exit()

        # Mise à jour
        dashboard.update()
        Diver.update()
        fish_behind.update()
        fish_infront.update()
        if random.random() < PROBA_FISH:
            fish = Fish(plongeur)
            if fish.dim < 70:
                fish_behind.add(fish)
            else:
                fish_infront.add(fish)
            
        if random.random() < PROBA_SHARK:
            shark = Shark(plongeur)
            if shark.dim < 120:
                fish_behind.add(shark)
            else:
                fish_infront.add(shark)

        if random.random() < PROBA_GLOBEFISH:
            fish = GlobeFish(plongeur)
            if fish.dim < 50:
                fish_behind.add(fish)
            else:
                fish_infront.add(fish)

        if random.random() < PROBA_BIGFISH:
            big_fish = BigFish(plongeur)
            if big_fish.dim < 60:
                fish_behind.add(big_fish)
            else:
                fish_infront.add(big_fish)

        if random.random() < PROBA_DARTFISH:
            dart_fish = DartFish(plongeur)
            if dart_fish.dim < 70:
                fish_behind.add(dart_fish)
            else:
                fish_infront.add(dart_fish)

        if (plongeur.start and plongeur.air <= 0) or (plongeur.energie == 0 and plongeur.vitesse > 0.3):
            play_again = False
            font = pygame.font.Font("font/04B_03__.TTF", 30)
            #Dim : 48 * 16 pixels
            button_image1 = pygame.image.load("images/button/[1] Normal.png").convert_alpha()
            button_image2 = pygame.image.load("images/button/[2] Clicked.png").convert_alpha()
            button_image1 = pygame.transform.scale(button_image1, (screen_width() // 6, screen_width() // 6 * 16 /48))
            button_image2 = pygame.transform.scale(button_image2, (screen_width() // 6, screen_width() // 6 * 16 /48))
            button_rect_play = button_image1.get_rect()
            button_rect_play.center = (3*screen_width() // 8, 5*screen_height()//8)
            button_rect_quit = button_image1.get_rect()
            button_rect_quit.center = (5 * screen_width() // 8, 5*screen_height()//8)
            color_title = (20,20,110)
            while not play_again:
                dashboard.draw_background()
                fish_behind.draw(screen)
                dashboard.draw_foreground()
                Diver.draw(screen)
                fish_infront.draw(screen)
                dashboard.draw_info()
                dashboard.draw_time(plongeur.total_time / FPS)
                if plongeur.air <= 0:
                    afficher_message(screen, "Oops... You drowned. You ran out of air", screen_width()//2, 2 * screen_height() // 5)
                else:
                    afficher_message(screen, "Oops... You drowned.", screen_width()//2, 3 * screen_height() // 10)
                    afficher_message(screen, "Not enough energy to get back to the surface", screen_width()//2, 2 * screen_height() // 5)
                afficher_message(screen, "Luckily, the safety divers were there to save you!", screen_width()//2, screen_height() // 2)
                button_rect_quit.center = (5 * screen_width() // 8, 5*screen_height()//8)
                button_rect_play.center = (3*screen_width() // 8, 5*screen_height()//8)

                mouse_x, mouse_y = pygame.mouse.get_pos()

                if button_rect_play.collidepoint(mouse_x, mouse_y):
                    screen.blit(button_image2, button_rect_play)
                    draw_text(screen, "Play Again", font, color_title, button_rect_play.centerx, button_rect_play.centery + 10)
                else:
                    screen.blit(button_image1, button_rect_play)
                    draw_text(screen, "Play Again", font, color_title, button_rect_play.centerx, button_rect_play.centery)
                
                if button_rect_quit.collidepoint(mouse_x, mouse_y):
                    screen.blit(button_image2, button_rect_quit)
                    draw_text(screen, "Quit", font, color_title, button_rect_quit.centerx, button_rect_quit.centery + 10)

                else:
                    screen.blit(button_image1, button_rect_quit)
                    draw_text(screen, "Quit", font, color_title, button_rect_quit.centerx, button_rect_quit.centery)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                            sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if button_rect_play.collidepoint(mouse_x, mouse_y):
                            return "Play"
                        if button_rect_quit.collidepoint(mouse_x, mouse_y):
                            sys.exit()
                pygame.display.flip()

            running = False

        if plongeur.start and plongeur.profondeur <= 0 and plongeur.profondeur_max > 0:
            if mod == "Play":
                detection = False
                font = pygame.font.Font("font/04B_03__.TTF", 30)
                #Dim : 48 * 16 pixels
                button_image1 = pygame.image.load("images/button/[1] Normal.png").convert_alpha()
                button_image2 = pygame.image.load("images/button/[2] Clicked.png").convert_alpha()
                button_image1 = pygame.transform.scale(button_image1, (screen_width() // 6, screen_width() // 6 * 16 /48))
                button_image2 = pygame.transform.scale(button_image2, (screen_width() // 6, screen_width() // 6 * 16 /48))
                button_rect_yes = button_image1.get_rect()
                button_rect_yes.center = (3*screen_width() // 8, 5*screen_height()//8)
                button_rect_no = button_image1.get_rect()
                button_rect_no.center = (5 * screen_width() // 8, 5*screen_height()//8)
                color_title = (20,20,110)
                while not detection:
                    dashboard.draw_background()
                    fish_behind.draw(screen)
                    dashboard.draw_foreground()
                    Diver.draw(screen)
                    fish_infront.draw(screen)
                    dashboard.draw_info()
                    dashboard.draw_time(plongeur.total_time / FPS)

                    afficher_message(screen, f"You reached {round(plongeur.profondeur_max,1)} meters", screen_width()//2, 2 * screen_height() // 5)
                    afficher_message(screen, "Did you hold your breath the whole time ?", screen_width()//2, screen_height() // 2)

                    button_rect_no.center = (5 * screen_width() // 8, 5*screen_height()//8)
                    button_rect_yes.center = (3*screen_width() // 8, 5*screen_height()//8)

                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    if button_rect_yes.collidepoint(mouse_x, mouse_y):
                        screen.blit(button_image2, button_rect_yes)
                        draw_text(screen, "YES !", font, color_title, button_rect_yes.centerx, button_rect_yes.centery + 10)
                    else:
                        screen.blit(button_image1, button_rect_yes)
                        draw_text(screen, "YES !", font, color_title, button_rect_yes.centerx, button_rect_yes.centery)
                    
                    if button_rect_no.collidepoint(mouse_x, mouse_y):
                        screen.blit(button_image2, button_rect_no)
                        draw_text(screen, "No", font, color_title, button_rect_no.centerx, button_rect_no.centery + 10)
                    else:
                        screen.blit(button_image1, button_rect_no)
                        draw_text(screen, "No", font, color_title, button_rect_no.centerx, button_rect_no.centery)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                running = False
                                sys.exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            if button_rect_yes.collidepoint(mouse_x, mouse_y):
                                with open("records/record_play.txt", "r") as fichier:
                                    record = float(fichier.read())
                                if record < round(plongeur.profondeur_max,1):
                                    with open("records/record_play.txt", "w") as fichier:
                                        fichier.write(str(round(plongeur.profondeur_max,1)))
                                detection = True
                                success = True
                            if button_rect_no.collidepoint(mouse_x, mouse_y):
                                detection = True
                                success = False
                    pygame.display.flip()

            if mod == "Explore":
                with open("records/record_explore.txt", "r") as fichier:
                    record = float(fichier.read())
                if record < round(plongeur.profondeur_max,1):
                    with open("records/record_explore.txt", "w") as fichier:
                        fichier.write(str(round(plongeur.profondeur_max,1)))

            play_again = False
            font = pygame.font.Font("font/04B_03__.TTF", 30)
            #Dim : 48 * 16 pixels
            button_image1 = pygame.image.load("images/button/[1] Normal.png").convert_alpha()
            button_image2 = pygame.image.load("images/button/[2] Clicked.png").convert_alpha()
            button_image1 = pygame.transform.scale(button_image1, (screen_width() // 6, screen_width() // 6 * 16 /48))
            button_image2 = pygame.transform.scale(button_image2, (screen_width() // 6, screen_width() // 6 * 16 /48))
            button_rect_play = button_image1.get_rect()
            button_rect_play.center = (3*screen_width() // 8, 5*screen_height()//8)
            button_rect_quit = button_image1.get_rect()
            button_rect_quit.center = (5 * screen_width() // 8, 5*screen_height()//8)
            color_title = (20,20,110)
            while not play_again:
                dashboard.draw_background()
                fish_behind.draw(screen)
                dashboard.draw_foreground()
                Diver.draw(screen)
                fish_infront.draw(screen)
                dashboard.draw_info()
                dashboard.draw_time(plongeur.total_time / FPS)

                if mod=="Play":
                    if success:
                        afficher_message(screen, f"You reached {round(plongeur.profondeur_max,1)} meters", screen_width()//2, 2 * screen_height() // 5)
                        afficher_message(screen, f"Congratulations !", screen_width()//2, screen_height() // 2)
                    else:  
                        afficher_message(screen, f"Better luck next time !", screen_width()//2, 2 * screen_height() // 5)
                else:
                    afficher_message(screen, f"You reached {round(plongeur.profondeur_max,1)} meters. Congrats !", screen_width()//2, 2 * screen_height() // 5)
                button_rect_quit.center = (5 * screen_width() // 8, 5*screen_height()//8)
                button_rect_play.center = (3*screen_width() // 8, 5*screen_height()//8)

                mouse_x, mouse_y = pygame.mouse.get_pos()

                if button_rect_play.collidepoint(mouse_x, mouse_y):
                    screen.blit(button_image2, button_rect_play)
                    draw_text(screen, "Play Again", font, color_title, button_rect_play.centerx, button_rect_play.centery + 10)
                else:
                    screen.blit(button_image1, button_rect_play)
                    draw_text(screen, "Play Again", font, color_title, button_rect_play.centerx, button_rect_play.centery)
                
                if button_rect_quit.collidepoint(mouse_x, mouse_y):
                    screen.blit(button_image2, button_rect_quit)
                    draw_text(screen, "Quit", font, color_title, button_rect_quit.centerx, button_rect_quit.centery + 10)

                else:
                    screen.blit(button_image1, button_rect_quit)
                    draw_text(screen, "Quit", font, color_title, button_rect_quit.centerx, button_rect_quit.centery)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                            sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if button_rect_play.collidepoint(mouse_x, mouse_y):
                            return "Play"
                        if button_rect_quit.collidepoint(mouse_x, mouse_y):
                            return "QUIT"
                pygame.display.flip()

            running = False

        # Rendu
        dashboard.draw_background()
        fish_behind.draw(screen)
        dashboard.draw_foreground()
        Diver.draw(screen)
        fish_infront.draw(screen)
        dashboard.draw_info()
        dashboard.warning()

        pygame.display.flip()

def afficher_message(screen, message, w, h):
    font = pygame.font.Font("font/04B_03__.TTF", 40)
    text = font.render(message, True, WHITE)
    text_rect = text.get_rect(center= (w, h))
    # screen.fill(BLUE)
    screen.blit(text, text_rect)

def run():
    screen = init()
    clock = pygame.time.Clock()
    info = menu(screen)
    while info != "QUIT":
        info = run_game(screen)
    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()


