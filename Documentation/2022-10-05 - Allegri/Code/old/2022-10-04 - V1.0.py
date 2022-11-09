import math
from matplotlib import pyplot as plt

class Cylinder:
    def __init__(self, d, h, prev=None):
        self.r = d / 200
        self.h = h/ 100

        self.prev = prev
        self.succ = list()

        if prev is not None:

            prev.succ.appen(self)

    def volume(self):
        return (math.pi * self.h * self.r ** 2)

    def area_s(self):
        return (math.pi * self.r * 2 * self.h)

    def area(self):
        return ((math.pi * self.r * 2 * self.h) + (math.pi * 4 * self.r ** 2)) / 10000

    def Qc(self):
        if v_air<= 0.2:
            Qc = self.hc * self.area_s() * (self.Tsk() - Tamb) * fcl
        else:
            hc= 8.3 * (v_air**0.5)                  #ASHRAE
            Qc = hc * self.area_s() * (self.Tsk() - Tamb) * fcl
        return Qc

    def Qc_iter (self,T):
        if v_air <= 0.2:
            Qc = self.hc * self.area_s() * (self.Tsk() - T) * fcl
        else:
            hc = 8.3 * (v_air ** 0.5)  # ASHRAE
            Qc = hc * self.area_s() * (self.Tsk() - T) * fcl
        return Qc

    def Qr(self):
        sigma= 5.67*(10**(-8))
        eps_pelle= 0.95
        Qr =  sigma * self.area_s() *eps_pelle* ((self.Tsk()**4) - (Tamb**4)) * fcl * 0.73                 #termine preso da Fagner,
        return Qr                                                                                   #è il rapporto tra l'area effettivamente sottoposta
                                                                                                    # a scambio termico per radiazione e l'area di DuBois
    def Qr_iter (self,T):
        sigma = 5.67 * (10 ** (-8))
        eps_pelle = 0.95
        Qr = sigma * self.area_s() * eps_pelle * ((self.Tsk() ** 4) - (T ** 4)) * fcl * 0.73
        return Qr

    def He(self):
        P1 = Pvap(self.Tsk())
        P2 = Pvap(Tamb)
        w = w_sk(Tamb)
        if v_air <= 0.2:
            he= 16.5 * self.hc
        else:
            he= 8.3 * (v_air**0.5) * 16.5
        He = self.area_s() * (P1 - (phi * P2)) * w / ((Rcl + (1 / (fcl * he))))
        return He

    def He_iter(self,T):
        P1 = Pvap(self.Tsk())
        P2 = Pvap(T)
        w = 0.006
        if v_air <= 0.2:
            he= 16.5 * self.hc
        else:
            he= 8.3 * (v_air**0.5) * 16.5
        He = self.area_s() * (P1 - (phi * P2)) * w / ((Rcl + (1 / (fcl * he))))
        return He

    def H_res(self):
        H_res = ((0.0014 * Body().M() * (34 - Tamb + 273.15)) + (0.0173 * Body().M() * (5.87 - Pvap(Tamb)))) * self.area_s()  # da ASHRAE
        return H_res

    def H_res_iter(self,T):
        H_res = ((0.0014 * Body().M() * (34 - T + 273.15)) + (0.0173 * Body().M() * (5.87 - Pvap(T)))) * self.area_s()  # da ASHRAE
        return H_res

    def M_vol(self):
        M_vol= self.M_i()/ self.volume()
        return M_vol

    def Tsk(self):
        k= 2.21                                      #conduzione in cilindro con generazione di calore
        Tsk= self.Tint-(self.M_vol()*(self.r**2)/(4*k))
        return Tsk

    def DeltaH_bl(self):

        delta = 0.

        if self.prev is not None:

            dt = self.T_int - self.prev.T_int
            delta += self.blod_HE(dt)

        for succ in self.succ:

            dt = self.T_int - succ.T_int
            delta += self.blod_HE(dt)

    def blod_HE(self, DT):
        delta= -(0.001 * self.v_dot_bl /60) * rho_bl * cp_ve * DT * self.eps
        return delta

    def M_i(self):
        return Body().M() * self.volume() / Body().Vol_tot()

    def Udot(self):
        Udot = self.M_i() - (self.Qc() + self.Qr() + self.He() + self.H_res()) + self.DeltaH_bl()
        return Udot

