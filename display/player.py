from math import sqrt, sin, cos
from core.world import WorldPoint
from core.rotation import Rotation

class Player:
    G = 9.81
    VV = 5.0
    def __init__(self):
        self.velocity = 4.0
        self.sensitivity = 2.0
        self.moving = False
        self.rotating = False
        self.jumping = False
        self.vertical_velocity = Player.VV

    def rotate(self, horizontal, vertical, dt):
        """
        horizontal is horizontal mouse movement
        vertical is vertical mouse movement
        dt is delta time
        returns delta rotation
        """
        self.rotating = horizontal != 0 or vertical != 0
        return Rotation(-horizontal * self.sensitivity * dt, -vertical * self.sensitivity * dt)

    def move(self, lr, ud, dt, rotation_xy):
        """
        lr is -1, 0, 1 for right, no movement, left
        ud is -1, 0, 1 for forward, no movement, backward
        dt is delta time
        rotation_xy is the xy plane rotation of the camera
        returns delta movement
        """
        if lr == 0 and ud == 0:
            # no movement
            self.moving = False
            return WorldPoint(0, 0, 0)
        
        self.moving = True
        distance = self.velocity * dt / sqrt(lr ** 2 + ud ** 2)
        s, c = sin(rotation_xy), cos(rotation_xy)
        dx = c * ud - s * lr
        dy = s * ud + c * lr
        return WorldPoint(dx * distance, dy * distance, 0)
    
    def end_jump(self):
        self.jumping = False
        self.vertical_velocity = Player.VV

    def jump(self, space, dt):
        if self.jumping:
            self.vertical_velocity -= dt * 9.81
            return WorldPoint(0, 0, dt * self.vertical_velocity)
        else:
            if space:
                self.jumping = True
                self.vertical_velocity -= dt * 9.81
                return WorldPoint(0, 0, dt * self.vertical_velocity)
            else:
                return WorldPoint(0, 0, 0)
