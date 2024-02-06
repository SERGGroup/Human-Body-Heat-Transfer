import math

class Body:
    def __init__(self, height=1.80, weight=76, gender=1, age=25, T_amb=288, v_air=0.1):
        self.height = height    #[m]
        self.weight = weight    #[kg]
        self.gender = gender    #[male=1; female=0]
        self.age = age
        self.T_amb = T_amb  #[K]
        self.v_air = v_air  #[m/s]

    def Dubois_surface(self):
        return 0.202*(self.weight**0.425)*(self.height**0.725)




