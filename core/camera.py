from math import tan, pi
from core.window import WindowPoint, WindowLine, WindowPolygon
from core.world import WorldPoint, WorldLine, WorldPolygon
from core.rotation import Rotation

class Camera:
    """
    camera
    position is a WorldPoint
    rotation is a Rotation
    clipping_planes is a tuple of two elements for near and far
    fov is the field of view angle in radians
    """
    def __init__(self):
        self.position = WorldPoint(0, 0, 0)
        self.rotation = Rotation(0, 0)
        self.clipping_planes = (1, 5)
        self.fov = 0.6 * pi

    def __repr__(self):
        return f"Camera(position: {self.position}, rotation: {self.rotation}, clippings: {self.clipping_planes}, fov: {self.fov})"
    
    def render_point(self, world_point):
        """
        converts WorldPoint to WindowPoint
        """
        clipped_relative_point = self.relative_position(world_point).clipped(*self.clipping_planes)
        if clipped_relative_point:
            return self.perspective(clipped_relative_point)
        
    def render_line(self, world_line):
        """
        converts WorldLine to WindowLine
        """
        clipped_relative_line = WorldLine(self.relative_position(world_line.p1), self.relative_position(world_line.p2)).clipped(*self.clipping_planes)
        if clipped_relative_line:
            return WindowLine(self.perspective(clipped_relative_line.p1), self.perspective(clipped_relative_line.p2))
        
    def render_polygon(self, world_polygon):
        """
        converts WorldPolygon to WindowPolygon
        """
        clipped_relative_polygon = WorldPolygon([self.relative_position(p) for p in world_polygon.vertices]).clipped(*self.clipping_planes)
        if clipped_relative_polygon:
            return WindowPolygon([self.perspective(p) for p in clipped_relative_polygon.vertices])
    
    def relative_position(self, world_point):
        """
        relative world position of the WorldPoint
        """
        return (world_point - self.position).rotate_z(-self.rotation.a).rotate_y(self.rotation.b)
    
    def perspective(self, relative_point):
        """
        converts relative WorldPoint to WindowPoint
        """
        x, y, z = relative_point
        k = 0.5 / tan(0.5 * self.fov)
        return WindowPoint(-k * y / x, k * z / x)
