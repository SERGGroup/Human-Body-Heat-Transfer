import math
from CoolProp.CoolProp import PropsSI
from .support import CylinderGeometry
from .support import CylinderCoefficients
from .support import EnvironmentalConditions
from main_code.body_class import Body


class Cylinder:
    def __init__(self,
                 geometry: CylinderGeometry,
                 body: Body,
                 coefficients: CylinderCoefficients,
                 environmental_conditions: EnvironmentalConditions,
                 # T_int: float = 309,
                 # internal_heat_source: float = 100,
                 # work: float = 0
                 ):
        self.environmental_conditions = environmental_conditions
        self.geometry = geometry
        self.body = body
        self.coefficients = coefficients
        # self.T_int = T_int  # [K]
        # self.internal_heat_source = internal_heat_source  # [W]
        # self.work = work
        self.K_res = 1.43E-6  # metabolic proportionality constant [kg/J]

    def delta_T(self) -> float:
        return self.body.T_int - self.environmental_conditions.temperature  # [K]

    def calculate_Tcl(self) -> float:
        net_energy = self.environmental_conditions.M_act() - self.body.work
        return (35.7 - 0.275 * net_energy - self.coefficients.get_R_cl() * net_energy -
                3.05 * (5.73E3 * 0.007 * net_energy - self.environmental_conditions.pressure) -
                0.42 * net_energy * 58.15 * self.body.DuBois_surface() +
                0.0173 * self.environmental_conditions.M_act() * (5.87E3 - self.environmental_conditions.pressure) -
                - 0.0014 * self.environmental_conditions.M_act() * (34 - self.environmental_conditions.temperature -
                                                                    self.environmental_conditions.ABSOLUTE_ZERO))

    def Q_cond(self) -> float:
        return (2 * math.pi * self.geometry.h * self.coefficients.get_k_skin() *
                (self.body.T_skin - self.environmental_conditions.temperature) / math.log(
                    (self.geometry.d + self.geometry.s) / self.geometry.d))  # [W]

    def Q_conv(self) -> float:
        # return self.coefficients.calculate_hc() * self.geometry.calculate_area() * self.delta_T()  # [W]
        return self.coefficients.calculate_fcl() * self.coefficients.calculate_hc() * self.geometry.calculate_area() * \
            (self.body.T_cl - self.environmental_conditions.temperature)  # [W]

    def Q_irr(self) -> float:
        return (self.coefficients.get_sigma() * self.geometry.calculate_area() * self.coefficients.get_epsilon_skin()
                * self.coefficients.calculate_fcl() * (
                        self.body.T_int ** 4 - self.environmental_conditions.temperature ** 4))  # [W]

        # return self.coefficients.calculate_fcl() * self.coefficients.calculate_hr() * \
        #     (self.body.T_cl - self.coefficients.get_T_mr())

    # def get_Qconv_Qirr(self) -> float:
    #     return (self.body.T_skin - self.get_to()) / self.coefficients.

    def E_sk(self) -> float:
        P_s_sk = self.environmental_conditions.get_properties()['Water Vapor Pressure Skin']
        P_s = self.environmental_conditions.get_properties()['Water Vapor Pressure']
        E_sk = (self.coefficients.get_w() *
                (P_s_sk - P_s) /
                (self.coefficients.get_R_e_cl() + 1 / (self.coefficients.calculate_fcl()
                                                       * self.coefficients.calculate_he()))
                * self.geometry.calculate_area())  # [W]
        return E_sk

    def get_volumetric_blood_rate(self) -> float:
        return ((10 * self.body.T_int) + (
                1 * self.body.T_skin)) / 60000000  #[m^3/s]: correlation found in an article on the internet

    # @staticmethod
    def get_rho_blood(self) -> float:
        return 1050  # [Kg/m^3]; assuming blood is an incompressible fluid

    def calculate_mass_blood_rate(self) -> float:
        return self.get_rho_blood() * self.get_volumetric_blood_rate()  # [kg/s]

    # @staticmethod
    def get_blood_delta_P(self) -> float:
        return 16000  # [Pa]

    def calculate_blood_delta_h(self) -> float:  # dH = Cv*dT + V*dP ;assuming an isothermal increase of pressure
        return (self.get_rho_blood()) ** (-1) * self.get_blood_delta_P()  # [J/kg]

    # @staticmethod
    def efficiency_pump(self) -> float:
        return 0.25

    def Q_blood(self) -> float:
        return self.calculate_blood_delta_h() * self.calculate_mass_blood_rate()  # [W];  # power associated with kinetic energy of the flow

    def W_pump_rev_blood(self) -> float:
        return self.calculate_mass_blood_rate() * (
                1 / self.get_rho_blood()) * self.get_blood_delta_P()  # [W]

    def W_pump_blood(self) -> float:
        return self.W_pump_rev_blood() / self.efficiency_pump()  # [W]

    def calculate_m_res(self) -> float:
        return self.K_res * self.body.internal_heat_source * self.body.DuBois_surface()  # [kg/s]

    def calculate_m_w_res(self) -> float:
        return self.calculate_m_res() * (self.environmental_conditions.get_properties()['Humidity Ratio Exhaled']
                                         - self.environmental_conditions.get_properties()['Humidity Ratio'])  # [kg/s]

    def C_res(self) -> float:
        return 1.4E-3 * self.body.internal_heat_source * (34 - (self.environmental_conditions.temperature - 273.15))

    def E_res(self) -> float:
        return 1.73E-2 * self.body.internal_heat_source * (
                5.87E3 - self.environmental_conditions.get_properties()['Water Vapor Pressure'])

    def calculate_T_ex(self) -> float:
        return (32.6 + 0.066 * (self.environmental_conditions.temperature - 273.15) +
                32 * self.environmental_conditions.get_properties()['Humidity Ratio'])

    def Q_res(self) -> float:
        # return self.C_res() + self.E_res()
        return (self.calculate_m_res() * (self.environmental_conditions.get_properties()['Enthalpy Exhaled'] -
                                          self.environmental_conditions.get_properties()['Enthalpy Inhaled']) +
                self.calculate_m_w_res() * self.environmental_conditions.get_properties()['Specific Heat'] *
                (self.calculate_T_ex() - (self.environmental_conditions.temperature - 273.15)))       # [W]

    def Delta_H_blood(self):

    # def W(self) -> float:
    #     return self.body.work

    # def BMI(self) -> float:
    #     return self.body.weight / (self.body.height ** 2)
    #
    # def BF(self) -> float:
    #     if self.body.gender:
    #         if 20 <= self.body.age <= 39:
    #             return (0.19 - 0.08) / (39 - 20) * (self.body.age - 20) + 0.08
    #         elif 40 <= self.body.age <= 59:
    #             return (0.21 - 0.11) / (59 - 40) * (self.body.age - 40) + 0.11
    #         elif 60 <= self.body.age <= 79:
    #             return (0.24 - 0.13) / (79 - 60) * (self.body.age - 60) + 0.13
    #     else:
    #         if 20 <= self.body.age <= 39:
    #             return (0.32 - 0.21) / (39 - 20) * (self.body.age - 20) + 0.21
    #         elif 40 <= self.body.age <= 59:
    #             return (0.33 - 0.23) / (59 - 40) * (self.body.age - 40) + 0.23
    #         elif 60 <= self.body.age <= 79:
    #             return (0.35 - 0.24) / (79 - 60) * (self.body.age - 60) + 0.24
    #     # return 1.39 * self.BMI() + 0.16 * self.body.age - 10.8 * self.body.gender - 9
    #
    # def M_shiv(self) -> float:
    #     if (37 - (self.body.T_int - 273.15)) > 0:
    #         T_int_ = (37 - (self.body.T_int - 273.15))
    #     else:
    #         T_int_ = 0
    #     if (33 - (self.body.T_skin - 273.15)) > 0:
    #         T_skin_ = (33 - (self.body.T_skin - 273.15))
    #     else:
    #         T_skin_ = 0
    #     return (155.5 * T_int_ + 47.0 * T_skin_ - 1.57 * (T_skin_ ** 2)) / (self.BF() ** 0.5)

    def energy_balance(self, delta_t: float) -> float:  # M - W = Q_cond + Q_conv + Q_irr + E_sk + Q_blood
        q_cond = self.Q_cond()
        q_conv = self.Q_conv()
        q_irr = self.Q_irr()
        # w = self.W_pump_blood()
        e_sk = self.E_sk()
        q_blood = self.Q_blood()
        q_res = self.Q_res()
        balance = self.body.internal_heat_source - (q_cond + q_conv + q_irr + e_sk + q_blood + q_res)

        # Update T_int
        self.body.T_int += (balance * delta_t) / (self.body.weight * self.coefficients.get_cp_skin())
        # Check T_int --> 28 < T_int < 45 °C
        # if not (28 + 273.15 <= self.T_int <= 45 + 273.15):
        #     raise ValueError("Error: The value of T_int is outside the allowed range (18C - 45C)")

        return self.body.T_int

    def dissipated_energy_watt(self) -> float:
        q_cond = self.Q_cond()
        q_conv = self.Q_conv()
        q_irr = self.Q_irr()
        w = self.W()
        return q_cond + q_conv + q_irr + w

    def dissipated_energy_joule(self, delta_t: float) -> float:
        q_cond = self.Q_cond()
        q_conv = self.Q_conv()
        q_irr = self.Q_irr()
        w = self.W()
        return (q_cond + q_conv + q_irr + w) * delta_t
