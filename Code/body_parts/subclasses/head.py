from Code.body_parts.cylinder_model import Cylinder


class Head(Cylinder):
    def __init__(self, d, h):

        super().__init__(d, h)

        self.prev=prev
        self.hr = 4.1
        self.hc = 3.6
        self.he = 5.9
        self.doppio = 0
        self.eps= 1
        self.Tint = 311.5
        self.Tar= 310.5
        self.v_dot_bl = 0.75
