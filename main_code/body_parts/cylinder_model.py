import math


#Creation of Cylinder class --> main class where the future subclasses, which represent every body parts, will refer

class Cylinder:

    def __init__(self, d, h, body=None, T_int=None, internal_heat_source = 100 ):
        self.d = d  #[m]
        self.h = h  #[m]
        self.body = body
        self.T_int = T_int  #[K]
        self.internal_heat_source = internal_heat_source    #[W] --> it rapresents the "M" for this first heat balance, but it will be defined in a Body's method

    #Functions to calculate the geometric characteristics of the cylinder

    def calculate_area(self):
        radius = self.d / 2
        lateral_area = 2 * math.pi * radius * self.h  #[m^2]
        base_area = 2 * math.pi * radius ** 2  #[m^2]
        total_area = lateral_area + base_area  #[m^2]
        return total_area

    def calculate_volume(self):
        radius = self.d / 2
        volume = math.pi * radius ** 2 * self.h #[m^3]
        return volume

    #Functions to calculate the different therms of the energy balance --> M-W = Q_cond + Q_conv + Q_irr

    def Q_cond(self):
        #cylinder's thermal conductivity coefficient
        k = 0.3 #0,3[W/m*K] --> value obtained from ASHRAE

        #cylinder's thickness
        s = 0.2  #[m] -->value obtained from research on internet, assuming the heat exchange by conduction take place only throught skin

        exchange_area = self.calculate_area()
        delta_T = self.T_int - self.body.T_amb

        q_cond = (2 * math.pi * self.h * k * delta_T) / math.log(self.d + s / self.d)
        return q_cond

    def Q_conv(self):
        delta_T = self.T_int - self.body.T_amb
        exchange_area = self.calculate_area()

        if self.body.v_air < 0.2:
            h_c = 3.1   #[W/m^2*K]; Table 6, Aiman's file
            q_conv = h_c * exchange_area * delta_T
        else:
            h_c = 8.3 * (self.body.v_air ** 0.6)   #Table 6, Aiman's file
            q_conv = h_c * exchange_area * delta_T
        return q_conv

    def Q_irr(self):
        exchange_area = self.calculate_area()
        sigma = 5.67 * (10 ** (-8))  #[W/m^2*K^4]
        epsilon_skin = 0.95 #Aiman's file
        f_cl = 0.70 #Aiman's file

        q_irr = exchange_area * sigma * epsilon_skin * f_cl * (self.T_int ** 4 - self.body.T_amb ** 4)
        return q_irr

    def W(self):
        W = 0   #withount cosider the work done by hear, lungs etc...
        return W

    def energy_balance(self, delta_t):
        q_cond = self.Q_cond()
        q_conv = self.Q_conv()
        q_irr = self.Q_irr()
        w = self.W()
        cp_air = 1005 #[J/kg*K]

        balance = self.internal_heat_source - w - q_cond - q_conv - q_irr
        self.T_int += (balance * delta_t) / (self.body.weight * self.body.height * cp_air)   #Conversion from è[W] to [K]
        return self.T_int

    def dissipated_energy_watt(self):
        q_cond = self.Q_cond()
        q_conv = self.Q_conv()
        q_irr = self.Q_irr()
        w = self.W()

        dissipated_w =q_cond + q_conv + q_irr + w
        return dissipated_w

    def dissipated_energy_joule(self, delta_t):
        q_cond = self.Q_cond()
        q_conv = self.Q_conv()
        q_irr = self.Q_irr()
        w = self.W()

        dissipated_j = (q_cond + q_conv + q_irr + w)*delta_t
        return dissipated_j