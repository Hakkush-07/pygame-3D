class WindowPoint:
    """
    point on the window
    coordinates are in terms of window width
    (0, 0): center
    (0.5, 0): middle of the right border
    (-0.5, 0): middle of the left border
    (0, 0.5): probably a bit above middle of top border
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"WindowPoint({self.x}, {self.y})"
    
    def __iter__(self):
        return iter((self.x, self.y))
    
    def __add__(self, other):
        return WindowPoint(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return self + (-other)
    
    def __neg__(self):
        return WindowPoint(-self.x, -self.y)

    def __iadd__(self, other):
        return self + other
    
    def __mul__(self, other):
        return WindowPoint(other * self.x, other * self.y)
    
    def code(self, min_x, min_y, max_x, max_y):
        """
        region code in Cohen Sutherland Line Clipping Algorithm
        window is the rectangle defined by the lines
        x = min_x, y = min_y, x = max_x, y = max_y

        1001 | 1000 | 1010
        -----|------|-----
        0001 | 0000 | 0010
        -----|------|-----
        0101 | 0100 | 0110

        """
        return (self.x < min_x) * 1 + (self.x > max_x) * 2 + (self.y < min_y) * 4 + (self.y > max_y) * 8
    
    def clipped(self, min_x, min_y, max_x, max_y):
        return self if min_x < self.x < max_x and min_y < self.y < max_y else None

class WindowLine:
    def __init__(self, p1, p2):
        """
        line on the window
        endpoints are WindowPoint
        """
        self.p1 = p1
        self.p2 = p2
    
    def __repr__(self):
        return f"WindowLine({self.p1}, {self.p2})"
    
    def __iter__(self):
        return iter((self.p1, self.p2))
    
    def intersection_x(self, a):
        """
        intersection point with the line x = a
        """
        dx, dy = self.p2 - self.p1
        s = dy / dx if dx else 1000
        y = self.p1.y + (a - self.p1.x) * s
        return WindowPoint(a, y)
    
    def intersection_y(self, b):
        """
        intersection point with the line y = b
        """
        dx, dy = self.p2 - self.p1
        s = dx / dy if dy else 1000
        x = self.p1.x + (b - self.p1.y) * s
        return WindowPoint(x, b)
    
    def clipped(self, min_x, min_y, max_x, max_y):
        """
        Cohen Sutherland Line Clipping Algorithm
        returns clipped line to the rectangle defined by the lines
        x = min_x, y = min_y, x = max_x, y = max_y
        """
        c1 = self.p1.code(min_x, min_y, max_x, max_y)
        c2 = self.p2.code(min_x, min_y, max_x, max_y)
        if c1 == 0 and c2 == 0:
            # line is visible
            return self
        if c1 & c2 != 0:
            # line is invisible
            return

        # line is clipping candidate

        # find new p1 candidate
        p1 = self.p1
        if c1 & 8:
            p1 = self.intersection_y(max_y)
        elif c1 & 4:
            p1 = self.intersection_y(min_y)
        elif c1 & 2:
            p1 = self.intersection_x(max_x)
        elif c1 & 1:
            p1 = self.intersection_x(min_x)
        
        # find new p2 candidate
        p2 = self.p2
        if c2 & 8:
            p2 = self.intersection_y(max_y)
        elif c2 & 4:
            p2 = self.intersection_y(min_y)
        elif c2 & 2:
            p2 = self.intersection_x(max_x)
        elif c2 & 1:
            p2 = self.intersection_x(min_x)
        
        # rerun the algorithm to remove all overflowed line parts
        cc1 = p1.code(min_x, min_y, max_x, max_y)
        cc2 = p2.code(min_x, min_y, max_x, max_y)
        if c1 == 0 and c2 == 0:
            # newly constructed line is visible
            return WindowLine(p1, p2)
        if c1 & c2 != 0:
            # newly constructed line is invisible
            return
        
        # newly constructed line needs to be clipped one more time
        line = WindowLine(p1, p2)

        # find clipped p1
        pp1 = p1
        if cc1 & 8:
            pp1 = line.intersection_y(max_y)
        elif cc1 & 4:
            pp1 = line.intersection_y(min_y)
        elif cc1 & 2:
            pp1 = line.intersection_x(max_x)
        elif cc1 & 1:
            pp1 = line.intersection_x(min_x)
        
        # find clipped p2
        pp2 = p2
        if cc2 & 8:
            pp2 = self.intersection_y(max_y)
        elif cc2 & 4:
            pp2 = self.intersection_y(min_y)
        elif cc2 & 2:
            pp2 = self.intersection_x(max_x)
        elif cc2 & 1:
            pp2 = self.intersection_x(min_x)
        
        return WindowPoint(pp1, pp2)

class WindowPolygon:
    def __init__(self, vertices):
        """
        polygon on the window
        vertices are WindowPoint
        """
        self.vertices = vertices
    
    def clip_min_x(self, border):
        """
        Sutherland Hodgman Polygon Clipping Algorithm one line clipping
        removes left side of the line x = border
        """
        new_vertices = []
        for i in range(-1, len(self.vertices) - 1):
            x1, _ = p1 = self.vertices[i]
            x2, _ = p2 = self.vertices[i + 1]
            line = WindowLine(p1, p2)
            if x1 < border and x2 < border:
                pass
            elif x1 < border and x2 > border:
                new_vertices.append(line.intersection_x(border))
                new_vertices.append(p2)
            elif x1 > border and x2 < border:
                new_vertices.append(line.intersection_x(border))
            elif x1 > border and x2 > border:
                new_vertices.append(p2)
        return WindowPolygon(new_vertices)
    
    def clip_max_x(self, border):
        """
        Sutherland Hodgman polygon Clipping Algorithm one line clipping
        removes right side of the line x = border
        """
        new_vertices = []
        for i in range(-1, len(self.vertices) - 1):
            x1, _ = p1 = self.vertices[i]
            x2, _ = p2 = self.vertices[i + 1]
            line = WindowLine(p1, p2)
            if x1 > border and x2 > border:
                pass
            elif x1 > border and x2 < border:
                new_vertices.append(line.intersection_x(border))
                new_vertices.append(p2)
            elif x1 < border and x2 > border:
                new_vertices.append(line.intersection_x(border))
            elif x1 < border and x2 < border:
                new_vertices.append(p2)
        return WindowPolygon(new_vertices)
    
    def clip_min_y(self, border):
        """
        Sutherland Hodgman Polygon Clipping Algorithm one line clipping
        removes bottom of the line y = border
        """
        new_vertices = []
        for i in range(-1, len(self.vertices) - 1):
            _, y1 = p1 = self.vertices[i]
            _, y2 = p2 = self.vertices[i + 1]
            line = WindowLine(p1, p2)
            if y1 < border and y2 < border:
                pass
            elif y1 < border and y2 > border:
                new_vertices.append(line.intersection_y(border))
                new_vertices.append(p2)
            elif y1 > border and y2 < border:
                new_vertices.append(line.intersection_y(border))
            elif y1 > border and y2 > border:
                new_vertices.append(p2)
        return WindowPolygon(new_vertices)
    
    def clip_max_y(self, border):
        """
        Sutherland Hodgman polygon Clipping Algorithm one line clipping
        removes top of the line y = border
        """
        new_vertices = []
        for i in range(-1, len(self.vertices) - 1):
            _, y1 = p1 = self.vertices[i]
            _, y2 = p2 = self.vertices[i + 1]
            line = WindowLine(p1, p2)
            if y1 > border and y2 > border:
                pass
            elif y1 > border and y2 < border:
                new_vertices.append(line.intersection_y(border))
                new_vertices.append(p2)
            elif y1 < border and y2 > border:
                new_vertices.append(line.intersection_y(border))
            elif y1 < border and y2 < border:
                new_vertices.append(p2)
        return WindowPolygon(new_vertices)
    
    def clipped(self, min_x, min_y, max_x, max_y):
        """
        Sutherland Hodgman Polygon Clipping Algorithm
        returns clipped polygon to the rectangle defined by the lines
        x = min_x, y = min_y, x = max_x, y = max_y
        """
        clipped_polygon = self.clip_min_x(min_x).clip_min_y(min_y).clip_max_x(max_x).clip_max_y(max_y)
        return clipped_polygon if len(clipped_polygon.vertices) > 2 else None

