
class Body:
    def __init__(self, height=1.80, weight=76, gender=1, age=25, T_skin=310, T_cl=307):
        self.height = height    # [m]
        self.weight = weight    # [kg]
        self.gender = gender    # [male=1; female=0]
        self.age = age
        self.T_skin = T_skin
        self.T_cl = T_cl

    def Dubois_surface(self):
        return 0.202*(self.weight**0.425)*(self.height**0.725)  # [m^2]
