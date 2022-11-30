from Code.body_parts.cylinder_model import Cylinder

class Trunk(Cylinder):
    def __init__(self, d, h, body):

        super().__init__(d, h, body)

        self.hr = 4.4
        self.hc = 3.2
        self.he = 5.3
        self.doppio = 0
        self.eps= 1
        self.Tint = 310.15
        self.v_dot_bl = 1.73

    def H_res(self):

        return self.body.H_res() * 0.30