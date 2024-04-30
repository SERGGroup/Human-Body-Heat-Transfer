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
                 T_int: float = 309, internal_heat_source: float = 100):
        self.environmental_conditions = environmental_conditions
        self.geometry = geometry
        self.body = body
        self.coefficients = coefficients
        self.T_int = T_int  # [K]
        self.internal_heat_source = internal_heat_source  # [W]

    def delta_T(self) -> float:
        return self.T_int - self.environmental_conditions.temperature  # [K]

    def Q_cond(self) -> float:
        return 2 * math.pi * self.geometry.h * self.coefficients.get_k_skin() * self.delta_T() / math.log(
            (self.geometry.d + self.geometry.s) / self.geometry.d)  # [W]

    def Q_conv(self) -> float:
        return self.coefficients.calculate_hc() * self.geometry.calculate_area() * self.delta_T()  # [W]

    def Q_irr(self) -> float:
        return (self.coefficients.get_sigma() * self.geometry.calculate_area() * self.coefficients.get_epsilon_skin()
                * self.coefficients.f_cl * (self.T_int ** 4 - self.environmental_conditions.temperature ** 4))  # [W]

    def E_sk(self) -> float:
        P_s_sk = self.environmental_conditions.get_properties()['Water Vapor Pressure Skin']
        P_s = self.environmental_conditions.get_properties()['Water Vapor Pressure']
        E_sk = self.coefficients.get_w() * (P_s_sk - P_s) * (
                1 / self.coefficients.calculate_R_e_t()) * self.body.DuBois_surface()  # [W]
        return E_sk


    def get_volumetric_blood_rate(self) -> float:
        return ((10 * self.T_int) + (
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

    def energy_balance(self, delta_t: float) -> float:  # M - W = Q_cond + Q_conv + Q_irr + E_sk + Q_blood
        q_cond = self.Q_cond()
        q_conv = self.Q_conv()
        q_irr = self.Q_irr()
        # w = self.W_pump_blood()
        e_sk = self.E_sk()
        q_blood = self.Q_blood()
        balance = self.internal_heat_source - (q_cond + q_conv + q_irr + e_sk + q_blood)

        # Update T_int
        self.T_int += (balance * delta_t) / (self.body.weight * self.coefficients.get_cp_skin())
        # Check T_int --> 18 < T_int < 43 °C
        if not (18 + 273.15 <= self.T_int <= 43 + 273.15):
            raise ValueError("Error: The value of T_int is outside the allowed range (18C - 45C)")

        return self.T_int

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
