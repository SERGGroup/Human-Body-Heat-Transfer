class Body:
    def __init__(self, height=1.80, weight=76,gender=1,age=25,total_area= 1.8,T_amb=293, v_air = 1.5 ):
        self.height = height    #[m]
        self.weight = weight    #[kg]
        self.gender = gender    #[male=1 ; female=0]
        self.age = age  #[dimensionless]
        self.total_area = total_area    #[m^2]
        self.T_amb = T_amb  #[K]
        self.v_air = v_air  #[m/s]