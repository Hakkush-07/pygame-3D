import pygame
from pygame.locals import *
import sys
from pygame3D.camera import Camera
from pygame3D.fpc import FirstPersonController
from pygame3D.cube import Cube
from pygame3D.window import WINDOW, CLOCK, FPS, HALF_W, HALF_H
from pygame3D.colors import *

pygame.init()

camera = Camera(position=(0, 0, 0), rotation=(0, 0, 0), fov=137, clipping_planes=(0.2, 5), offset=(HALF_W, HALF_H))
fpc = FirstPersonController(camera)
cube = Cube(camera=camera, position=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1))

fixed_fps = False

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

    fps = CLOCK.get_fps()
    WINDOW.fill(LIGHT_BLUE)
    WINDOW.blit(pygame.font.Font(None, 32).render(str(int(fps)), True, BLACK), (10, 10))
    cube.draw(WINDOW, BLACK, update=False)
    pygame.display.update()

    fpc.update(fps)

    if fixed_fps:
        CLOCK.tick(FPS)
    else:
        CLOCK.tick()


# TODO Object class with corners and edges parameter
# TODO first, Sphere class
