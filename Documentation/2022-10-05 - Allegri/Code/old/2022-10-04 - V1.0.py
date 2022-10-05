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
        self.r = d / 2
        self.h = h
        self.hr = 4.1
        self.hc = 3.6
        self.he = 5.9
        self.doppio = 0


class Trunk(Cylinder):
    def __init__(self, d, h):
        self.r = d / 2
        self.h = h
        self.hr = 4.4
        self.hc = 3.2
        self.he = 5.3
        self.doppio = 0


class Arm(Cylinder):
    def __init__(self, d, h):
        self.r = d / 2
        self.h = h
        self.hr = 5.2
        self.hc = 2.9
        self.he = 4.8
        self.doppio = 1


class Forearm(Cylinder):
    def __init__(self, d, h):
        self.r = d / 2
        self.h = h
        self.hr = 4.9
        self.hc = 3.7
        self.he = 6.1
        self.doppio = 1


class Hand(Cylinder):
    def __init__(self, d, h):
        self.r = d / 2
        self.h = h
        self.hr = 4.1
        self.hc = 4.1
        self.he = 6.8
        self.doppio = 1


class Thigh(Cylinder):
    def __init__(self, d, h):
        self.r = d / 2
        self.h = h
        self.hr = 4.3
        self.hc = 4.1
        self.he = 6.8
        self.doppio = 1


class Leg(Cylinder):
    def __init__(self, d, h):
        self.r = d / 2
        self.h = h
        self.hr = 5.3
        self.hc = 4.1
        self.he = 6.8
        self.doppio = 1


class Foot(Cylinder):
    def __init__(self, d, h):
        self.r = d / 2
        self.h = h
        self.hr = 3.9
        self.hc = 5.1
        self.he = 8.4
        self.doppio = 1


Atot = 1.8
Pamb = 101325
Tamb = 293
Tsk = 307
fcl = 1  # (corpo nudo)
Rcl = 0
phi = 0.6
altezza = 1.76
peso = 76
sesso = 1  # 1=maschio,0=femmina
eta = 25

head = Head(14.6, 20.7)  # misure prese da Takemori et al. per persona di 1,76 m,
neck = Neck(11.4, 8.3)  # da trovare relazioni fra i diversi raggi e tra un raggio
trunk = Trunk(26.0, 79.8)  # di riferimento (tronco) e l'altezza del campione ?
arm = Arm(9.0, 35.3)
forearm = Forearm(7.4, 29.2)
hand = Hand(4.6, 30.0)
thigh = Thigh(13.4, 35.2)
leg = Leg(8.6, 37.9)
foot = Foot(7.2, 24.1)

body = [head, neck, trunk, arm, forearm, hand, thigh, leg, foot]

'''
class Body:
    def __init__(self):
        self.l=body'''


def Area_tot_scambio(body):
    for i in body:
        A = 0
        if i.doppio == 0:
            A += i.area_s()
        else:
            A += 2 * i.area_s()
    return A


def Area_tot(body):
    for i in body:
        A = 0
        if i.doppio == 0:
            A += i.area()
        else:
            A += 2 * i.area()
    return A


def Qctot(body):  # calore scambiato per convezione
    Q = 0
    for i in body:
        Qc = i.hc * i.area_s() * (Tsk - Tamb) * fcl
        if i.doppio == 0:
            Q += Qc
        else:
            Q += 2 * Qc
    return Q


def Qrtot(body):  # calore scambiato per irraggiamento
    Q = 0
    for i in body:
        Qr = i.hr * i.area_s() * (Tsk - Tamb) * fcl
        if i.doppio == 0:
            Q += Qr
        else:
            Q += 2 * Qr
    return Q


def Pvap(T):
    P = 1000 * math.exp((40650 / 8.314) * ((1 / 280.12) - (1 / T)))  # equazione di Clapeyron
    return P


def w_sk(Tamb):  # parametro
    if Tamb < 304:  # in K
        w = 0.009 * Tamb - 2.577
    else:
        w = 0.122 * Tamb - 36.816
    return w


def He(Tamb, Tsk, phi, body):  # calore scambiato per evaporazione
    H = 0  # nel modello EES la Rcl è 10, non capisco perchè
    P1 = Pvap(Tsk)  # mettendo Rcl=10 ottengo un risultato simile a quello di EES
    P2 = Pvap(Tamb)
    w = w_sk(Tamb)
    for i in body:
        He = i.area_s() * (P1 - (phi * P2)) * w / ((Rcl + (1 / (fcl * i.he))))
        if i.doppio == 0:
            H += He
        else:
            H += 2 * He
    return H


def M(altezza, eta, peso, sesso):
    if sesso == 1:
        M = 66.5 + 13.8 * peso + 5 * altezza - 6.8 * eta
    else:
        M = 65.51 + 9.6 * peso + 1.8 * altezza - 4.7 * eta
    return M


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
    return hvap * 1000  # [J]


cp_air = 1005  # assumo come costante
Texp = Tsk + 1  # temperatura aria espirata da assumere (come la assumo??)
Tixp = Tamb  # ipotesi fatta da me
phi_exp = 0.9  # umidità relativa
phi_ixp = phi  # umidità relativa
Pvap_ixp = Pvap(Tixp)
Pvap_exp = Pvap(Texp)
omega_ixp = 0.622 * ((Pvap_ixp) / (Pamb - Pvap_ixp))
omega_exp = 0.622 * ((Pvap_exp) / (Pamb - Pvap_exp))
m_dot_res = 1.433 * Atot * M(altezza, eta, peso, sesso) * (10 ** (-6))


def DeltaH_res(cp_air, Texp, Tixp, phi_exp, phi_ixp, omega_ixp, omega_exp):
    DeltaH_res = m_dot_res * cp_air * (Texp - Tixp) + m_dot_res * ((omega_exp * hvap(Texp)) - (omega_ixp * hvap(Tixp)))
    return DeltaH_res


print('Qctot=', Qctot(body))
print('Qrtot=', Qrtot(body))
print('He=', He(Tamb, Tsk, phi, body))
print('mres=', m_dot_res)
print('DeltaH=', DeltaH_res(cp_air, Texp, Tixp, phi_exp, phi_ixp, omega_ixp, omega_exp))
