from CoolProp.CoolProp import PropsSI, HAPropsSI
import numpy as np
import math
from matplotlib import pyplot as plt

class Body:
    def __init__(self, height=1.80, weight=76, gender=1, age=25, T_skin=310, T_cl=307):
        self.height = height    # [m]
        self.weight = weight    # [kg]
        self.gender = gender    # [male=1; female=0]
        self.age = age
        self.T_skin = T_skin
        self.T_cl = T_cl

    def Dubois_surface(self):
        return 0.202*(self.weight**0.425)*(self.height**0.725)  # [m^2]

class EnvironmentalConditions:
    def __init__(self, body: Body, temperature=298, pressure=101325, humidity=0.50, v_air=0.6, properties=None,
                 fluid='water'):
        self.body = body
        self.fluid = fluid
        self.temperature = temperature
        self.pressure = pressure
        self.humidity = humidity
        self.properties = properties
        self.v_air = v_air

    def set_conditions(self, temperature, pressure, humidity):
        self.temperature = temperature
        self.pressure = pressure
        self.humidity = humidity

    def calculate_properties(self):
        density = PropsSI('D', 'T', self.temperature, 'P', self.pressure, self.fluid)
        enthalpy = PropsSI('H', 'T', self.temperature, 'P', self.pressure, self.fluid)
        entropy = PropsSI('S', 'T', self.temperature, 'P', self.pressure, self.fluid)
        specific_heat = PropsSI('C', 'T', self.temperature, 'P', self.pressure, self.fluid)
        dynamic_viscosity = PropsSI('V', 'T', self.temperature, 'P', self.pressure, self.fluid)
        thermal_conductivity = PropsSI('L', 'T', self.temperature, 'P', self.pressure, self.fluid)
        water_vapor_pressure = PropsSI('P', 'T', self.temperature, 'Q', 1, 'Water')
        water_vapor_pressure_skin = PropsSI('P', 'T', self.body.T_skin, 'Q', 1, 'Water')
        humidity_ratio = HAPropsSI('W', 'T', self.temperature, 'P', self.pressure, 'RH', self.humidity)
        wet_bulb_temperature = HAPropsSI('Twb', 'T', self.temperature, 'P', self.pressure, 'RH', self.humidity)
        water_vapor_pressure_37_degrees = PropsSI('P', 'T', 310.15, 'Q', 1, 'Water')

        self.properties = {
            'Temperature':                       self.temperature
            , 'Pressure':                        self.pressure
            , 'Humidity':                        self.humidity
            , 'Density':                         density
            , 'Enthalpy':                        enthalpy
            , 'Entropy':                         entropy
            , 'Specific Heat':                   specific_heat
            , 'Dynamic Viscosity':               dynamic_viscosity
            , 'Thermal Conductivity':            thermal_conductivity
            , 'Water Vapor Pressure':            water_vapor_pressure
            , 'Water Vapor Pressure Skin':       water_vapor_pressure_skin
            , 'Humidity Ratio':                  humidity_ratio
            , 'Wet Bulb Temperature':            wet_bulb_temperature
            , 'Water Vapor Pressure 37 degrees': water_vapor_pressure_37_degrees
        }

    def get_properties(self):
        return self.properties

    def get_vector_a(self):
        return np.array([0.5, 0.5, 3.5, 3.5, 3.5, 3.5])  # [up, down, left, right, front, back]

    def get_vector_b(self):
        return np.array([3.5, 3.5, 4.5, 4.5, 4.5, 4.5])

    def get_vector_c(self):
        return np.array([3.5, 0.5, 0.5, 4.5, 3.5, 0.5])

    def calculate_area_factor(self, vector_a, vector_b, vector_c):
        x_v = vector_a / vector_b
        y_v = vector_b / vector_c
        x_h = vector_c / vector_b
        y_h = vector_a / vector_b

        F_dv = (1 / (2 * np.pi)) * ((x_v / np.sqrt(1 + x_v ** 2)) * np.arctan(y_v / np.sqrt(1 + x_v ** 2)) + (
                y_v / np.sqrt(1 + y_v ** 2)) * np.arctan(x_v / np.sqrt(1 + y_v ** 2)))
        F_dh = (1 / (2 * np.pi)) * (np.arctan(1 / y_h) + (y_h / np.sqrt(x_h ** 2 + y_h ** 2)) * np.arctan(
            1 / np.sqrt(x_h ** 2 + y_h ** 2)))

        area_factor = []

        for i in range(len(vector_a)):
            if i < 2:
                area_factor.append(F_dv[i])
            else:
                area_factor.append(F_dh[i])

        return area_factor

    def get_vector_T_surf(self):
        return np.array([20, 18, 19, 20, 21.5, 22])  # wall temperatures

    def calculate_T_mr(self, area_factor, T_surf):
        return (np.sum(np.fromiter((T_surf[i] ** 4 * area_factor[i] for i in range(len(area_factor))), dtype=float)) /
                np.sum(np.fromiter((area_factor[i] for i in range(len(area_factor))), dtype=float))) ** (1 / 4)  # [°C]

    def get_inspired_air_composition(self):
        comp = {
            'pCO2': 0.03,  # %
            'pO2':  20.93,  # %
            'pN2':  79.04  # %
        }
        return comp

    def get_expired_air_composition(self):
        comp = {
            'pCO2': 3.60,  # %
            'pO2':  16.86,  # %
            'pN2':  79.54  # %
        }
        return comp

    def get_Pt_torr(self):
        return 760  # [Torr]; 760 [Torr] = 101325 [Pa]

    def get_V_atps(self):
        return 30  # [l]; volume of expired gas

    def calculate_V_st(self):
        return self.get_V_atps() * (273.15 / self.temperature)  # [l]; gas volume at standard temperature

    def calculate_V_sp(self):
        return self.get_V_atps() * (self.get_Pt_torr() / 760)  # [l]; gas volume at standard pressure

    def calculate_V_spd(self):
        water_vapor_pressure_torr = (self.properties['Water Vapor Pressure']) / 133.3  # [torr]
        return self.get_V_atps() * (
                    (self.get_Pt_torr() - water_vapor_pressure_torr) / 760)  # [l]; gas volume at standard pressure dry

    def get_water_vapor_pressure_at_37_degrees_torr(self):
        water_vapor_pressure_37_degrees = (self.properties['Water Vapor Pressure 37 degrees']) / 133.3  # [torr]
        return water_vapor_pressure_37_degrees  # [Torr]

    def calculate_V_stpd(self):
        water_vapor_pressure_torr = (self.properties['Water Vapor Pressure']) / 133.3  # [torr]
        return self.get_V_atps() * ((self.get_Pt_torr() - water_vapor_pressure_torr) / 760) * (
                    273.15 / self.temperature)  # [l]; gas volume

    def calculate_V_btps(self):
        water_vapor_pressure_torr = (self.properties['Water Vapor Pressure']) / 133.3  # [torr]
        water_vapor_pressure_37_degrees = (self.properties['Water Vapor Pressure 37 degrees']) / 133.3  # [torr]
        return (self.get_V_atps() * (310.15 / self.temperature)
                * ((self.get_Pt_torr() - water_vapor_pressure_torr) / (
                            self.get_Pt_torr() - water_vapor_pressure_37_degrees)))

    def get_V_e(self):
        return 26.483  # [l]; volume of expired air

    def calculate_V_i(self):
        comp_insp = self.get_inspired_air_composition()
        comp_exp = self.get_expired_air_composition()
        return (self.get_V_e() * (comp_exp['pN2'] / 100 * self.get_V_e())) / (
                    comp_insp['pN2'] / 100 * self.get_V_e())  # [l]; volume of inspired air

    def calculate_V_O2_i(self):
        comp_insp = self.get_inspired_air_composition()
        return comp_insp['pO2'] / 100 * self.calculate_V_i()  # [l]; volume of O2 in inspired air

    def calculate_VO2_e(self):
        comp_exp = self.get_expired_air_composition()
        return comp_exp['pO2'] / 100 * self.get_V_e()  # [l]; volume of O2 in expired air

    def calculate_VO2(self):
        return self.calculate_V_O2_i() - self.calculate_VO2_e()  # [l]; volume of O2 removed from inspired air

    def calculate_VCO2(self):
        comp_insp = self.get_inspired_air_composition()
        comp_exp = self.get_expired_air_composition()
        return (comp_exp['pCO2'] / 100 * self.get_V_e()) - (
                    comp_insp['pCO2'] / 100 * self.calculate_V_i())  # [l]; volume of carbon dioxide produced

    def get_Q_O2_for_minute(self):
        return self.calculate_VO2()

    def get_Q_CO2_for_minute(self):
        return self.calculate_VCO2()

    def calculate_RQ(self):
        return self.get_Q_CO2_for_minute() / self.get_Q_O2_for_minute()  # respiratory quotient

    def calculate_O2_true(self):
        comp_insp = self.get_inspired_air_composition()
        comp_exp = self.get_expired_air_composition()
        return ((comp_exp['pN2'] / 100) / (comp_insp['pN2'] / 100) * (comp_insp['pO2'] / 100)) - (
                    comp_exp['pO2'] / 100)  # percentage of O2 consumed for any volume of air expired

