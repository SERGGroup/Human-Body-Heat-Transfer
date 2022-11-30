import math
from matplotlib import pyplot as plt

class Cylinder:
    def __init__(self, d, h, body, prev=None):

        self.r = d / 200
        self.h = h/ 100
        self.delta=0.90

        self.body = body
        self.prev = prev
        self.succ = list()

        if self.prev is not None:

            prev.succ.append(self)

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
        Hr=0
        if type(self) == Trunk:
                Hr += body.H_res() * 0.30
        elif type(self) == Head:
                Hr += body.H_res() * 0.45
        elif type(self) == Neck:
                Hr += body.H_res() * 0.25
        else:
                Hr+=0
        return Hr



    def M_vol(self):
        M_vol= self.M_i()/ self.volume() *self.delta
        return M_vol

    def Tsk(self):
        k= 2.21                                      #conduzione in cilindro con generazione di calore
        Tsk= self.Tint-(self.M_vol()*(self.r**2)/(4*k))
        return Tsk

    def DeltaH_bl(self):                        #self.Tint = Tvenosa
                                                #self.prec.Tint = Tarteriosa
        delta = 0.

        if self.prev is not None:

            dt = self.Tint - self.prev.Tint
            delta += self.blod_HE(dt)

        for succ in self.succ:

            dt = self.Tint - succ.Tint
            delta += self.blod_HE(dt)

        return delta

    def blod_HE(self, DT):
        delta= -(0.001 * self.v_dot_bl /60) * rho_bl * cp_ve * DT * self.eps
        return delta

    def M_i(self):
        return Body().M() * self.volume() / Body().Vol_tot()

    def Udot(self):
        Udot = self.M_i() - (self.Qc() + self.Qr() + self.He() + self.H_res()) + self.DeltaH_bl()
        return Udot

class Head(Cylinder):
    def __init__(self, d, h, body, prev):

        #self.succ=[]
        super().__init__(d, h, body, prev)
        self.prev= Neck(11.4, 8.3)
        self.hr = 4.1
        self.hc = 3.6
        self.he = 5.9
        self.doppio = 0
        self.eps= 1
        self.Tint = 311.5
        self.Tar= 310.5
        self.v_dot_bl = 0.75


class Neck(Cylinder):
    def __init__(self, d, h, body, prev):

        super().__init__(d, h, body, prev)

        #self.succ= []
        self.prev= Trunk(26.0, 79.8)
        self.hr = 4.1
        self.hc = 3.6
        self.he = 5.9
        self.doppio = 0
        self.eps = 1
        self.Tint = 310.5
        self.v_dot_bl = 0.75


class Trunk(Cylinder):
    def __init__(self, d, h, body):

        #self.succ= [Neck(11.4, 8.3), Arm(9.0, 35.3), Thigh(13.4, 35.2)]
        super().__init__(d, h, body)
        self.hr = 4.4
        self.hc = 3.2
        self.he = 5.3
        self.doppio = 0
        self.eps= 1
        self.Tint = 310.15
        self.v_dot_bl = 1.73


class Arm(Cylinder):
    def __init__(self, d, h, body, prev):

        super().__init__(d, h, body, prev)

        self.prev= Trunk(26.0, 79.8)
        self.hr = 5.2
        self.hc = 2.9
        self.he = 4.8
        self.doppio = 1
        self.eps= 0.92
        self.Tint = 309.5
        self.v_dot_bl = 0.21


class Forearm(Cylinder):
    def __init__(self, d, h, body, prev):

        super().__init__(d, h, body, prev)

        self.prev= Arm(9.0, 35.3)
        self.hr = 4.9
        self.hc = 3.7
        self.he = 6.1
        self.doppio = 1
        self.eps = 0.92
        self.Tint = 309
        self.v_dot_bl = 0.21


class Hand(Cylinder):
    def __init__(self, d, h, body, prev):

        super().__init__(d, h, body, prev)

        self.prev=Forearm(7.4, 29.2)
        self.hr = 4.1
        self.hc = 4.1
        self.he = 6.8
        self.doppio = 1
        self.eps = 0.92
        self.Tint = 308.5
        self.v_dot_bl = 0.21


class Thigh(Cylinder):
    def __init__(self, d, h, body, prev):

        super().__init__(d, h, body, prev)

        self.prev= Trunk(26.0, 79.8)
        self.hr = 4.3
        self.hc = 4.1
        self.he = 6.8
        self.doppio = 1
        self.eps = 0.92
        self.Tint = 309.5
        self.v_dot_bl = 0.28


