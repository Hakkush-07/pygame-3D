class Rotation:
    def __init__(self, alpha, beta):
        """
        rotation
        alpha: rotation in xy plane (0 means +x, pi/2 means +y while beta is 0)
        beta: rotation up and down (0 means ahead, pi/2 means up, -pi/2 means down)
        """
        self.alpha = self.a = alpha
        self.beta = self.b = beta
    
    def __repr__(self):
        return f"Rotation({self.a}, {self.b}))"
    
    def __add__(self, other):
        return Rotation(self.a + other.a, self.b + other.b)

    def __iadd__(self, other):
        return self + other
