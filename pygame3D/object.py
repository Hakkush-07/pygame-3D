import numpy as np
import pygame
from pygame3D.camera import rotate_x, rotate_y, rotate_z, translate


def do_scale(factor, point):
    matrix = np.matrix(
        [
            [factor[0], 0, 0, 0],
            [0, factor[1], 0, 0],
            [0, 0, factor[2], 0],
            [0, 0, 0, 1]
        ]
    )
    return matrix @ point


class Object:
    def __init__(self, camera, position, rotation, scale, color, corners, edges):
        self.camera = camera
        self.position = position
        self.rotation = rotation
        self.rx, self.ry, self.rz = self.rotation
        self.scale = scale
        self.color = color
        self.raw_corners = [np.matrix([x, y, z, 1]).T for x, y, z in corners]
        self.corners = self.get_corners()
        self.edges = edges
        self.use_update = False

    def get_corners(self):
        return [translate(self.position,
                          rotate_x(self.rx,
                                   rotate_y(self.ry,
                                            rotate_z(self.rz,
                                                     do_scale(self.scale, corner)
                                                     )
                                            )
                                   )
                          )
                for corner in self.raw_corners]

    def draw(self, window, fps, render_corners=False, render_edges=True):
        relative_corners = [self.camera.relative(corner) for corner in self.corners]
        if render_corners:
            for corner in relative_corners:
                a = self.camera.render(corner)
                if a:
                    pygame.draw.circle(window, self.color, a, 5)
        if render_edges:
            for edge in self.edges:
                line = self.camera.render_line(relative_corners[edge[0]], relative_corners[edge[1]])
                if line:
                    pygame.draw.line(window, self.color, line[0], line[1], 1)
        if self.use_update:
            self.update(fps)

    def update(self, fps):
        if fps != 0:
            self.rx += 0.01 * 60 / fps
            self.ry += 0.01 * 60 / fps
            self.rz += 0.01 * 60 / fps
        self.corners = self.get_corners()