class Leg(Cylinder):
    def __init__(self, d, h, body, prev):

        super().__init__(d, h, body, prev)

        self.prev=Thigh(13.4, 35.2)
        self.hr = 5.3
        self.hc = 4.1
        self.he = 6.8
        self.doppio = 1
        self.eps = 0.92
        self.Tint = 309
        self.v_dot_bl = 0.28


class Foot(Cylinder):
    def __init__(self, d, h, body, prev):

        super().__init__(d, h, body, prev)

        self.prev=Leg(8.6, 37.9)
        self.hr = 3.9
        self.hc = 5.1
        self.he = 8.4
        self.doppio = 1
        self.eps = 0.92
        self.Tint = 308.5
        self.v_dot_bl = 0.28


class Body:
    def __init__(self):

        self.altezza=1.76
        self.peso=76
        self.sesso=1                                #1=maschio,0=femmina
        self.eta=25
        self.Atot=1.8

        # misure prese da Takemori et al. per persona di 1,76 m,
        # da trovare relazioni fra i diversi raggi e tra un raggio
        # di riferimento (tronco) e l'altezza del campione ?
    def __init_body_parts(self):

        trunk = Trunk(26.0, 79.8, self)
        neck = Neck(11.4, 8.3, self, trunk)
        head = Head(11.4, 8.3, self, neck)

        self.l = [head,
                  neck,
                  trunk,
                  Arm(9.0, 35.3),
                  Forearm(7.4, 29.2),
                  Hand(4.6, 30.0),
                  Thigh(13.4, 35.2),
                  Leg(8.6, 37.9),
                  Foot(7.2, 24.1)]


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
        for i in body.l:
            if i.doppio==0:
                Q += i.Qc()
            else:
                Q+= i.Qc() * 2
        return Q

    def Qctot_iter(self,T):                                        # calore scambiato per convezione                  #ASHRAE
        Q=0
        for i in body.l:
            if i.doppio==0:
                Q += i.Qc_iter(T)
            else:
                Q+= i.Qc_iter(T) * 2
        return Q
    def Qrtot(self):                                                # calore scambiato per irraggiamento
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
        m_dot_res= 1.433 * self.Atot * self.M() * (10 ** (-5))
        return m_dot_res

    def H_res(self):
        H_res = ((0.0014 * Body().M() * (34 - Tamb + 273.15)) + (0.0173 * Body().M() * (5.87 - Pvap(Tamb)))) * self.Area_tot_scambio()  # da ASHRAE
        return H_res

    def H_res_iter(self,T):
        H_res = ((0.0014 * Body().M() * (34 - Tamb + 273.15)) + (0.0173 * Body().M() * (5.87 - Pvap(T)))) * self.Area_tot_scambio()  # da ASHRAE
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

    def Br(self):
        Br = 0
        for i in self.l:
            B = i.Qr() * (1 - (Tamb / i.Tsk()))
            if i.doppio == 0:
                Br += B
            else:
                Br += 2 * B
        return Br

    def Bc(self):
        Bc = 0
        for i in self.l:
            B = i.Qc() * (1 - (Tamb / i.Tsk()))
            if i.doppio == 0:
                Bc += B
            else:
                Bc += 2 * B
        return Bc

    def mean_Tsk(self):
        T = 0
        for i in self.l:
            if i.doppio == 0:
                T += i.Tsk()
            else:
                T += 2 * i.Tsk()
        return T / 15

    def Be(self):  # suodre stimato 10-12 l al giorno
        mw_ = 3 * 10 ** (-6) * 1000  # ipotizzata al valore minimo con 0.3*10^-6, valore 3 in linea con articlo di ferreira
        h_lv = 2260  # kJ/K
        s_lv = 6.056  # kJ/kg*K
        R_w = 0.46151  # kJ/kg*K
        Be = mw_ * (h_lv - Tamb * s_lv) + mw_ * R_w * Tamb * math.log((Pvap(self.mean_Tsk()) / Pvap(Tamb)))
        return Be

    def Bres(self):
        R_w = 461.51  # J/kg*K
        Tex = Trunk.Tint
        deltaB_air = self.m_dot_res() * (cp_air * (Tex - Tamb - Tamb * math.log((Tex / Tamb))))                                                                      # semplificazioni dovute al fatto che T0==Tamb e P0==Pamb
        deltaB_wat = self.m_dot_res() * omegax(Pvap(Tex)) * (cp_w * (Tex - Tamb - Tamb * math.log((Tex / Tamb))) + R_w * Tamb * math.log((Pvap(Tex) / Pvap(Tamb))))  # semplificazioni dovute al fatto che T0==Tamb e P0==Pamb
        return deltaB_air - deltaB_wat

    def Bdest(self):
        return self.M() - (self.Bc()+self.Br()+self.Bres()+self.Be()) - self.W()

    def rendimento(self):
        rend = 1 - (Body().Bdest()/Body().M())
        return rend


