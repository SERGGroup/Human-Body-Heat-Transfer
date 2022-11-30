from Code.body_parts.cylinder_model import Cylinder

class Foot(Cylinder):
    def __init__(self, d, h, body, prev):

        super().__init__(d, h, body, prev)

        self.prev=prev
        self.hr = 3.9
        self.hc = 5.1
        self.he = 8.4
        self.doppio = 1
        self.eps = 0.92
        self.Tint = 308.5
        self.v_dot_bl = 0.28