import pygame
from pygame.locals import FULLSCREEN

# construction of the window and relevant variables

pygame.init()

info = pygame.display.Info()
WINDOW_SIZE = (info.current_w, info.current_h)
WINDOW = pygame.display.set_mode(WINDOW_SIZE, FULLSCREEN)

CLOCK = pygame.time.Clock()
FPS = 60

W, H = WINDOW_SIZE
HALF_W, HALF_H = int(W / 2), int(H / 2)
