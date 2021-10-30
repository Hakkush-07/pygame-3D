from pygame3D.object import Object

phi = (1 + 5**0.5) / 2


class Icosahedron(Object):
    def __init__(self, camera, position, rotation, scale, color):
        super().__init__(camera, position, rotation, scale, color,
                         corners=[(0.0, i, j) for i in [-1.0, 1.0] for j in [-phi, phi]] +
                                 [(i, j, 0.0) for i in [-1.0, 1.0] for j in [-phi, phi]] +
                                 [(j, 0.0, i) for i in [-1.0, 1.0] for j in [-phi, phi]],
                         edges=[
                             (0, 2), (1, 3), (4, 6), (5, 7), (8, 10), (9, 11), (0, 4), (0, 6), (0, 8), (0, 9), (2, 8),
                             (2, 5), (2, 7), (2, 9), (1, 4), (1, 6), (1, 10), (1, 11), (3, 5), (3, 7), (3, 10),
                             (3, 11), (4, 8), (4, 10), (5, 8), (5, 10), (6, 9), (6, 11), (7, 9), (7, 11)
                         ]
                         )
