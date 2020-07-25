from math import atan2 as arctan
from math import sqrt, sin, cos, tan, pi


def get_point_coordinate(dxy, dz, x, y, z, px, py, pz, fovd, w, h, b=0.01):
    """Returns the pixel coordinates of a cartesian point which is not behind player, returns None otherwise."""
    xx, yy, zz = px - x, py - y, pz - z

    def ry(a, x, y, z):
        """Rotates a cartesian point wrt y axis."""
        return z * sin(a) + x * cos(a), y, z * cos(a) - x * sin(a)

    def rz(a, x, y, z):
        """Rotates a cartesian point wrt z axis."""
        return x * cos(a) - y * sin(a), x * sin(a) + y * cos(a), z

    def rda(dxy, dz, sx, sy, sz):
        """Returns relative angles of a cartesian vector according to given spherical angles."""
        x, y, z = sx, sy, sz
        x, y, z = rz(-dxy, x, y, z)
        x, y, z = ry(dz, x, y, z)
        az = arctan(z, sqrt(x ** 2 + y ** 2))
        axy = arctan(y, x)
        return axy, az

    def sctopix(axy, az, fovd, w, h):
        """Converts angle info to pixel coordinates taking into consideration fov."""
        if -pi / 2 + b < axy < pi / 2 - b and -pi / 2 + b < az < pi / 2 - b:
            pixel_x, pixel_y = round(-fovd * tan(axy)), round(-fovd * tan(az) / cos(axy))
            return w + pixel_x, h + pixel_y

    axy, az = rda(dxy, dz, xx, yy, zz)
    return sctopix(axy, az, fovd, w, h)


def get_segment_coordinate(dxy, dz, x, y, z, sp1x, sp1y, sp1z, sp2x, sp2y, sp2z, fovd, w, h):
    """Returns pixel coordinates of segment endpoints if both are not behind player."""
    f1 = get_point_coordinate(dxy, dz, x, y, z, sp1x, sp1y, sp1z, fovd, w, h)
    f2 = get_point_coordinate(dxy, dz, x, y, z, sp2x, sp2y, sp2z, fovd, w, h)
    if f1 and f2:
        return f1[0], f1[1], f2[0], f2[1]


def angles_to_mouse(mx, my, fovd, w, h):
    """Returns appropriate rotation according to mouse position."""
    u, v = w - mx, h - my
    alpha = arctan(u, fovd)
    beta = arctan(v, sqrt(u**2 + fovd**2))
    return alpha, beta
