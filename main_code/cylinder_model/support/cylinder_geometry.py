import math


class CylinderGeometry:
    def __init__(self, d: float, h: float, s: float):
        self.d = d  # diameter [m]
        self.h = h  # height [m]
        self.s = s  # [m]
        self.r = self.d / 2  # radius [m]

    def calculate_area(self) -> float:
        return (2 * math.pi * self.r * self.h) + (2 * math.pi * self.r ** 2)  # [m^2]

    def calculate_volume(self) -> float:
        return math.pi * self.r ** 2 * self.h  # [m^3]


