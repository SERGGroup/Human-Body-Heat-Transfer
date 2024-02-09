import math
class CylinderGeometry:
    def __init__(self, d, h, s):
        self.d = d  #[m]
        self.h = h  #[m]
        self.s = s  #[m]
        self.r = self.d/2    #[m]

    def calculate_area(self):
        return(2*math.pi * self.r *self.h) + (2*math.pi * self.r**2)    #[m^2]

    def calculate_volume(self):
        return math.pi*self.r**2*self.h    #[m^3]