class Head(Cylinder):
    def __init__(self, d, h):
        super().__init__(d, h)

        self.hr = 4.1
        self.hc = 3.6
        self.he = 5.9
        self.doppio = 0
        self.eps= 0.90
        self.Tint = 311.5
        self.Tar= 310.5
        self.v_dot_bl = 0.75


class Neck(Cylinder):
    def __init__(self, d, h):
        super().__init__(d, h)

        self.hr = 4.1
        self.hc = 3.6
        self.he = 5.9
        self.doppio = 0
        self.eps = 0.90
        self.Tint = 310.5
        self.v_dot_bl = 0.75


class Trunk(Cylinder):
    def __init__(self, d, h):
        super().__init__(d, h)

        self.hr = 4.4
        self.hc = 3.2
        self.he = 5.3
        self.doppio = 0
        self.eps= 1
        self.Tint = 310
        self.v_dot_bl = 1.73


class Arm(Cylinder):
    def __init__(self, d, h):
        super().__init__(d, h)

        self.hr = 5.2
        self.hc = 2.9
        self.he = 4.8
        self.doppio = 1
        self.eps= 0.92
        self.Tint = 309.5
        self.v_dot_bl = 0.21


class Forearm(Cylinder):
    def __init__(self, d, h):

        super().__init__(d, h)
        self.hr = 4.9
        self.hc = 3.7
        self.he = 6.1
        self.doppio = 1
        self.eps = 0.92
        self.Tint = 309
        self.v_dot_bl = 0.21


class Hand(Cylinder):
    def __init__(self, d, h):

        super().__init__(d, h)
        self.hr = 4.1
        self.hc = 4.1
        self.he = 6.8
        self.doppio = 1
        self.eps = 0.92
        self.Tint = 308.5
        self.v_dot_bl = 0.21


class Thigh(Cylinder):
    def __init__(self, d, h):

        super().__init__(d, h)
        self.hr = 4.3
        self.hc = 4.1
        self.he = 6.8
        self.doppio = 1
        self.eps = 0.92
        self.Tint = 309.5
        self.v_dot_bl = 0.28


class Leg(Cylinder):
    def __init__(self, d, h):

        super().__init__(d, h)
        self.hr = 5.3
        self.hc = 4.1
        self.he = 6.8
        self.doppio = 1
        self.eps = 0.92
        self.Tint = 309
        self.v_dot_bl = 0.28


class Foot(Cylinder):
    def __init__(self, d, h):
        super().__init__(d, h)

        self.hr = 3.9
        self.hc = 5.1
        self.he = 8.4
        self.doppio = 1
        self.eps = 0.92
        self.Tint = 308.5
        self.v_dot_bl = 0.28      #[L/min]


