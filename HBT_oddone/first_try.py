import math

"""When everything works, i'll divide the code in variouis files
(i don't know why but my pc don't wont to to import classes beetween different files -.-"
"""

#Creation of Body class ---> when we model every body parts, we'll make an overall balance and add variables
#I assume that the person represented by this class is seated in first approximation
class Body:
    def __init__(self, height=1.80, weight=76,gender=1,age=25,total_area= 1.8,T_amb=293, v_air = 1.5 ):
        self.height = height    #[m]
        self.weight = weight    #[kg]
        self.gender = gender    #[male=1 ; female=0]
        self.age = age  #[dimensionless]
        self.total_area = total_area    #[m^2]
        self.T_amb = T_amb  #[K]
        self.v_air = v_air  #[m/s]


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

"""
Try if it works
"""

person = Body()
trunk = Cylinder(d=0.2, h=0.6, body=person, T_int=309, internal_heat_source=100)

# simulaiton of energy balance for 60 seconds:

delta_time = 60  # secondi
final_T_int = trunk.energy_balance(delta_time)
heat_lost_w = trunk.dissipated_energy_watt()
heat_lost_j = trunk.dissipated_energy_joule(delta_time)

print(f'Final T_int: {final_T_int} [K]')
print(f'Heat lost: {heat_lost_w} [W]')
print(f'Heat lost: {heat_lost_j} [j]')












































