from Code.body_parts.cylinder_model import Cylinder

class Neck(Cylinder):
    def __init__(self, d, h, body, prev):

        super().__init__(d, h, body, prev)

        self.prev= prev
        self.hr = 4.1
        self.hc = 3.6
        self.he = 5.9
        self.doppio = 0
        self.eps = 1
        self.Tint = 310.5
        self.v_dot_bl = 0.75

    def H_res(self):
        return self.body.H_res() * 0.25