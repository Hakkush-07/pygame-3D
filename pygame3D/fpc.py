import numpy as np
import pygame
from pygame.locals import *
import math


class FirstPersonController:
    def __init__(self, camera, velocity=3.0, sensitivity=0.01):
        self.velocity = velocity
        self.sensitivity = sensitivity
        self.camera = camera
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

    def rotate(self):
        a, b = pygame.mouse.get_rel()
        self.camera.ry += self.sensitivity * a
        self.camera.rx -= self.sensitivity * b

    def move(self, fps):
        y = self.camera.ry
        matrix = np.matrix(
            [
                [math.cos(y), math.sin(y)],
                [0, 0],
                [-math.sin(y), math.cos(y)],
                [0, 0]
            ]
        )
        keys = pygame.key.get_pressed()
        a = keys[K_d] - keys[K_a]
        b = keys[K_w] - keys[K_s]
        if a * a + b * b != 0 and fps != 0:
            k = self.velocity / (fps * math.sqrt(a * a + b * b))
            self.camera.position += k * (matrix @ np.matrix([a, b]).T)

    def update(self, fps):
        self.rotate()
        self.move(fps)
