from Code.body_parts.cylinder_model import Cylinder

class Arm(Cylinder):
    def __init__(self, d, h, body, prev):

        super().__init__(d, h, body, prev)

        self.prev= prev
        self.hr = 5.2
        self.hc = 2.9
        self.he = 4.8
        self.doppio = 1
        self.eps= 0.92
        self.Tint = 309.5
        self.v_dot_bl = 0.21
