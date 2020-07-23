from math import atan2 as arctan
from math import sqrt, sin, cos, tan, pi


# to calculate pixel coordinates of a 3d point with cartesian coordinates
# according to player position (in cartesian) and direction (in spherical), and fov distance
# it returns None when the point is behind the player in order to avoid undesired images
def get_point_coordinate(dxy, dz, x, y, z, px, py, pz, fovd, w, h, b=0.01):
    xx, yy, zz = px - x, py - y, pz - z

    def ry(a, x, y, z):
        return z * sin(a) + x * cos(a), y, z * cos(a) - x * sin(a)

    def rz(a, x, y, z):
        return x * cos(a) - y * sin(a), x * sin(a) + y * cos(a), z

    def rda(dxy, dz, sx, sy, sz):
        x, y, z = sx, sy, sz
        x, y, z = rz(-dxy, x, y, z)
        x, y, z = ry(dz, x, y, z)
        az = arctan(z, sqrt(x ** 2 + y ** 2))
        axy = arctan(y, x)
        return axy, az

    def sctopix(axy, az, fovd, w, h):
        if -pi / 2 + b < axy < pi / 2 - b and -pi / 2 + b < az < pi / 2 - b:
            pixel_x, pixel_y = round(-fovd * tan(axy)), round(-fovd * tan(az) / cos(axy))
            return w + pixel_x, h + pixel_y

    axy, az = rda(dxy, dz, xx, yy, zz)
    return sctopix(axy, az, fovd, w, h)


# to calculate pixel coordinates of the endpoints of a segment
def get_segment_coordinate(dxy, dz, x, y, z, sp1x, sp1y, sp1z, sp2x, sp2y, sp2z, fovd, w, h):
    f1 = get_point_coordinate(dxy, dz, x, y, z, sp1x, sp1y, sp1z, fovd, w, h)
    f2 = get_point_coordinate(dxy, dz, x, y, z, sp2x, sp2y, sp2z, fovd, w, h)
    if f1 and f2:
        return f1[0], f1[1], f2[0], f2[1]


# to calculate changes in direction angles while the mouse cursor is moving
def angles_to_mouse(mx, my, fovd, w, h):
    u, v = w - mx, h - my
    alpha = arctan(u, fovd)
    beta = arctan(v, sqrt(u**2 + fovd**2))
    return alpha, beta