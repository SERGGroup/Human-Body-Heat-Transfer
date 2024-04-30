from CoolProp.CoolProp import PropsSI, HAPropsSI
import numpy as np
from main_code.body_class import Body


class EnvironmentalConditions:
    def __init__(
            self,
            body: Body,
            temperature: float = 273.15 + 24.85,
            pressure: float = 101325,
            humidity: float = 0.50,
            v_air: float = 0.6,
            properties: float = None,
            fluid: str = 'water'):
        self.body = body
        self.fluid = fluid
        self.temperature = temperature
        self.pressure = pressure
        self.humidity = humidity
        self.properties = properties
        self.v_air = v_air

    def set_conditions(self, temperature, pressure, humidity) -> None:
        self.temperature = temperature
        self.pressure = pressure
        self.humidity = humidity

    def calculate_properties(self) -> dict[str, float]:
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
            'Temperature':                          self.temperature,
            'Pressure':                             self.pressure,
            'Humidity':                             self.humidity,
            'Density':                              density,
            'Enthalpy':                             enthalpy,
            'Entropy':                              entropy,
            'Specific Heat':                        specific_heat,
            'Dynamic Viscosity':                    dynamic_viscosity,
            'Thermal Conductivity':                 thermal_conductivity,
            'Water Vapor Pressure':                 water_vapor_pressure,
            'Water Vapor Pressure Skin':            water_vapor_pressure_skin,
            'Humidity Ratio':                       humidity_ratio,
            'Wet Bulb Temperature':                 wet_bulb_temperature,
            'Water Vapor Pressure 37 degrees':      water_vapor_pressure_37_degrees
        }

    def get_properties(self):
        return self.properties

    @staticmethod
    def get_vector_a(self) -> np.ndarray:
        return np.array([0.5, 0.5, 3.5, 3.5, 3.5, 3.5])  # [up, down, left, right, front, back]

    @staticmethod
    def get_vector_b(self) -> np.ndarray:
        return np.array([3.5, 3.5, 4.5, 4.5, 4.5, 4.5])

    @staticmethod
    def get_vector_c(self) -> np.ndarray:
        return np.array([3.5, 0.5, 0.5, 4.5, 3.5, 0.5])

    def calculate_area_factor(self, vector_a: np.ndarray, vector_b: np.ndarray, vector_c: np.ndarray) -> list[float]:
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

    @staticmethod
    def get_vector_T_surf(self) -> np.ndarray:
        return np.array([20, 18, 19, 20, 21.5, 22])  # wall temperatures

    def calculate_T_mr(self, area_factor: list[float], T_surf: np.ndarray) -> float:
        return (np.sum(np.fromiter((T_surf[i] ** 4 * area_factor[i] for i in range(len(area_factor))), dtype=float)) /
                np.sum(np.fromiter((area_factor[i] for i in range(len(area_factor))), dtype=float))) ** (1 / 4)  # [°C]

    @staticmethod
    def get_inspired_air_composition(self) -> dict[str, float]:
        comp = {
            'pCO2': 0.03,  # %
            'pO2':  20.93,  # %
            'pN2':  79.04  # %
        }
        return comp

    @staticmethod
    def get_expired_air_composition(self) -> dict[str, float]:
        comp = {
            'pCO2': 3.60,  # %
            'pO2':  16.86,  # %
            'pN2':  79.54  # %
        }
        return comp

    @staticmethod
    def get_Pt_torr(self) -> float:
        return 760  # [Torr]; 760 [Torr] = 101325 [Pa]

    @staticmethod
    def get_V_atps(self) -> float:
        return 30  # [l]; volume of expired gas

    def calculate_V_st(self) -> float:
        return self.get_V_atps() * (273.15 / self.temperature)  # [l]; gas volume at standard temperature

    def calculate_V_sp(self) -> float:
        return self.get_V_atps() * (self.get_Pt_torr() / 760)  # [l]; gas volume at standard pressure

    def calculate_V_spd(self) -> float:
        water_vapor_pressure_torr = (self.properties['Water Vapor Pressure']) / 133.3  # [torr]
        return self.get_V_atps() * (
                    (self.get_Pt_torr() - water_vapor_pressure_torr) / 760)  # [l]; gas volume at standard pressure dry

    def get_water_vapor_pressure_at_37_degrees_torr(self) -> float:
        water_vapor_pressure_37_degrees = (self.properties['Water Vapor Pressure 37 degrees']) / 133.3  # [torr]
        return water_vapor_pressure_37_degrees  # [Torr]

    def calculate_V_stpd(self) -> float:
        water_vapor_pressure_torr = (self.properties['Water Vapor Pressure']) / 133.3  # [torr]
        return self.get_V_atps() * ((self.get_Pt_torr() - water_vapor_pressure_torr) / 760) * (
                    273.15 / self.temperature)  # [l]; gas volume

    def calculate_V_btps(self) -> float:
        water_vapor_pressure_torr = (self.properties['Water Vapor Pressure']) / 133.3  # [torr]
        water_vapor_pressure_37_degrees = (self.properties['Water Vapor Pressure 37 degrees']) / 133.3  # [torr]
        return (self.get_V_atps() * (310.15 / self.temperature)
                * ((self.get_Pt_torr() - water_vapor_pressure_torr) / (
                            self.get_Pt_torr() - water_vapor_pressure_37_degrees)))

    def get_V_e(self) -> float:
        return 26.483  # [l]; volume of expired air

    def calculate_V_i(self) -> float:
        comp_insp = self.get_inspired_air_composition()
        comp_exp = self.get_expired_air_composition()
        return (self.get_V_e() * (comp_exp['pN2'] / 100 * self.get_V_e())) / (
                    comp_insp['pN2'] / 100 * self.get_V_e())  # [l]; volume of inspired air

    def calculate_V_O2_i(self) -> float:
        comp_insp = self.get_inspired_air_composition()
        return comp_insp['pO2'] / 100 * self.calculate_V_i()  # [l]; volume of O2 in inspired air

    def calculate_VO2_e(self) -> float:
        comp_exp = self.get_expired_air_composition()
        return comp_exp['pO2'] / 100 * self.get_V_e()  # [l]; volume of O2 in expired air

    def calculate_VO2(self) -> float:
        return self.calculate_V_O2_i() - self.calculate_VO2_e()  # [l]; volume of O2 removed from inspired air

    def calculate_VCO2(self) -> float:
        comp_insp = self.get_inspired_air_composition()
        comp_exp = self.get_expired_air_composition()
        return (comp_exp['pCO2'] / 100 * self.get_V_e()) - (
                    comp_insp['pCO2'] / 100 * self.calculate_V_i())  # [l]; volume of carbon dioxide produced

    def get_Q_O2_for_minute(self) -> float:
        return self.calculate_VO2()

    def get_Q_CO2_for_minute(self) -> float:
        return self.calculate_VCO2()

    def calculate_RQ(self) -> float:
        return self.get_Q_CO2_for_minute() / self.get_Q_O2_for_minute()  # respiratory quotient

    def calculate_O2_true(self) -> float:
        comp_insp = self.get_inspired_air_composition()
        comp_exp = self.get_expired_air_composition()
        return ((comp_exp['pN2'] / 100) / (comp_insp['pN2'] / 100) * (comp_insp['pO2'] / 100)) - (
                    comp_exp['pO2'] / 100)  # percentage of O2 consumed for any volume of air expired