class CylinderGeometry:
    def __init__(self, d, h, s):
        self.d = d  # [m]
        self.h = h  # [m]
        self.s = s  # [m]
        self.r = self.d / 2  # [m]

    def calculate_area(self):
        return (2 * math.pi * self.r * self.h) + (2 * math.pi * self.r ** 2)  # [m^2]

    def calculate_volume(self):
        return math.pi * self.r ** 2 * self.h  # [m^3]

class CylinderCoefficients:
    def __init__(self, body: Body, environmental_conditions: EnvironmentalConditions, f_cl=0.70):
        self.body = body
        self.environmental_conditions = environmental_conditions
        self.f_cl = f_cl  # coefficient to calculate real irradius area

    def get_k_skin(self):
        return 0.3  # [W/m*K]; thermal conductivity coefficient

    def get_cp_skin(self):
        return 3500  # [j/Kg*K]; specific heat of the skin

    def get_epsilon_skin(self):
        return 0.95

    def get_sigma(self):
        return 5.67 * (10 ** (-8))  # [W/(m^2-K^4)]

    def calculate_hc(self):  # i only make the conditions for a seated body
        if self.environmental_conditions.v_air < 0.2:
            h_c = 3.1
        elif 0.2 <= self.environmental_conditions.v_air < 4:
            h_c = 8.3 * (self.environmental_conditions.v_air ** 0.6)
        else:
            h_c = 0
        return h_c  # [W/m^2*K]

    def get_LR(self):
        return 0.0165  # [K/Pa] = 16.5 [K/kPa]; Lewis ratio

    def calculate_he(self):
        return self.get_LR() * self.calculate_hc()  # [W/m^2*Pa]

    def get_R_e_cl(self):
        return 0.7858  # [(m^2*Pa)/W]; evaporate heat transfer resistence of clothing

    def get_w_diff(self):
        return 0.06  # skin wettedness by diffusion]

    def get_w(self):
        return 0.25  # skin wettedness

    def calculate_R_e_t(self):
        return self.get_R_e_cl() + (1 / (self.calculate_he() * self.f_cl))  # [(m^2*Pa)/W]; total evaporate resistance

    def get_volumetric_bood_rate(self):
        return 5 / 60000  # [m^3/s]; value finded on internet, for a full body

    def get_rho_blood(self):
        return 1050  # [Kg/m^3]; assuming blood is an incompressible fluid

    def calculate_mass_blood_rate(self):
        return self.get_rho_blood() * self.get_volumetric_bood_rate()  # [Kg/s]

    def get_blood_delta_P(self):
        return 16000  # [Pa]

    def calculate_blood_delta_h(self):  # dH = Cv*dT + V*dP ;assuming an isotermal increase of pressure
        return (self.get_rho_blood()) ** (-1) * self.get_blood_delta_P()  # [J/Kg]

    def efficiency_pump(self):
        return 0.25