class Body:
    def __init__(self):
        self.l=[Head(14.6, 20.7),
                Neck(11.4, 8.3),
                Trunk(26.0, 79.8),
                Arm(9.0, 35.3),
                Forearm(7.4, 29.2),
                Hand(4.6, 30.0),
                Thigh(13.4, 35.2),
                Leg(8.6, 37.9),
                Foot(7.2, 24.1)]
        self.altezza=1.76
        self.peso=76
        self.sesso=1                                #1=maschio,0=femmina
        self.eta=25
        self.Atot=1.8


                                                    # misure prese da Takemori et al. per persona di 1,76 m,
                                                    # da trovare relazioni fra i diversi raggi e tra un raggio
                                                    # di riferimento (tronco) e l'altezza del campione ?
    def Area_tot_scambio(self):
        A=0
        for i in self.l:
            if i.doppio == 0:
                A += i.area_s()
            else:
                A += 2 * i.area_s()
        return A


    def Area_tot(self):
       A=0
       for i in self.l:
            if i.doppio == 0:
                A += i.area()
            else:
                A += 2 * i.area()
       return A

    def Vol_tot(self):
        V=0
        for i in self.l:
            if i.doppio == 0:
                V += i.volume()
            else:
                V += 2 * i.volume()
        return V

    def M(self):
        if self.sesso == 1:
            M = 66.5 + 13.8 * self.peso + 5 * self.altezza * 100 - 6.8 * self.eta
        else:
            M = 65.51 + 9.6 * self.peso + 1.8 * self.altezza * 100 - 4.7 * self.eta

        return  M * 4184 / 86400

    def Qctot(self):                                        # calore scambiato per convezione                  #ASHRAE
        Q=0
        for i in l:
            if i.doppio==0:
                Q += i.Qc()
            else:
                Q+= i.Qc() * 2
        return Q

    def Qctot_iter(self,T):                                        # calore scambiato per convezione                  #ASHRAE
        Q=0
        for i in l:
            if i.doppio==0:
                Q += i.Qc_iter(T)
            else:
                Q+= i.Qc_iter(T) * 2
        return Q
    def Qrtot(self):                                        # calore scambiato per irraggiamento
        Q = 0
        for i in self.l:
            if i.doppio == 0:
                Q += i.Qr()
            else:
                Q += 2 * i.Qr()
        return Q

    def Qrtot_iter(self,T):                                        # calore scambiato per irraggiamento
        Q = 0
        for i in self.l:
            if i.doppio == 0:
                Q += i.Qr_iter(T)
            else:
                Q += 2 * i.Qr_iter(T)
        return Q

    def He(self):                                           # calore scambiato per evaporazione
        H = 0                                               # nel modello EES la Rcl è 10, non capisco perchè
        for i in self.l:                                    # essendo a riposo e cercando una T per cui U_dot = 0 pensavo di mettere la w minima
            if i.doppio == 0:
                H += i.He()
            else:
                H += 2 * i.He()
        return H
    def He_iter(self,T):
        H = 0
        for i in self.l:
            if i.doppio == 0:
                H += i.He_iter(T)
            else:
                H += 2 * i.He_iter(T)
        return H
    def m_dot_res(self):
        m_dot_res= 1.433 * self.Atot * self.M * (10 ** (-6))
        return m_dot_res


    def H_res(self):
        #H_res = (Body().m_dot_res() * cp_air * (Texp - Tixp)) + (Body().m_dot_res() * ((omegax(Pvap(Texp)) * hvap(Texp)) - (omegax(Pvap(Tixp)) * hvap(Tixp))))
        H_res = 0
        for i in self.l:
            if i.doppio == 0:
                H_res += i.H_res()
            else:
                H_res += 2 * i.H_res()
        return H_res

    def H_res_iter(self,T):
        H_res = 0
        for i in self.l:
            if i.doppio == 0:
                H_res += i.H_res_iter(T)
            else:
                H_res += 2 * i.H_res_iter(T)
        return H_res

    def W(self):
        W=0             #corpo a riposo
        return W
    def Udot(self):
        Udot = Body().M() - (Body().Qctot() + Body().Qrtot() + Body().He() + Body().H_res()) - Body().W()
        return Udot

    def Udot_iter(self,T):
        Udot = Body().M() - (Body().Qctot_iter(T) + Body().Qrtot_iter(T) + Body().He_iter(T) + Body().H_res_iter(T)) - Body().W()
        return Udot


def Pvap(T):
    #P = 611.2 * math.exp((40650 / 8.314) * ((1 / 273.15) - (1 / T)))  # equazione di Clapeyron
    P=(math.exp(18.956-(4030.18/(T-38.15))))/10                        #eq Antoine, conversione da Human Thermal enviroment pag 15
    return P

def TC(Tamb):
    T=Tamb
    while math.fabs(body.Udot_iter(T)) > 0.1:
        if body.Udot_iter(T) < 0:
            T += 0.01
            #print ('T=',T, '[K]')
            #print('Udot=',body.Udot_iter(T),'[W]')
        else:
            T -= 0.01
            #print ('T=',T , '[K]')
            #print('Udot=',body.Udot_iter(T),'[W]')
    return T

def w_sk(Tamb):# parametro
    T=303 #TC(Tamb)
    if Tamb <= T:  # in K
        w = 0.006
    else:
        w= 0.006 + 0.009 * (Tamb - T)
    return w

