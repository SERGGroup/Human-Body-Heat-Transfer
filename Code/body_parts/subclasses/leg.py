from Code.body_parts.cylinder_model import Cylinder

class Leg(Cylinder):
    def __init__(self, d, h, body, prev):
        super().__init__(d, h, body, prev)

        self.prev = prev
        self.hr = 5.3
        self.hc = 4.1
        self.he = 6.8
        self.doppio = 1
        self.eps = 0.92
        self.Tint = 309
        self.v_dot_bl = 0.28