class Cylinder:
    def __init__(self,
                 geometry: CylinderGeometry,
                 body: Body,
                 coefficients: CylinderCoefficients,
                 environmental_conditions: EnvironmentalConditions,
                 T_int=309, internal_heat_source=100):
        self.environmental_conditions = environmental_conditions
        self.geometry = geometry
        self.body = body
        self.coefficients = coefficients
        self.T_int = T_int  # [K]
        self.internal_heat_source = internal_heat_source  # [W]

    def delta_T(self):
        return self.T_int - self.environmental_conditions.temperature  # [K]

    def Q_cond(self):
        return 2 * math.pi * self.geometry.h * self.coefficients.get_k_skin() * self.delta_T() / math.log(
            (self.geometry.d + self.geometry.s) / self.geometry.d)  # [W]

    def Q_conv(self):
        return self.coefficients.calculate_hc() * self.geometry.calculate_area() * self.delta_T()  # [W]

    def Q_irr(self):
        return (self.coefficients.get_sigma() * self.geometry.calculate_area() * self.coefficients.get_epsilon_skin()
                * self.coefficients.f_cl * (self.T_int ** 4 - self.environmental_conditions.temperature ** 4))  # [W]

    def E_sk(self):
        P_s_sk = self.environmental_conditions.get_properties()['Water Vapor Pressure Skin']
        P_s = self.environmental_conditions.get_properties()['Water Vapor Pressure']
        E_sk = self.coefficients.get_w() * (P_s_sk - P_s) * (
                    1 / self.coefficients.calculate_R_e_t()) * self.body.Dubois_surface()  # [W]
        return E_sk

    def Q_blood(self):
        return self.coefficients.calculate_blood_delta_h() * self.coefficients.calculate_mass_blood_rate()  # [W];  # power associated with kinetic energy of the flow

    def W_pump_rev_blood(self):
        return self.coefficients.calculate_mass_blood_rate() * (
                    1 / self.coefficients.get_rho_blood()) * self.coefficients.get_blood_delta_P()  # [W]

    def W_pump_blood(self):
        return self.W_pump_rev_blood() / self.coefficients.efficiency_pump()  # [W]

    def energy_balance(self, delta_t):  # M - W = Q_cond + Q_conv + Q_irr + E_sk + Q_blood
        q_cond = self.Q_cond()
        q_conv = self.Q_conv()
        q_irr = self.Q_irr()
        # w = self.W_pump_blood()
        e_sk = self.E_sk()
        q_blood = self.Q_blood()
        balance = self.internal_heat_source - (q_cond + q_conv + q_irr + e_sk + q_blood)

        #Update T_int
        self.T_int += (balance * delta_t) / (self.body.weight * self.coefficients.get_cp_skin())
        #Check T_int --> 18 < T_int < 43 °C
        if not (18<= self.T_int <=43):
            print("Error: Il valore di T_int è al di fuori dell'intervallo consentito")

        return self.T_int

    def dissipated_energy_watt(self):
        q_cond = self.Q_cond()
        q_conv = self.Q_conv()
        q_irr = self.Q_irr()
        w = self.W()
        return q_cond + q_conv + q_irr + w

    def dissipated_energy_joule(self, delta_t):
        q_cond = self.Q_cond()
        q_conv = self.Q_conv()
        q_irr = self.Q_irr()
        w = self.W()
        return (q_cond + q_conv + q_irr + w) * delta_t

