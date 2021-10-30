import numpy as np
import math


def rotate_x(angle, point):
    matrix = np.matrix(
        [
            [1, 0, 0, 0],
            [0, math.cos(angle), math.sin(angle), 0],
            [0, -math.sin(angle), math.cos(angle), 0],
            [0, 0, 0, 1]
        ]
    )
    return matrix @ point


def rotate_y(angle, point):
    matrix = np.matrix(
        [
            [math.cos(angle), 0, math.sin(angle), 0],
            [0, 1, 0, 0],
            [-math.sin(angle), 0, math.cos(angle), 0],
            [0, 0, 0, 1]
        ]
    )
    return matrix @ point


def rotate_z(angle, point):
    matrix = np.matrix(
        [
            [math.cos(angle), -math.sin(angle), 0, 0],
            [math.sin(angle), math.cos(angle), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]
    )
    return matrix @ point


def translate(translation, point, constant=1):
    matrix = np.matrix(
        [
            [1, 0, 0, constant * translation[0]],
            [0, 1, 0, constant * translation[1]],
            [0, 0, 1, constant * translation[2]],
            [0, 0, 0, 1]
        ]
    )
    return matrix @ point


def intersection(point_1, point_2, plane):
    a, b, c = point_1.item(0, 0), point_1.item(1, 0), point_1.item(2, 0)
    d, e, f = point_2.item(0, 0), point_2.item(1, 0), point_2.item(2, 0)
    k = (plane - c) / (f - c)
    return np.matrix([(d - a) * k + a, (e - b) * k + b, plane, 1]).T


class Camera:
    def __init__(self, position, rotation, fov, clipping_planes, offset):
        self.position = np.matrix(list(position) + [1], dtype=float).T
        self.rx, self.ry, self.rz = rotation
        self.fov = fov
        self.offset = offset
        self.ow, self.oh = self.offset
        self.a = self.ow / math.tan(self.fov * math.pi / 360)
        self.clipping = clipping_planes
        self.near, self.far = self.clipping

    def relative(self, point):
        return rotate_x(-self.rx,
                        rotate_y(-self.ry,
                                 rotate_z(-self.rz,
                                          translate(self.position.T.tolist()[0], point, -1)
                                          )
                                 )
                        )

    def perspective(self, relative_point):
        matrix = np.matrix(
            [
                [self.a, 0, self.ow, 0],
                [0, -self.a, self.oh, 0],
                [0, 0, 1, 0]
            ]
        )
        homogeneous_result = matrix @ relative_point
        return np.squeeze(np.asarray(homogeneous_result / homogeneous_result[-1])).tolist()[:-1]

    def render(self, relative):
        if self.near < relative.item(2, 0) < self.far:
            return self.perspective(relative)

    def render_line(self, relative_1, relative_2):
        a, b = relative_1.item(2, 0), relative_2.item(2, 0)
        if a < self.near:
            if b < self.near:
                u = None
            else:
                u = self.perspective(intersection(relative_1, relative_2, self.near))
        elif a > self.far:
            if b > self.far:
                u = None
            else:
                u = self.perspective(intersection(relative_1, relative_2, self.far))
        else:
            u = self.perspective(relative_1)
        if b < self.near:
            if a < self.near:
                v = None
            else:
                v = self.perspective(intersection(relative_1, relative_2, self.near))
        elif b > self.far:
            if a > self.far:
                v = None
            else:
                v = self.perspective(intersection(relative_1, relative_2, self.far))
        else:
            v = self.perspective(relative_2)
        if not ((a < self.near and b < self.near) or (a > self.far and b > self.far)):
            return u, v
