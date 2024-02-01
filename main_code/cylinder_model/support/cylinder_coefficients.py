from main_code.body_class import Body
class CylinderCoefficients:
    def __init__(self, body: Body, k_skin=0.3,cp_skin=3500,f_cl=0.70,epsilon_skin = 0.95,sigma=5.67*(10**(-8)) ):
        self.body = body
        self.k_skin =k_skin   #[W/m*K]; thermal conductivity coefficient
        self.cp_skin = cp_skin  #[j/Kg*K]; specific heat of the skin
        self.f_cl = f_cl    #coefficient to calculate real irradius area
        self.epsilon_skin = epsilon_skin
        self.sigma = sigma  #[W/m^2*K^4]

    def calculate_hc(self):
        if self.body.v_air < 0.2:
            h_c = 3.1   #[W/m^2*K]
        else:
            h_c = 8.3*(self.body.v_air**0.6)
        return h_c