'''
TEST
'''
def simulate_temperature_evolution(cylinder, delta_t, max_steps=10):
    times = []
    temperatures = []
    q_cond_list = []

    current_time = 0
    while current_time < max_steps:
        times.append(current_time + delta_t)  # Tempo in secondi
        temperatures.append(cylinder.T_int)
        q_cond_list.append(cylinder.Q_cond())

        cylinder.energy_balance(delta_t)


        current_time += delta_t

    return times, temperatures, q_cond_list


# %% ----- OBJECT'S CREATION
tommaso = Body(height=1.80, weight=76, gender=1, age=25, T_skin=273.15 + 28, T_cl=273.15 + 25)
tommaso_env_conditions = EnvironmentalConditions(tommaso)
tommaso_env_conditions.set_conditions(temperature=273.15 + 0, pressure=101325, humidity=1)
tommaso_env_conditions.calculate_properties()
coefficient_cylinder = CylinderCoefficients(tommaso, tommaso_env_conditions)
geometry_cylinder = CylinderGeometry(d=0.2, h=0.8, s=0.2)
trunk = Cylinder(geometry_cylinder, tommaso, coefficient_cylinder, tommaso_env_conditions)

delta_t = 1  # Intervallo di tempo in secondi
times, temperatures, q_cond_list = simulate_temperature_evolution(trunk, delta_t, max_steps=60 * 60 * 24)

plt.plot(times, np.array(temperatures) - 273.15, linestyle='-')
plt.xticks(np.arange(0, len(times) + 1, step=60 * 60 * 2), labels=np.arange(0, 25, 2))
plt.xlabel('Time (hr)')
plt.ylabel('Internal Temperature ($\degree$C)')
plt.title('Change in internal temperature over time')
plt.grid(True)
plt.show()

plt.plot(times, np.array(q_cond_list), linestyle='-')
plt.xticks(np.arange(0, len(times) + 1, step=60 * 60 * 2), labels=np.arange(0, 25, 2))
plt.xlabel('Time (hr)')
plt.ylabel('Conduction heat (W/m$^2$)')
plt.title('Change in conduction heat over time')
plt.grid(True)
plt.show()

# %% ---- TEST CODE -----

print('il valore del calore scambiato per conduzione vale: ', trunk.Q_cond(), '[W]')
print('il valore del calore scambiato per convezione vale: ', trunk.Q_conv(), '[W]')
print('il valore del calore scambiato per irraggiamento vale: ', trunk.Q_irr(), '[W]')
print('il valore del calore perso per evaporazione vale: ', trunk.E_sk(), '[W]')
print('il valore del calore scambiato attraverso il sangue vale: ', trunk.Q_blood(), '[W]')
print('il valore del lavoro utilizzando per pompare il sangue vale: ', trunk.W_pump_blood(), '[W]')
print('il valore finale della T_int è: ', trunk.energy_balance(delta_t=60 * 60) - 273.15, '[degC]')