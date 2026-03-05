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
        return 5.67E-8  # [W/(m^2-K^4)]

    def calculate_hc(self) -> float:  # i only make the conditions for a seated body
        if self.environmental_conditions.v_air < 0.2:
            h_c: float = 3.1
        elif 0.2 <= self.environmental_conditions.v_air < 4:
            h_c = 8.3 * (self.environmental_conditions.v_air ** 0.6)
        # else:
        #     h_c = 0
        return h_c  # [W/m^2*K]

    Ar_AD_ratio = {'sitting': 0.70, 'standing': 0.73}

    def calculate_hr(self) -> float:
        T_mr = self.environmental_conditions.calculate_T_mr(
            area_factor=self.environmental_conditions.calculate_area_factor(
                vector_a=self.environmental_conditions.get_vector_a(),
                vector_b=self.environmental_conditions.get_vector_b(),
                vector_c=self.environmental_conditions.get_vector_c(),
            ),
            T_surf=self.environmental_conditions.get_vector_T_surf())
        return 4 * self.get_epsilon_skin() * self.get_sigma() * self.Ar_AD_ratio['sitting'] * \
            (273.15 + (self.body.T_cl + T_mr - self.environmental_conditions.ABSOLUTE_ZERO) / 2) ** 3
        # return 4.7 * self.get_epsilon_skin()    # [W/(m^2*K)]

    def get_T_mr(self) -> float:
        return self.environmental_conditions.calculate_T_mr(
            area_factor=self.environmental_conditions.calculate_area_factor(
                vector_a=self.environmental_conditions.get_vector_a(),
                vector_b=self.environmental_conditions.get_vector_b(),
                vector_c=self.environmental_conditions.get_vector_c(),
            ),
            T_surf=self.environmental_conditions.get_vector_T_surf()) + self.environmental_conditions.ABSOLUTE_ZERO

    def get_h(self) -> float:
        return self.calculate_hc() + self.calculate_hr()

    def calculate_to(self) -> float:
        return (self.calculate_hr() * self.get_T_mr() +
                self.calculate_hc() * self.environmental_conditions.temperature) / self.get_h()

    def calculate_fcl(self) -> float:
        return (self.body.T_cl - self.calculate_to()) / (self.body.T_skin - self.calculate_to())
        # return 0.7

    # @staticmethod
    def get_LR(self) -> float:
        return 0.0165  # [K/Pa] = 16.5 [K/kPa]; Lewis ratio

    def calculate_he(self) -> float:
        return self.get_LR() * self.calculate_hc()  # [W/(m^2*Pa)]

    def get_R_cl(self):
        return 0.155 * 1.01    # 1 clo = 0.155 [m^2*K)/W] 1.01 = Trousers, long-sleeved shirt, longsleeved sweater, T-shirt

    # @staticmethod
    def get_R_e_cl(self) -> float:
        return 0.7858  # [(m^2*Pa)/W]; evaporate heat transfer resistence of clothing

    # @staticmethod
    def get_w_diff(self) -> float:
        return 0.06  # skin wettedness by diffusion]

    # @staticmethod
    def get_w(self) -> float:
        if self.environmental_conditions.temperature < 2.577 / 0.009:
            return 0.0
        elif 2.577 / 0.009 <= self.environmental_conditions.temperature < 303:
            return 0.009 * self.environmental_conditions.temperature - 2.577
        elif 303 <= self.environmental_conditions.temperature < 37.816 / 0.122:
            return 0.122 * self.environmental_conditions.temperature - 36.816
        else:
            return 1

    def calculate_R_e_t(self) -> float:
        return self.get_R_e_cl() + (1 / (self.calculate_he() * self.calculate_fcl()))  # [(m^2*Pa)/W]; total evaporate resistance

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