'''def hvap(T):
    t = T - 273.15
    if t >= 0 and t < 10:
        hvap = 42.117 * t / 10
    elif t >= 10 and t < 20:
        hvap = 42.117 + ((84.012 - 42.117) * (t - 10) / 10)
    elif t >= 20 and t < 30:
        hvap = 84.012 + ((125.883 - 84.012) * (t - 20) / 10)
    elif t >= 30 and t <= 40:
        hvap = 125.883 + ((167.623 - 125.883) * (t - 30) / 10)
    return hvap * 1000'''

'''def omegax(Px):
    omega = 0.622 * ((Px) / (Pamb - Px))
    return omega'''





Pamb=101325
Tamb=300
v_air=0.15
#Tsk=306.5
fcl=1 #(corpo nudo)
Rcl=0
phi=0.5
cp_air = 1005           # assumo come costante
cp_bl=3850 #[J/kg*K]
cp_ve=cp_bl
cp_ar=cp_bl
rho_bl=1059 #[kg/m^3]

body = Body()
head = Head(14.6, 20.7)
neck = Neck(11.4, 8.3)
trunk = Trunk(26.0, 79.8)
arm = Arm(9.0, 35.3)
forearm = Forearm(7.4, 29.2)
hand = Hand(4.6, 30.0)
thigh = Thigh(13.4, 35.2)
leg = Leg(8.6, 37.9)
foot = Foot(7.2, 24.1)

l=[head, neck, trunk, arm, forearm, hand, thigh, leg, foot]
L=['head', 'neck', 'trunk', 'arm', 'forearm', 'hand', 'thigh', 'leg', 'foot']


'''while math.fabs(body.Udot_iter()) > 0.1:
    Tamb += 0.01
    print ('Tamb=',Tamb, '[K]')
    print('Udot=',body.Udot_iter(),'[W]')
    print('\n')
print(w_sk(Tamb))'''


# print(TC(Tamb))
# n=0
# for i in l:
#     print(L[n])
#     print('Mvol= ', i.M_i(),'[W/m^3]')
#     print('Tsk', i.Tsk(), '[K]')
#     print('Qc=', i.Qc(),'[W]')
#     print('Qr=', i.Qr(),'[W]')
#     print('He=', i.He(),'[W]')
#     print('H_res=', i.H_res(),'[W]')
#     if i is not trunk:
#         print('DeltaH blood=', i.DeltaH_bl(), '[W]')
#         print('Udot=', i.Udot(), '[W]')
#     else:
#         delta=0
#         for i in l:
#             if i.doppio==0:
#                 delta -= i.DeltaH_bl()
#             else:
#                 delta -= 2*i.DeltaH_bl()
#         print('DeltaH blood', delta , '[kg/s]')
#         print('Udot=', i.Udot() + delta, '[W]')
#     print('\n')
#     n+=1
#
#
# print('Body')
# print('M= ', body.M(),'[W]')
# print('Qc=', body.Qctot(),'[W]')
# print('Qr=', body.Qrtot(),'[W]')
# print('He=', body.He(),'[W]')
# print('H_res=', body.H_res(),'[W]')
# print('Udot=', body.Udot(), '[W]')
'''
y=[]
x=[]
while Tamb <=310:
    y.append(body.Udot())
    x.append(Tamb)
    Tamb += 1

plt.plot(x,y)
plt.title("variazione di energia interna")
plt.xlabel("T[K]")
plt.ylabel("U[W]")
plt.show()'''

def error_function(x):

    res = 0

    i = 1
    for part in body.l:

        part.eps = x[0]
        if not type(part) == Trunk:

            part.Tint = x[i]
            i = i + 1

    for part in body.l:

        res += part.Udot() ** 2

    print(res)
    return res

import scipy.optimize as opt
import numpy as np

res = opt.minimize(error_function, np.array([0.11, 311.5, 310.5, 309.5, 309, 308.5, 309.5, 309, 308.5]))
print(res.x)

# [Head(14.6, 20.7),
# Neck(11.4, 8.3),
# Trunk(26.0, 79.8),
# Arm(9.0, 35.3),
# Forearm(7.4, 29.2),
# Hand(4.6, 30.0),
# Thigh(13.4, 35.2),
# Leg(8.6, 37.9),
# Foot(7.2, 24.1)]