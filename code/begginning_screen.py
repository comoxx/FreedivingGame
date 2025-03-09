import pygame
import time
from code.objects.bubbles import Bubbles
import random
from code.constants import *


bubbles_behind = pygame.sprite.Group()
bubbles_infront = pygame.sprite.Group()


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


def draw_text_centered(surface, text_lines, font, color, center_x = None, center_y= None):
    if center_x == None:
        center_x = surface.get_width() // 2
    if center_y == None:
        center_y = surface.get_height() //2
    """Dessine du texte multiligne centré horizontalement et verticalement."""
    total_height = sum(font.get_linesize() for line in text_lines)
    y = center_y - total_height // 2  
    for i in range(len(text_lines)):
        text_surface = font.render(text_lines[i], True, color[i])
        text_rect = text_surface.get_rect()
        text_rect.centerx = center_x  
        text_rect.y = y
        surface.blit(text_surface, text_rect)
        y += font.get_linesize()


all_sprites = pygame.sprite.Group()

def draw_foreground(screen):
    image_1 = pygame.image.load("images/background/foreground-1.png").convert_alpha()
    image_2 = pygame.image.load("images/background/foreground-2.png").convert_alpha()
    rect = image_1.get_rect()
    hauteur_image = rect.height #192 px for both
    largeur_image = rect.width # 256 px for both
    new_hauteur = hauteur_image * screen_width() / (3 * largeur_image)
    image_1 = pygame.transform.scale(image_1, (screen_width() / 3, new_hauteur))
    image_2 = pygame.transform.scale(image_2, (screen_width() / 3, new_hauteur))
    screen.blit(image_1, (0, screen_height() - new_hauteur))
    screen.blit(image_2, (screen_width() / 3, screen_height() - new_hauteur))
    screen.blit(image_1, (screen_width() * 2 / 3, screen_height() - new_hauteur))

def draw_background(screen):
    global bubbles_behind
    global bubbles_infront
    global all_sprites
    image_far = pygame.image.load("images/background/far.png").convert_alpha()
    image_sand = pygame.image.load("images/background/sand.png").convert_alpha()
    rect = image_sand.get_rect()
    hauteur_image = rect.height #192
    largeur_image = rect.width #256
    new_hauteur = hauteur_image * screen_width() / (3 * largeur_image)
    image_sand = pygame.transform.scale(image_sand, (screen_width() / 3, new_hauteur))
    image_far = pygame.transform.scale(image_far, (screen_width() / 3, new_hauteur))
    for y in range(screen_height()):
            color = (
                WATER_TOP_COLOR[0] + (WATER_BOTTOM_COLOR[0] - WATER_TOP_COLOR[0]) * min(y / (screen_height() - new_hauteur), 1),
                WATER_TOP_COLOR[1] + (WATER_BOTTOM_COLOR[1] - WATER_TOP_COLOR[1]) * min(y / (screen_height() - new_hauteur), 1),
                WATER_TOP_COLOR[2] + (WATER_BOTTOM_COLOR[2] - WATER_TOP_COLOR[2]) * min(y / (screen_height() - new_hauteur), 1)
            )
            pygame.draw.line(screen, color, (0, y), (screen_width(), y))
    for i in range(3):
        screen.blit(image_far, (screen_width() * i / 3, screen_height() - new_hauteur))
    for i in range(3):
        screen.blit(image_sand, (screen_width() * i / 3, screen_height() - new_hauteur))

    if (random.random() < 0.07 and len(all_sprites.sprites()) < 50):
        bubble = Bubbles(screen, bubbles_behind, bubbles_infront)
        if bubble.infront:
            bubbles_infront.add(bubble)
        else:
            bubbles_behind.add(bubble)

    for i in bubbles_infront:
        if i.finished:
            bubbles_infront.remove(i)

    for i in bubbles_behind:
        if i.finished:
            bubbles_behind.remove(i)



