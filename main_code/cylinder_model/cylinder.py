import math
from .support import CylinderGeometry
from .support import CylinderCoefficients
from .support import EnvironmentalConditions
from main_code.body_class import Body

class Cylinder:
    def __init__(self,
                 geometry: CylinderGeometry, body: Body,coefficients: CylinderCoefficients,environmental_conditions: EnvironmentalConditions,
                 T_int=309, internal_heat_source=100):
        self.environmental_conditions = environmental_conditions
        self.geometry = geometry
        self.body = body
        self.coefficients = coefficients
        self.T_int = T_int  #[K]
        self.internal_heat_source = internal_heat_source  #[W]

    def delta_T(self):
        return self.T_int - self.environmental_conditions.temperature    #[K]

    def Q_cond(self):
        return 2*math.pi*self.geometry.h*self.coefficients.get_k_skin()*self.delta_T()/math.log((self.geometry.d+self.geometry.s)/(self.geometry.d))    #[W]

    def Q_conv(self):
        return self.coefficients.calculate_hc()*self.geometry.calculate_area()*self.delta_T()   #[W]

    def Q_irr(self):
        return self.coefficients.get_sigma()*self.geometry.calculate_area()*self.coefficients.get_epsilon_skin()*self.coefficients.f_cl*(self.T_int**4-self.environmental_conditions.temperature**4)  #[W]

    def W(self):
        return 0

    def energy_balance(self, delta_t, max_steps=1000):  # M - W = Q_cond + Q_conv + Q_irr
        q_cond = self.Q_cond()
        q_conv = self.Q_conv()
        q_irr = self.Q_irr()
        w = self.W()
        balance = self.internal_heat_source - w - q_cond - q_conv - q_irr
        self.T_int += (balance * delta_t) / (self.body.weight * self.coefficients.get_cp_skin())
        return self.T_int

    def dissipated_energy_watt(self):
        q_cond = self.Q_cond()
        q_conv = self.Q_conv()
        q_irr = self.Q_irr()
        w = self.W()
        return q_cond+q_conv+q_irr+w

    def dissipated_energy_joule(self,delta_t):
        q_cond = self.Q_cond()
        q_conv = self.Q_conv()
        q_irr = self.Q_irr()
        w = self.W()
        return (q_cond+q_conv+q_irr+w)*delta_t


















