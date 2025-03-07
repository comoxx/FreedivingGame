import pygame
FPS = 60

#Physics parameters :
WATER_DENSITY = 1020
G = 9.81

#Game parameters : 
DEPTH_BOTTOM_INIT = 25 #meters
HEIGHT_POSITION = 1 / 3
MAX_DEPTH = 80
MAX_DEPTH_PARRALAX = MAX_DEPTH - DEPTH_BOTTOM_INIT

#Fish :
MIN_DEPTH_FISH = 2
MAX_DEPTH_FISH = 30
PROBA_FISH = 0.005

MIN_DEPTH_BIGFISH = 60
MAX_DEPTH_BIGFISH = 100
PROBA_BIGFISH = 0.003

MIN_DEPTH_DARTFISH = 10
MAX_DEPTH_DARTFISH = 80
PROBA_DARTFISH = 0.005

MIN_DEPTH_GLOBEFISH = 5
MAX_DEPTH_GLOBEFISH = 30
PROBA_GLOBEFISH = 0.002

MIN_DEPTH_SHARK = 10
MAX_DEPTH_SHARK = 100
PROBA_SHARK = 0.0005

#DIVER :
PALM_FORCE = 5000 # Newtons
WEIGHT = 70 #kilos
INCOMPRESSIBLE_VOLUME = 66 #Liters
LUNGS_VOLUME = 8 #Liters
FRICTION_COEF = 0.05


#Colors : 
YELLOW = (255, 165, 0)
BLACK = (0, 0, 0)
BLUE = (94, 126, 181)
WHITE = (255, 255, 255) 
CIRCLE_COLOR = (178, 212, 255)
WATER_TOP_COLOR = (94, 126, 181)
WATER_BOTTOM_COLOR =  (62, 121, 221)
OCEAN_IMAGE_COLOR = (94,126,181)
RED = (255,0,0)



#Get dimensions of the screen :
def screen_width():
    screen_info = pygame.display.Info()
    return screen_info.current_w

def screen_height():
    screen_info = pygame.display.Info()
    return screen_info.current_h