def menu(screen):
    global bubbles_infront, bubbles_behind
    running_menu = True
    font_title = pygame.font.Font("font/04B_03__.TTF", 100)
    font = pygame.font.Font("font/04B_03__.TTF", 30)
    color_title = (20,20,110)
    frame_count = 0
    while running_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_menu = False
                return "QUIT"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running_menu = False
                    return "QUIT"
                if event.key == pygame.K_SPACE:
                    running_menu = False
                    return True
        bubbles_infront.update()
        bubbles_behind.update()
        draw_background(screen)
        bubbles_behind.draw(screen)
        draw_text(screen, "The FreeDiving Game", font_title, color_title, None, 5 * screen_height() // 13)
        draw_foreground(screen)
        # if frame_count % (2*FPS) < FPS: 
        draw_text(screen, "Press Space Bar to continue", font, WHITE, None, 5 * screen_height() // 7)
        draw_text(screen, "Press ESC to exit", font, WHITE, None, 11 * screen_height() // 14)
        bubbles_infront.draw(screen)
        # draw_text(screen, "@Come HOSXE", font_credits, WHITE, 9*screen_width()// 10, 15 * screen_height() // 16)

        frame_count += 1
        pygame.display.flip()

def selection(screen):
    running = True
    font = pygame.font.Font("font/04B_03__.TTF", 30)
    font_credits = pygame.font.Font("font/04B_03__.TTF", 24)
    #Dim : 48 * 16 pixels
    button_image1 = pygame.image.load("images/button/[1] Normal.png").convert_alpha()
    button_image2 = pygame.image.load("images/button/[2] Clicked.png").convert_alpha()
    button_image1 = pygame.transform.scale(button_image1, (screen_width() // 6, screen_width() // 6 * 16 /48))
    button_image2 = pygame.transform.scale(button_image2, (screen_width() // 6, screen_width() // 6 * 16 /48))
    
    button_image3 = pygame.transform.scale(button_image1, (screen_width() // 10, screen_width() // 10 * 16 /48))
    button_image4 = pygame.transform.scale(button_image2, (screen_width() // 10, screen_width() // 10 * 16 /48))


    button_rect_play = button_image1.get_rect()
    button_rect_play.center = (3*screen_width() // 8, 5*screen_height()//8)
    button_rect_explore = button_image1.get_rect()
    button_rect_explore.center = (5 * screen_width() // 8, 5*screen_height()//8)

    button_rect_credits = button_image3.get_rect()
    button_rect_credits.center = (screen_width() // 2, 7*screen_height()//8)
    color_title = (20,20,110)

    font_title = pygame.font.Font("font/04B_03__.TTF", 100)

    while running:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        bubbles_infront.update()
        bubbles_behind.update()
        draw_background(screen)
        bubbles_behind.draw(screen)
        draw_foreground(screen)
        draw_text(screen, "The FreeDiving Game", font_title, color_title, None, 5 * screen_height() // 13)


        if button_rect_play.collidepoint(mouse_x, mouse_y):
            screen.blit(button_image2, button_rect_play)
            draw_text(screen, "Play", font, color_title, button_rect_play.centerx, button_rect_play.centery + 10)
            draw_text_centered(screen, ["Play the game with your own oxygen !", "A real freediving simulation"], font, [WHITE, WHITE], button_rect_play.centerx, button_rect_play.centery + 100)
        else:
            screen.blit(button_image1, button_rect_play)
            draw_text(screen, "Play", font, color_title, button_rect_play.centerx, button_rect_play.centery)
        
        if button_rect_explore.collidepoint(mouse_x, mouse_y):
            screen.blit(button_image2, button_rect_explore)
            draw_text(screen, "Explore", font, color_title, button_rect_explore.centerx, button_rect_explore.centery + 10)
            draw_text_centered(screen, ["Play the game with", "an oxygen bar"], font, [WHITE, WHITE], button_rect_explore.centerx, button_rect_explore.centery + 100)

        else:
            screen.blit(button_image1, button_rect_explore)
            draw_text(screen, "Explore", font, color_title, button_rect_explore.centerx, button_rect_explore.centery)

        if button_rect_credits.collidepoint(mouse_x, mouse_y):
            screen.blit(button_image4, button_rect_credits)
            draw_text(screen, "Credits", font_credits, color_title, button_rect_credits.centerx, button_rect_credits.centery + 8)
            # draw_text_centered(screen, ["Play the game with your own oxygen !", "A real freediving simulation"], font, [WHITE, WHITE], button_rect_play.centerx, button_rect_play.centery + 100)
        else:
            screen.blit(button_image3, button_rect_credits)
            draw_text(screen, "Credits", font_credits, color_title, button_rect_credits.centerx, button_rect_credits.centery)
        
        # draw_text(screen, "@Come HOSXE", font_credits, WHITE, 9*screen_width()// 10, 15 * screen_height() // 16)
        bubbles_infront.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "QUIT"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    return "QUIT"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect_play.collidepoint(mouse_x, mouse_y):
                    return "Play"
                if button_rect_explore.collidepoint(mouse_x, mouse_y):
                    return "Explore"
                if button_rect_credits.collidepoint(mouse_x, mouse_y):
                    return "Credits"
        pygame.display.flip()

def credits(screen):
    global bubbles_behind, bubbles_infront
    running_menu = True
    font = pygame.font.Font("font/04B_03__.TTF", 30)
    while running_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_menu = False
                return "QUIT"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running_menu = False
                    return "QUIT"
                else:
                    running_menu = False
                    return "SELECTION"
        # Efface l'écran avec une couleur bleue
        bubbles_infront.update()
        bubbles_behind.update()
        draw_background(screen)
        bubbles_behind.draw(screen)
        draw_foreground(screen)

        # Affiche les instructions
        text_lines = ["CREDITS"," ",  
                      "By Come Hosxe","In Ali-Deniz Ozkan's course : The GameLab 2024", 
                      "Music by Pascal Belisle (public license)", "Graphics by Luis Zuno (public license)", " ", " ",
                      "CONTACT"," ", "come.hosxe@gmail.com"
                      ]
        color = [YELLOW, BLACK, 
                 BLACK, BLACK, 
                 BLACK, BLACK, BLACK, BLACK,
                 YELLOW, BLACK, BLACK]
        
        draw_text_centered(screen, text_lines, font, color)
        bubbles_infront.draw(screen)
        #draw_text(screen, "Press enter to continue...", font, WHITE, 2 * screen_width() // 3, 7 * screen_height() // 8)
        pygame.display.flip()


def beginning(screen, mod):
    global bubbles_behind, bubbles_infront
    running_menu = True
    font = pygame.font.Font("font/04B_03__.TTF", 30)
    frame_count = 0
    while running_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_menu = False
                return "QUIT"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running_menu = False
                    return "QUIT"
                elif event.key == pygame.K_SPACE:
                    running_menu = False
        # Efface l'écran avec une couleur bleue
        bubbles_infront.update()
        bubbles_behind.update()
        draw_background(screen)
        bubbles_behind.draw(screen)
        draw_foreground(screen)

        # Affiche les instructions
        if mod=="Play":
            text_lines = ["INSTRUCTIONS", " ", "Prepare to hold your breath", "and dive into the depths of the ocean.", "You'll need to relax to hold your breath longer", " ", " ",
                           "BE CAREFUL", " ", "You have an energy bar with 30 fin strokes !", " ", " ",
                           "CONTROLS"," ", "Press Enter to palm", "Use Space Bar to turn around",
                           ]
            color = [YELLOW, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK,
                    YELLOW, BLACK, BLACK, BLACK, BLACK,
                    YELLOW, BLACK, BLACK, BLACK]
            
        if mod=="Explore": 
            "Oxygen bar : decreases at each time and", "with every stroke of the fins"
            text_lines = ["INSTRUCTIONS", " ",  "Discover the game without holding your breath.", "You will have a simulated oxygen bar !", " ", " ",
                        "BE CAREFUL", " ", "Energy bar : 30 fin strokes", "Oxygen Bar : decreases at each time and with every stroke of the fins", " ", " ",
                        "CONTROLS"," ", "Press Enter to palm", "Use space bar to turn around"]
            color = [YELLOW, BLACK, BLACK, BLACK, BLACK, BLACK,
                     YELLOW, BLACK, BLACK, BLACK, BLACK, BLACK,
                     YELLOW, BLACK, BLACK, BLACK]
        draw_text_centered(screen, text_lines, font, color)
        if frame_count % (2*FPS) < FPS: 
            draw_text(screen, "Press Space Bar to start...", font, WHITE, None, 6 * screen_height() // 7)
        bubbles_infront.draw(screen)
        pygame.display.flip()

        frame_count += 1

def draw_circle(screen, color, x, y, radius):
    """Dessine un cercle sur l'écran."""
    surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    gradient = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(gradient, (255, 255, 255, 0), (radius, radius), radius)
    pygame.draw.circle(gradient, color, (radius, radius), radius)
    surface.blit(gradient, (0, 0), special_flags=pygame.BLEND_RGBA_MAX)

    # Dessiner le cercle sur l'écran avec le dégradé
    screen.blit(surface, (x - radius, y - radius))

def square_breath(screen):
    global bubbles_infront, bubbles_behind
    font = pygame.font.Font("font/04B_03__.TTF", 30)
    running = True
    inhale_duration = 5  # Durée de l'inhalation en secondes
    hold_duration = 5    # Durée de la retenue en secondes
    exhale_duration = 5  # Durée de l'exhalation en secondes
    pause_duration = 5   # Durée de la pause entre chaque phase en secondes
    start_time = time.time()
    phase = "inhale"  # Phase initiale

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "QUIT"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    return "QUIT"
                if event.key == pygame.K_SPACE:
                    running = False

        elapsed_time = time.time() - start_time

        # Logique pour déterminer la phase actuelle
        if phase == "inhale" and elapsed_time >= inhale_duration:
            phase = "hold"
            start_time = time.time()
            elapsed_time = 0
        elif phase == "hold" and elapsed_time >= hold_duration:
            phase = "exhale"
            start_time = time.time()
            elapsed_time = 0

        elif phase == "exhale" and elapsed_time >= exhale_duration:
            phase = "pause"
            start_time = time.time()
            elapsed_time = 0

        elif phase == "pause" and elapsed_time >= pause_duration:
            phase = "inhale"
            start_time = time.time()
            elapsed_time = 0

        # Efface l'écran avec une couleur bleue
        bubbles_behind.update()
        bubbles_infront.update()
        draw_background(screen)
        bubbles_behind.draw(screen)
        draw_foreground(screen)
        square_size = screen_height() // 2
        square_x = (screen_width() - square_size) // 2
        square_y = (screen_height() - square_size) // 2
        pygame.draw.rect(screen, (255, 255, 255), (square_x, square_y, square_size, square_size), 2)

        # Dessiner le petit cercle au contour du carré en fonction de la phase de respiration
        circle_radius = min(square_size, square_size) // 40
        if phase == "inhale":
            circle_x = square_x + (elapsed_time / inhale_duration) * (square_size)
            circle_y = square_y
        elif phase == "hold":
            circle_x = square_x + square_size
            circle_y = square_y + (elapsed_time / hold_duration) * (square_size)
        elif phase == "exhale":
            circle_x = square_x + square_size  - (elapsed_time / exhale_duration) * (square_size)
            circle_y = square_y + square_size
        else:  # phase == "pause"
            circle_x = square_x
            circle_y = square_y + square_size  - (elapsed_time / pause_duration) * (square_size)
        
        pygame.draw.circle(screen, (255, 255, 255), (int(circle_x), int(circle_y)), circle_radius)

        draw_text(screen, "Press space to start the 10 seconds countdown !", font, WHITE, None, 7 * screen_height() // 8)
        # Dessine le cercle avec la taille appropriée selon la phase
        if phase == "inhale":
            circle_radius = int((elapsed_time / inhale_duration) * (screen_width() // 20)) + screen_width() // 20
        elif phase == "hold":
            circle_radius = screen_width() // 20 + screen_width() // 20
        elif phase == "exhale":
            exhale_elapsed_time = elapsed_time
            circle_radius = int((1 - exhale_elapsed_time / exhale_duration) * (screen_width() // 20)) + screen_width() // 20
        else:  # phase == "pause"
            circle_radius = screen_width() // 20
        draw_circle(screen, CIRCLE_COLOR, screen_width() // 2, screen_height() // 2, circle_radius)
        draw_text(screen, phase.upper(), font, BLACK, x=None, y=None)
        draw_text(screen, "Follow the instructions to relax", font, WHITE, x=None, y=screen_height() // 8)
        bubbles_infront.draw(screen)
        # Met à jour l'affichage
        pygame.display.flip()

def countdown(screen):
    global bubbles_infront, bubbles_behind
    number = 10
    font = pygame.font.Font("font/04B_03__.TTF", 100)
    font2 = pygame.font.Font("font/04B_03__.TTF", 30)
    running = True
    start_time = time.time()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "QUIT"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    return "QUIT"
        bubbles_behind.update()
        bubbles_infront.update()
        draw_background(screen)
        bubbles_behind.draw(screen)
        draw_foreground(screen)
        draw_text(screen, str(number), font, WHITE, None, screen_height() // 3)

        text_lines = ["Controls", "", "Press Enter to palm", "Use Spacebar to turn around"]
        color = [YELLOW, WHITE, WHITE, WHITE]
        draw_text_centered(screen, text_lines, font2, color, None, 2 * screen_height() // 3)
        bubbles_infront.draw(screen)
        elapsed_time = time.time() - start_time

        if elapsed_time > 1:
            number -=1
            start_time = time.time()
            if number <=0 :
                for i in bubbles_infront:
                    bubbles_infront.remove(i)
                for i in bubbles_behind:
                    bubbles_behind.remove(i)
                running = False
        pygame.display.flip()
    



        