def Pvap(T):
    #P = 611.2 * math.exp((40650 / 8.314) * ((1 / 273.15) - (1 / T)))  # equazione di Clapeyron
    P=(math.exp(18.956-(4030.18/(T-38.15))))/10                        #eq Antoine, conversione da Human Thermal enviroment pag 15
    return P

def TC(t,T1=310,T2=290):
    T=t
    if math.fabs(body.Udot_iter(t)) > 1:
        if body.Udot_iter(t) < 0:
            T= (t+T1)/2
            #print ('T1=',T1)
            #print ('T2=',T2)
            #print('U minore di zero, T=', T, '[K]')
            #print('\n')
            #print('Udot=', body.Udot_iter(T), '[W]')
            return  TC(T, T1, t)
            #T += 0.01

        else:
            T= (t+T2)/2
            #T -= 0.01
            #print('T1=', T1)
            #print('T2=', T2)
            #print('U maggiore di zero, T=', T, '[K]')
            #print('\n')
            #print('Udot=', body.Udot_iter(T), '[W]')
            return TC(T, t, T2)
    else:
        return T



def w_sk(Tamb):# parametro
    T=TC(Tamb)   #303
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

def omegax(Px):
    omega = 0.622 * ((Px) / (Pamb - Px))
    return omega

phi=0.5
v_air=0.15                      # tra 0 e 0.4
Tamb=309

Pamb=101325
fcl=1                           #(corpo nudo)
Rcl=0
cp_air = 1005           # assumo come costante
cp_bl=3850 #[J/kg*K]
cp_ve=cp_bl
cp_ar=cp_bl
rho_bl=1059 #[kg/m^3]
cp_w= 1900

body = Body()
'''
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


for i in l:
    print(i.succ)
    print(type(i.prev))
    print ('\n')
while math.fabs(trunk.Udot()) > 0.1:
    trunk.eps -= 0.01
    print ('Tint=', trunk.Tint , '[K]')
    print('eps=', trunk.eps)
    print('deltahBlod=', trunk.DeltaH_bl(), '[W]')
    print('Udot=', trunk.Udot() ,'[W]')
    print('\n')
print(w_sk(Tamb))

#----------------------------------

print('Tcomfort=', TC(Tamb))

#-------------------------------------------

n=0
for i in l:
    print(L[n])
    #print('Mvol= ', i.M_i(),'[W/m^3]')
    #print('Tsk=', i.Tsk(), '[K]')
    print('Qc=', i.Qc(),'[W]')
    print('Qr=', i.Qr(),'[W]')
    print('He=', i.He(),'[W]')
    print('H_res=', i.H_res(),'[W]')
    if i is not trunk:
        print('DeltaH blood=', i.DeltaH_bl(), '[W]')
        print('Udot=', i.Udot(), '[W]')
    else:
        delta=0
        for i in l:
            if i.doppio==0:
                delta -= i.DeltaH_bl()
            else:
                delta -= 2*i.DeltaH_bl()
        print('DeltaH blood', delta , '[kg/s]')
        print('Udot=', i.Udot() + delta, '[W]')
    print('\n')
    n+=1

print('Body')
print('M= ', body.M(),'[W]')
print('Qc=', body.Qctot(),'[W]')
print('Qr=', body.Qrtot(),'[W]')
print('He=', body.He(),'[W]')
print('H_res=', body.H_res(),'[W]')
print('Udot=', body.Udot(), '[W]')

#----------------------------------------
'''
print(TC(Tamb))

#----------------------------------------

def error_function(x):

    res = 0
    i =0  #1 #2
    
    for part in body.l:

        #part.eps = x[0]
        #part.delta = x[1]           #
        if not type(part) == Trunk:

            part.Tint = x[i]
            i = i + 1

    for part in body.l:

        res += part.Udot() ** 2

    #print(res)
    return res

import scipy.optimize as opt
import numpy as np
                                             #0.9,
res = opt.minimize(error_function, np.array([ 311.5, 310.5, 309, 308.5, 308, 309, 308.5, 308]))
print('\n')
print(res.x)

