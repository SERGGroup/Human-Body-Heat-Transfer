
class Body:
    def __init__(
            self,
            height: float = 1.73,
            weight: float = 76,
            gender: bool = 1,
            age: float = 25,
            T_skin: float = 273.15 + 36.85,
            T_cl: float = 273.15 + 33.85):
        self.height = height    # [m]
        self.weight = weight    # [kg]
        self.gender = gender    # [male=1; female=0]
        self.age = age
        self.T_skin = T_skin
        self.T_cl = T_cl

    def DuBois_surface(self):
        return 0.202*(self.weight**0.425)*(self.height**0.725)  # [m^2]
