from main_code.body_class import Body
from main_code.cylinder_model.support.environmental_conditions import EnvironmentalConditions
# from main_code.cylinder_model.cylinder import Cylinder


class CylinderCoefficients:
    def __init__(
            self,
            body: Body,
            environmental_conditions: EnvironmentalConditions,
            # cylinder: Cylinder,
            f_cl: float = 0.70):

        self.body = body
        self.environmental_conditions = environmental_conditions
        # self.cylinder = cylinder
        self.f_cl = f_cl  # coefficient to calculate real irradius area

    # @staticmethod
    def get_k_skin(self) -> float:
        return 0.3  # [W/(m*K)]; thermal conductivity coefficient

    # @staticmethod
    def get_cp_skin(self) -> float:
        return 3500  # [J/(kg*K)]; specific heat of the skin

    # @staticmethod
    def get_epsilon_skin(self) -> float:
        return 0.95

    # @staticmethod
    def get_sigma(self) -> float:
        return 5.67 * (10 ** (-8))  # [W/(m^2-K^4)]

    def calculate_hc(self) -> float:  # i only make the conditions for a seated body
        if self.environmental_conditions.v_air < 0.2:
            h_c: float = 3.1
        elif 0.2 <= self.environmental_conditions.v_air < 4:
            h_c = 8.3 * (self.environmental_conditions.v_air ** 0.6)
        else:
            h_c = 0
        return h_c  # [W/m^2*K]

    # @staticmethod
    def get_LR(self) -> float:
        return 0.0165  # [K/Pa] = 16.5 [K/kPa]; Lewis ratio

    def calculate_he(self) -> float:
        return self.get_LR() * self.calculate_hc()  # [W/(m^2*Pa)]

    # @staticmethod
    def get_R_e_cl(self) -> float:
        return 0.7858  # [(m^2*Pa)/W]; evaporate heat transfer resistence of clothing

    # @staticmethod
    def get_w_diff(self) -> float:
        return 0.06  # skin wettedness by diffusion]

    # @staticmethod
    def get_w(self) -> float:
        return 0.25  # skin wettedness

    def calculate_R_e_t(self) -> float:
        return self.get_R_e_cl() + (1 / (self.calculate_he() * self.f_cl))  # [(m^2*Pa)/W]; total evaporate resistance

    # def get_volumetric_bood_rate(self):
    #     return ((10*self.cylinder.T_int)+(1*self.body.T_skin))/60000000 #[m^3/s]: correlation founded in an article on the internet
    #
    # def get_rho_blood(self):
    #     return 1050  # [Kg/m^3]; assuming blood is an incompressible fluid
    #
    # def calculate_mass_blood_rate(self):
    #     return self.get_rho_blood() * self.get_volumetric_bood_rate()  # [Kg/s]
    #
    # def get_blood_delta_P(self):
    #     return 16000  # [Pa]
    #
    # def calculate_blood_delta_h(self):  # dH = Cv*dT + V*dP ;assuming an isotermal increase of pressure
    #     return (self.get_rho_blood()) ** (-1) * self.get_blood_delta_P()  # [J/Kg]
    #
    # def efficiency_pump(self):
    #     return 0.25


