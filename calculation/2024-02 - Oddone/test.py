import CoolProp.CoolProp as CP
import math

class Body:
    def __init__(self, height=1.80, weight=76, gender=1, age=25, T_skin=310, T_cl=307):
        self.height = height    #[m]
        self.weight = weight    #[kg]
        self.gender = gender    #[male=1; female=0]
        self.age = age
        self.T_skin = T_skin
        self.T_cl = T_cl

    def Dubois_surface(self):
        return 0.202*(self.weight**0.425)*(self.height**0.725)  #[m^2]

class EnvironmentalConditions:
    def __init__(self, temperature=298, pressure=101325, humidity=0.60,v_air = 0.6, properties=None, fluid='water'):
        self.fluid = fluid
        self.temperature = temperature
        self.pressure = pressure
        self.humidity = humidity
        self. properties = properties
        self.v_air = v_air

    def set_conditions(self,temperature,pressure,humidity):
        self.temperature = temperature
        self.pressure = pressure
        self.humidity = humidity

    def calculate_properties(self):
        density = CP.PropsSI('D', 'T', self.temperature , 'P', self.pressure , self.fluid)
        enthalpy = CP.PropsSI('H', 'T', self.temperature , 'P', self.pressure , self.fluid)
        entropy = CP.PropsSI('S', 'T', self.temperature, 'P', self.pressure, self.fluid)
        specific_heat = CP.PropsSI('C', 'T', self.temperature, 'P', self.pressure, self.fluid)
        dynamic_viscosity = CP.PropsSI('V', 'T', self.temperature, 'P', self.pressure, self.fluid)
        thermal_conductivity = CP.PropsSI('L', 'T', self.temperature, 'P', self.pressure, self.fluid)

        self.properties={
            'Temperature': self.temperature
            , 'Pressure': self.pressure
            , 'Humidity': self.humidity
            , 'Density': density
            , 'Enthalpy': enthalpy
            , 'Entropy': entropy
            , 'Specific Heat': specific_heat
            , 'Dynamic Viscosity': dynamic_viscosity
            , 'Thermal Conductivity': thermal_conductivity
        }

    def get_properties(self):
        return self.properties


class CylinderGeometry:
    def __init__(self, d, h, s):
        self.d = d  #[m]
        self.h = h  #[m]
        self.s = s  #[m]
        self.r = self.d/2    #[m]

    def calculate_area(self):
        return(2*math.pi * self.r *self.h) + (2*math.pi * self.r**2)    #[m^2]

    def calculate_volume(self):
        return math.pi*self.r**2*self.h    #[m^3]

class CylinderCoefficients:
    def __init__(self, body: Body, environmental_conditions: EnvironmentalConditions, f_cl=0.70 ):
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

    def calculate_hc(self):
        if self.environmental_conditions.v_air < 0.2:
            h_c = 3.1
        elif 0.2<= self.environmental_conditions.v_air < 4:
            h_c = 90
        else:
            h_c = 0
        return h_c

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

#TRY CODE
tommaso_env_conditions = EnvironmentalConditions()
tommaso_env_conditions.set_conditions(temperature=288, pressure = 101325, humidity = 0.5)
tommaso = Body()
coefficent_cylinder = CylinderCoefficients(tommaso,tommaso_env_conditions)
geometry_cylinder = CylinderGeometry(d=0.2, h=0.61, s=0.2)
trunk = Cylinder(geometry_cylinder, tommaso, coefficent_cylinder, tommaso_env_conditions)
h_c_value = trunk.coefficients.calculate_hc()
print(h_c_value)



