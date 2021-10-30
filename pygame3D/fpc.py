import numpy as np
import pygame
from pygame.locals import *
import math


class FirstPersonController:
    def __init__(self, camera, velocity=3.0, sensitivity=0.01):
        """
        First Person Controller that can be attached to a camera
        :param camera: the camera that the controller is attached to
        :param velocity: velocity of the controller (world units per second)
        :param sensitivity: how sensitive it responds to mouse movements (radian per pixel)
        """
        self.velocity = velocity
        self.sensitivity = sensitivity
        self.camera = camera
        # make the cursor invisible
        pygame.mouse.set_visible(False)
        # and make it able to go off the screen
        pygame.event.set_grab(True)

    def rotate(self):
        """
        rotates the camera according to the mouse movement (position difference from the previous frame)
        """
        a, b = pygame.mouse.get_rel()
        # the reason for the sign difference is that:
        # mouse goes right --> mouse x movement positive --> we should increase the rotation y of the camera
        # mouse goes down  --> mouse y movement positive --> we should decrease the rotation x of the camera
        self.camera.ry += self.sensitivity * a  # left right movement affects the rotation y
        self.camera.rx -= self.sensitivity * b  # up down movement affects the rotation x

    def move(self, fps):
        """
        moves the camera
        :param fps: the current fps, needed to move the camera by an amount independent of the fps
        """
        y = self.camera.ry  # only the rotation y is needed to construct the movement matrix
        matrix = np.matrix(
            [
                [math.cos(y), math.sin(y)],
                [0, 0],
                [-math.sin(y), math.cos(y)],
                [0, 0]
            ]
        )
        keys = pygame.key.get_pressed()
        a = keys[K_d] - keys[K_a]  # 1: right, -1: left, 0: no left-right movement
        b = keys[K_w] - keys[K_s]  # 1: up,    -1: down, 0: no up-down movement
        # if there is a movement and the frame needs to be updated
        if a * a + b * b != 0 and fps != 0:
            # fps in the denominator is there because fps should not affect the movement
            k = self.velocity / (fps * math.sqrt(a * a + b * b))
            self.camera.position += k * (matrix @ np.matrix([a, b]).T)

    def update(self, fps):
        """
        updates the camera every frame
        :param fps: the current fps, needed for the camera movement
        """
        self.rotate()
        self.move(fps)
