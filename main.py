import pygame
from pygame.locals import *
import sys
from pygame3D import *

pygame.init()

camera = Camera(position=(0, 0, 0), rotation=(0, 0, 0), fov=137, clipping_planes=(0.2, 5), offset=(HALF_W, HALF_H))
fpc = FirstPersonController(camera)
cube = Cube(camera=camera, position=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1), color=BLACK)
ico = Icosahedron(camera=camera, position=(4, 1, 0), rotation=(0, 0, 0), scale=(0.3, 0.3, 0.3), color=BLUE)
objects = [cube, ico]

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
    for obj in objects:
        obj.draw(WINDOW, fps)
    pygame.display.update()

    fpc.update(fps)

    if fixed_fps:
        CLOCK.tick(FPS)
    else:
        CLOCK.tick()
