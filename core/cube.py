from core.world import WorldPoint, WorldLine, WorldPolygon

class Cube:
    """
    cube in the world
    center coordinates are WorldPoint
    s is scale
    """
    def __init__(self, cx, cy, cz, s):
        self.x = cx
        self.y = cy
        self.z = cz
        self.s = s
        sl = [-s / 2, s / 2]
        self.corners = [WorldPoint(self.x + x, self.y + y, self.z + z) for x in sl for y in sl for z in sl]
        el = [(0, 1), (0, 2), (0, 4), (1, 3), (1, 5), (2, 3), (2, 6), (3, 7), (4, 5), (4, 6), (5, 7), (6, 7)]
        self.edges = [WorldLine(self.corners[i], self.corners[j]) for i, j in el]
        fl = [(0, 1, 3, 2), (0, 1, 5, 4), (0, 2, 6, 4), (1, 3, 7, 5), (2, 3, 7, 6), (4, 5, 7, 6)]
        self.faces = [WorldPolygon([self.corners[i], self.corners[j], self.corners[k], self.corners[l]]) for i, j, k, l in fl]
