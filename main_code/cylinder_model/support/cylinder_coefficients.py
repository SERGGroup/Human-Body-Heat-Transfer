from main_code.body_class import Body
from main_code.cylinder_model.support.environmental_conditions import EnvironmentalConditions
class CylinderCoefficients:
    def __init__(self, body: Body,environmental_conditions: EnvironmentalConditions,f_cl=0.70 ):
        self.body = body
        self.environmental_conditions = environmental_conditions
        self.f_cl = f_cl    #coefficient to calculate real irradius area

    def get_k_skin(self):
        return 0.3  #[W/m*K]; thermal conductivity coefficient

    def get_cp_skin(self):
        return 3500    #[j/Kg*K]; specific heat of the skin

    def get_epsilon_skin(self):
        return 0.95

    def get_sigma(self):
        return 5.67*(10**(-8))

    def calculate_hc(self): #for now i make only the seated conditions, when i'll define in body an attribute activity i'll make other conditions
        if self.environmental_conditions.v_air < 0.2:
            h_c = 3.1
        elif 0.2<= self.environmental_conditions.v_air < 4:
            h_c = 8.3*(self.environmental_conditions.v_air**0.6)
        else:
            h_c = 0
        return h_c









