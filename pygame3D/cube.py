from pygame3D.object import Object


class Cube(Object):
    def __init__(self, camera, position, rotation, scale, color):
        super().__init__(camera, position, rotation, scale, color,
                         corners=[(x, y, z) for x in [-0.5, 0.5] for y in [-0.5, 0.5] for z in [-0.5, 0.5]],
                         edges=[
                             (0, 1), (0, 2), (0, 4), (1, 3), (1, 5), (2, 3),
                             (2, 6), (3, 7), (4, 5), (4, 6), (5, 7), (6, 7)
                         ]
                         )
