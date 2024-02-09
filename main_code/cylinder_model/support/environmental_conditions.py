import CoolProp.CoolProp as CP


class EnvironmentalConditions:


    def __init__(self, temperature=298, pressure=101325, humidity=0.60, properties=None, fluid='water'):
        self.fluid = fluid
        self.temperature = temperature
        self.pressure = pressure
        self.humidity = humidity
        self. properties = properties

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


    def __repr__(self):
        return f"This is environmental conditions class."