i = 0
for part in body.l:
    if not type(part) == Trunk:
        part.Tint = res.x[i]
        i+=1
'''
#-------------------------------------------------------------------

i = 0 #1  # 2
a=['head', 'neck', 'arm', 'forearm', 'hand', 'thigh', 'leg', 'foot']
print('\n')
for part in body.l:
    if not type(part) == Trunk:
        part.Tint = res.x[i]
        print(a[i],'Tsk=', part.Tsk(), '[K]')
        print(a[i],'Qc=', part.Qc(), '[W]')
        print(a[i],'Qr=', part.Qr(), '[W]')
        print(a[i],'He=', part.He(), '[W]')
        print(a[i],'H_res=', part.H_res(), '[W]')
        print( a[i],'Tint=', part.Tint,'[K]')   #f'{type(part)} ='
        print (a[i],'Udot=', part.Udot(),'[W] ,')
        print('\n')
        i = i + 1


#------------------------------------------------------------------

print('Bc' ,body.Bc(), '[W]')
print('Br', body.Br(), '[W]')
print('Bres',body.Bres(), '[W]')
print('Be',body.Be(), '[W]')
print('Bdest',body.Bdest(), '[W]')
print('rendimento',body.rendimento())


#-----------------------grafici------------------------------------

Tamb=300
v_air=0.15
phi=0.5
x=[]
y1=[]
y2=[]
y3=[]
y6=[]
y7=[]
y8=[]
y9=[]
while Tamb <=310:
    #y1.append(body.Udot())
    y2.append(body.Bdest())
    y3.append(body.rendimento())
    y6.append(body.Bc())
    y7.append(body.Br())
    y8.append(body.Bres())
    y9.append(body.Be())

    x.append(Tamb)
    Tamb += 1

plt.plot(x,y1, label="dU/dt", color="red",marker="o")
plt.xlabel("T[K]")
plt.ylabel("[W]")
plt.legend()
plt.show()

plt.plot(x,y2, label="B_dest", color="blue",marker="o")
plt.xlabel("T[K]")
plt.ylabel("B_dest[W]")
plt.legend()
plt.show()

plt.plot(x,y3, label="η", color="black",marker="o")
plt.xlabel("T[K]")
plt.ylabel("η")
plt.legend()
plt.show()

plt.plot(x,y6, label="Bc", color="orange",marker="o")
plt.xlabel("T[K]")
plt.ylabel("[W]")
plt.legend()
plt.show()

plt.plot(x,y7, label="Br", color="purple",marker="o")
plt.xlabel("T[K]")
plt.ylabel("[W]")
plt.legend()
plt.show()

plt.plot(x,y8, label="Bres", color="violet",marker="o")
plt.xlabel("T[K]")
plt.ylabel("[W]")
plt.legend()
plt.show()

plt.plot(x,y9, label="Be", color="pink",marker="o")
plt.xlabel("T[K]")
plt.ylabel("[W]")
plt.legend()
plt.show()



v_air= 0.15
phi=0
x=[]
y5=[]
while phi < 1:
    y5.append(TC(303))
    x.append(phi)
    phi += 0.1



plt.plot(x,y5, label="T_CT[K]", color="green",marker="o")
plt.xlabel("φ")
#plt.ylabel("T_CT[K]")
plt.legend()
plt.show()


v_air=0
phi=0.5
x=[]
y4=[]
while v_air <= 0.40:
    y4.append(TC(Tamb))
    x.append(v_air)
    v_air +=0.05


plt.plot(x,y4, label="T_CT", color="grey",marker="o")
plt.xlabel("v_air[m/s]")
plt.ylabel("T_CT[K]")
plt.legend()
plt.show()




temperature_int = [37]
t_sk=[]
nomi = ['Trunk', 'Head', 'Neck', 'Arm', 'Forearm', 'Hand', 'Thigh', 'Leg', 'Foot']
for i in res.x:
    temperature_int.append(i-273.15)

plt.bar(nomi, temperature_int, color="brown", width= 0.5)
plt.ylabel("T_int[°C]")
plt.show()



v_air=0.15
phi=0.5
l=[head, neck, trunk, arm, forearm, hand, thigh, leg, foot]
L=['Head', 'Neck', 'Trunk', 'Arm', 'Forearm', 'Hand', 'Thigh', 'Leg', 'Foot']
colori=["red", "blue", "black", "orange", "purple", "violet", "pink", "green", "grey"]

x=[300,301,302,303,304,305,306,307,308,309,310]
y1=[]
y2=[]
y3=[]
y4=[]
y5=[]
y6=[]
y7=[]
y8=[]
y9=[]
Y=[y1,y2,y3,y4,y5,y6,y7,y8,y9]

for i in range(len(l)):
    Tamb = 300
    while Tamb <= 310:
        Y[i].append(l[i].Qc())
        Tamb += 1
    print(Y[i])

plt.plot(x,Y[0], label= L[0], color= colori[0], marker=".")
plt.plot(x,Y[1], label= L[1], color= colori[1], marker=".")
plt.plot(x,Y[2], label= L[2], color= colori[2], marker=".")
plt.plot(x,Y[3], label= L[3], color= colori[3], marker=".")
plt.plot(x,Y[4], label= L[4], color= colori[4], marker=".")
plt.plot(x,Y[5], label= L[5], color= colori[5], marker=".")
plt.plot(x,Y[6], label= L[6], color= colori[6], marker=".")
plt.plot(x,Y[7], label= L[7], color= colori[7], marker=".")
plt.plot(x,Y[8], label= L[8], color= colori[8], marker=".")
plt.xlabel("T[K]")
plt.ylabel("Qc[W]")
plt.legend()
plt.show()

x=[300,301,302,303,304,305,306,307,308,309,310]
y1=[]
y2=[]
y3=[]
y4=[]
y5=[]
y6=[]
y7=[]
y8=[]
y9=[]
Y=[y1,y2,y3,y4,y5,y6,y7,y8,y9]

for i in range(len(l)):
    Tamb = 300
    while Tamb <= 310:
        Y[i].append(l[i].Qr())
        Tamb += 1
    print(Y[i])

plt.plot(x,Y[0], label= L[0], color= colori[0], marker=".")
plt.plot(x,Y[1], label= L[1], color= colori[1], marker=".")
plt.plot(x,Y[2], label= L[2], color= colori[2], marker=".")
plt.plot(x,Y[3], label= L[3], color= colori[3], marker=".")
plt.plot(x,Y[4], label= L[4], color= colori[4], marker=".")
plt.plot(x,Y[5], label= L[5], color= colori[5], marker=".")
plt.plot(x,Y[6], label= L[6], color= colori[6], marker=".")
plt.plot(x,Y[7], label= L[7], color= colori[7], marker=".")
plt.plot(x,Y[8], label= L[8], color= colori[8], marker=".")
plt.xlabel("T[K]")
plt.ylabel("Qr[W]")
plt.legend()
plt.show()

x=[300,301,302,303,304,305,306,307,308,309,310]
y1=[]
y2=[]
y3=[]
y4=[]
y5=[]
y6=[]
y7=[]
y8=[]
y9=[]
Y=[y1,y2,y3,y4,y5,y6,y7,y8,y9]

for i in range(len(l)):
    Tamb = 300
    while Tamb <= 310:
        Y[i].append(l[i].H_res())
        Tamb += 1
    print(Y[i])

plt.plot(x,Y[0], label= L[0], color= colori[0], marker=".")
plt.plot(x,Y[1], label= L[1], color= colori[1], marker=".")
plt.plot(x,Y[2], label= L[2], color= colori[2], marker=".")
plt.xlabel("T[K]")
plt.ylabel("Hres[W]")
plt.legend()
plt.show()

x=[300,301,302,303,304,305,306,307,308,309,310]
y1=[]
y2=[]
y3=[]
y4=[]
y5=[]
y6=[]
y7=[]
y8=[]
y9=[]
Y=[y1,y2,y3,y4,y5,y6,y7,y8,y9]

for i in range(len(l)):
    Tamb = 300
    while Tamb <= 310:
        Y[i].append(l[i].He())
        Tamb += 1
    print(Y[i])

plt.plot(x,Y[0], label= L[0], color= colori[0], marker=".")
plt.plot(x,Y[1], label= L[1], color= colori[1], marker=".")
plt.plot(x,Y[2], label= L[2], color= colori[2], marker=".")
plt.plot(x,Y[3], label= L[3], color= colori[3], marker=".")
plt.plot(x,Y[4], label= L[4], color= colori[4], marker=".")
plt.plot(x,Y[5], label= L[5], color= colori[5], marker=".")
plt.plot(x,Y[6], label= L[6], color= colori[6], marker=".")
plt.plot(x,Y[7], label= L[7], color= colori[7], marker=".")
plt.plot(x,Y[8], label= L[8], color= colori[8], marker=".")
plt.xlabel("T[K]")
plt.ylabel("He[W]")
plt.legend()
plt.show()
'''



