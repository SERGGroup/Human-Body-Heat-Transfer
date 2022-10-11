import math


class Cylinder:
    def __init__(self, d, h):
        self.r = d / 2
        self.h = h

    def volume(self):
        return (math.pi * self.h * self.r ** 2) / 1000000

    def area_s(self):
        return (math.pi * self.r * 2 * self.h) / 10000

    def area(self):
        return ((math.pi * self.r * 2 * self.h) + (math.pi * 4 * self.r ** 2)) / 10000

    def Qc(self):
        Qc = self.hc * self.area_s() * (Tsk - Tamb) * fcl
        return Qc

    def Qr(self):
        Qr = self.hr * self.area_s() * (Tsk - Tamb) * fcl
        return Qr

    


class Head(Cylinder):
    def __init__(self, d, h):
        super().__init__(d, h)

        self.hr = 4.1
        self.hc = 3.6
        self.he = 5.9
        self.doppio = 0


class Neck(Cylinder):
    def __init__(self, d, h):
        super().__init__(d, h)

        self.hr = 4.1
        self.hc = 3.6
        self.he = 5.9
        self.doppio = 0


class Trunk(Cylinder):
    def __init__(self, d, h):
        super().__init__(d, h)

        self.hr = 4.4
        self.hc = 3.2
        self.he = 5.3
        self.doppio = 0


class Arm(Cylinder):
    def __init__(self, d, h):
        super().__init__(d, h)

        self.hr = 5.2
        self.hc = 2.9
        self.he = 4.8
        self.doppio = 1


class Forearm(Cylinder):
    def __init__(self, d, h):

        super().__init__(d, h)
        self.hr = 4.9
        self.hc = 3.7
        self.he = 6.1
        self.doppio = 1


class Hand(Cylinder):
    def __init__(self, d, h):

        super().__init__(d, h)
        self.hr = 4.1
        self.hc = 4.1
        self.he = 6.8
        self.doppio = 1


class Thigh(Cylinder):
    def __init__(self, d, h):

        super().__init__(d, h)
        self.hr = 4.3
        self.hc = 4.1
        self.he = 6.8
        self.doppio = 1


class Leg(Cylinder):
    def __init__(self, d, h):

        super().__init__(d, h)
        self.hr = 5.3
        self.hc = 4.1
        self.he = 6.8
        self.doppio = 1


class Foot(Cylinder):
    def __init__(self, d, h):
        super().__init__(d, h)

        self.hr = 3.9
        self.hc = 5.1
        self.he = 8.4
        self.doppio = 1


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
        for i in self.l:
            A = 0
            if i.doppio == 0:
                A += i.area_s()
            else:
                A += 2 * i.area_s()
        return A


    def Area_tot(self):
        for i in self.l:
            A = 0
            if i.doppio == 0:
                A += i.area()
            else:
                A += 2 * i.area()
        return A


    def Qctot(self):  # calore scambiato per convezione
        Q = 0
        for i in self.l:
            if i.doppio == 0:
                Q += i.Qc()
            else:
                Q += 2 * i.Qc()
        return Q


    def Qrtot(self):  # calore scambiato per irraggiamento
        Q = 0
        for i in self.l:
            if i.doppio == 0:
                Q += i.Qr()
            else:
                Q += 2 * i.Qr()
        return Q

    def He(self):  # calore scambiato per evaporazione
        H = 0  # nel modello EES la Rcl è 10, non capisco perchè
        P1 = Pvap(Tsk)  # mettendo Rcl=10 ottengo un risultato simile a quello di EES
        P2 = Pvap(Tamb)
        w = w_sk(Tamb)
        for i in self.l:
            He = i.area_s() * (P1 - (phi * P2)) * 0.06 / ((10 + (1 / (fcl * i.he))))
            if i.doppio == 0:
                H += He
            else:
                H += 2 * He
        return H

    def m_dot_res(self):
        m_dot_res= 1.433 * self.Atot * Body().M() * (10 ** (-6))
        return m_dot_res


    def DeltaH_res(self):
        DeltaH_res = (Body().m_dot_res() * cp_air * (Texp - Tixp)) + (Body().m_dot_res() * ((omegax(Pvap(Texp)) * hvap(Texp)) - (omegax(Pvap(Tixp)) * hvap(Tixp))))
        return DeltaH_res

    def M(self):
        if self.sesso == 1:
            M = 66.5 + 13.8 * self.peso + 5 * self.altezza * 100 - 6.8 * self.eta
        else:
            M = 65.51 + 9.6 * self.peso + 1.8 * self.altezza * 100 - 4.7 * self.eta
        return M * 4184 / 86400


    def W(self):
        W=0             #corpo a riposo
        return W
    def Udot(self):
        Udot = Body().M() - (Body().Qctot() + Body().Qrtot() + Body().He() + Body().DeltaH_res()) - Body().W()
        return Udot


def Pvap(T):
    P = 611.2 * math.exp((40650 / 8.314) * ((1 / 273.15) - (1 / T)))  # equazione di Clapeyron
    return P


def w_sk(Tamb):  # parametro
    if Tamb < 304:  # in K
        w = 0.009 * Tamb - 2.577
    else:
        w = 0.122 * Tamb - 36.816
    return w

def hvap(T):
    t = T - 273.15
    if t >= 0 and t < 10:
        hvap = 42.117 * t / 10
    elif t >= 10 and t < 20:
        hvap = 42.117 + ((84.012 - 42.117) * (t - 10) / 10)
    elif t >= 20 and t < 30:
        hvap = 84.012 + ((125.883 - 84.012) * (t - 20) / 10)
    elif t >= 30 and t <= 40:
        hvap = 125.883 + ((167.623 - 125.883) * (t - 30) / 10)
    return hvap * 1000

def omegax(Px):
    omega = 0.622 * ((Px) / (Pamb - Px))
    return omega





Pamb=101325
Tamb=302.5
Tsk=306.5
fcl=1 #(corpo nudo)
Rcl=0
phi=0.5
cp_air = 1005           # assumo come costante
Texp = Tsk + 1          # temperatura aria espirata da assumere (come la assumo??)
Tixp = Tamb             # ipotesi fatta da me
phi_exp = 0.9           # umidità relativa
phi_ixp = phi           # umidità relativa









print('Qctot=', Body().Qctot(),'[W]')
print('Qrtot=', Body().Qrtot(),'[W]')
print('He=', Body().He(),'[W]')
print('mres=', Body().m_dot_res(),'[kg/s]')
print('DeltaH=', Body().DeltaH_res(),'[W]')
print('Udot=',Body().Udot(),'[W]')