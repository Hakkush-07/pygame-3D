from math import sin, cos

class WorldPoint:
    """
    point in the world
    """
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __repr__(self):
        return f"WorldPoint({self.x}, {self.y}, {self.z})"
    
    def __iter__(self):
        return iter((self.x, self.y, self.z))
    
    def __add__(self, other):
        return WorldPoint(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return self + (-other)
    
    def __neg__(self):
        return WorldPoint(-self.x, -self.y, -self.z)

    def __iadd__(self, other):
        return self + other
    
    def rotate_z(self, a):
        """
        rotates around z axis
        a is the rotation angle in radians
        """
        x, y, z = self
        s, c = sin(a), cos(a)
        return WorldPoint(x * c - y * s, y * c + x * s, z)
    
    def rotate_y(self, a):
        """
        rotates around y axis
        a is the rotation angle in radians
        """
        x, y, z = self
        s, c = sin(a), cos(a)
        return WorldPoint(x * c + z * s, y, z * c - x * s)
    
    def clipped(self, near, far):
        return self if near < self.x < far else None

class WorldLine:
    """
    line in the world
    endpoints are WorldPoint
    """
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __repr__(self):
        return f"WorldLine({self.p1}, {self.p2})"
    
    def intersection(self, a):
        """
        intersection point with the plane x = a
        """
        dx, dy, dz = self.p2 - self.p1
        syx = dy / dx if dx else 1000
        szx = dz / dx if dx else 1000
        y = self.p1.y + (a - self.p1.x) * syx
        z = self.p1.z + (a - self.p1.x) * szx
        return WorldPoint(a, y, z)
    
    def clipped(self, near, far):
        """
        returns clipped to the volume defined by the planes
        x = near, x = far
        """
        if self.p1.x < near and self.p2.x < near:
            # line is outside of the volume
            return
        if self.p1.x > far and self.p2.x > far:
            # line is outside of the volume
            return
        if near <= self.p1.x <= far and near <= self.p2.x <= far:
            # line is inside of the volume
            return self
        
        # line needs to be clipped

        # find new p1
        p1 = self.p1
        if self.p1.x < near:
            p1 = self.intersection(near)
        elif self.p1.x > far:
            p1 = self.intersection(far)
        
        # find new p2
        p2 = self.p2
        if self.p2.x < near:
            p2 = self.intersection(near)
        elif self.p2.x > far:
            p2 = self.intersection(far)
        
        return WorldLine(p1, p2)

class WorldPolygon:
    """
    polygon in the world
    vertices are WorldPoint
    """
    def __init__(self, vertices):
        self.vertices = vertices
    
    def clip_min_x(self, border):
        """
        removes left of the plane x = border
        """
        new_vertices = []
        for i in range(-1, len(self.vertices) - 1):
            x1, _, _ = p1 = self.vertices[i]
            x2, _, _ = p2 = self.vertices[i + 1]
            line = WorldLine(p1, p2)

            if x1 < border and x2 < border:
                pass
            elif x1 < border and x2 > border:
                new_vertices.append(line.intersection(border))
                new_vertices.append(p2)
            elif x1 > border and x2 < border:
                new_vertices.append(line.intersection(border))
            elif x1 > border and x2 > border:
                new_vertices.append(p2)
        return WorldPolygon(new_vertices)
    
    def clip_max_x(self, border):
        """
        removes right of the plane x = border
        """
        new_vertices = []
        for i in range(-1, len(self.vertices) - 1):
            x1, _, _ = p1 = self.vertices[i]
            x2, _, _ = p2 = self.vertices[i + 1]
            line = WorldLine(p1, p2)

            if x1 > border and x2 > border:
                pass
            elif x1 > border and x2 < border:
                new_vertices.append(line.intersection(border))
                new_vertices.append(p2)
            elif x1 < border and x2 > border:
                new_vertices.append(line.intersection(border))
            elif x1 < border and x2 < border:
                new_vertices.append(p2)
        return WorldPolygon(new_vertices)
    
    def clipped(self, near, far):
        """
        returns clipped polygon to the volume defined by the planes
        x = near, x = far
        """
        if all([p.x < near for p in self.vertices]) or all([p.x > far for p in self.vertices]):
            # polygon is inside the volume
            return
        if all([near <= p.x <= far for p in self.vertices]):
            # polygon is outside the volume
            return self

        # polygon needs to be clipped
        clipped_polygon = self.clip_min_x(near).clip_max_x(far)
        return clipped_polygon if len(clipped_polygon.vertices) > 2 else None
