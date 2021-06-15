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


class Cube:
    def __init__(self, camera, position, rotation, scale):
        self.camera = camera
        self.position = position
        self.rotation = rotation
        self.rx, self.ry, self.rz = self.rotation
        self.scale = scale
        self.corners = [np.matrix([x, y, z, 1]).T for x in [-0.5, 0.5] for y in [-0.5, 0.5] for z in [-0.5, 0.5]]
        self.edges = [(0, 1), (0, 2), (0, 4), (1, 3), (1, 5), (2, 3), (2, 6), (3, 7), (4, 5), (4, 6), (5, 7), (6, 7)]
        self.abs_corners = self.absolute_corners()

    def absolute_corners(self):
        return [translate(self.position,
                          rotate_x(self.rx,
                                   rotate_y(self.ry,
                                            rotate_z(self.rz,
                                                     do_scale(self.scale, corner)
                                                     )
                                            )
                                   )
                          )
                for corner in self.corners]

    def draw(self, window, color, d=(0, 1), update=False):
        if update:
            rendered_corners = [self.camera.render(self.camera.relative(corner)) for corner in self.absolute_corners()]
            if d[0]:
                for corner in rendered_corners:
                    if corner:
                        pygame.draw.circle(window, color, corner, 5)
            if d[1]:
                for edge in self.edges:
                    if rendered_corners[edge[0]] and rendered_corners[edge[1]]:
                        pygame.draw.line(window, color, rendered_corners[edge[0]], rendered_corners[edge[1]], 1)
            self.update()
        else:
            relative_corners = [self.camera.relative(corner) for corner in self.abs_corners]
            if d[0]:
                for corner in relative_corners:
                    a = self.camera.render(corner)
                    if a:
                        pygame.draw.circle(window, color, a, 5)
            if d[1]:
                for edge in self.edges:
                    a, b = relative_corners[edge[0]], relative_corners[edge[1]]
                    line = self.camera.render_line(a, b, algorithm=True)
                    if line:
                        pygame.draw.line(window, color, line[0], line[1], 1)

    def update(self):
        self.rx += 0.01
        self.ry += 0.01
        self.rz += 0.01
