from Code.body_parts.subclasses.head import Head
from Code.body_parts.subclasses.neck import Neck
from Code.body_parts.subclasses.trunk import Trunk
from Code.body_parts.subclasses.arm import Arm
from Code.body_parts.subclasses.forearm import Forearm
from Code.body_parts.subclasses.hand import Hand
from Code.body_parts.subclasses.thigh import Thigh
from Code.body_parts.subclasses.leg import Leg
from Code.body_parts.subclasses.foot import Foot
from Code.constants import Constants as cst, Pvap, omegax
import math
import scipy.optimize as opt
import numpy as np



class Body:
    def __init__(self, altezza=1.8):

        self.__init__body_parts()

        self.altezza = altezza
        self.peso = 76
        self.sesso = 1        # 1=maschio,0=femmina
        self.eta = 25
        self.Atot = 1.8

        self.Tamb= 309
        self.phi= 0.5
        self.v_air= 0.15

    def __init__body_parts(self):

        trunk = Trunk(26.0, 79.8, self)
        neck = Neck(11.4, 8.3, self, trunk)
        head = Head(14.6, 20.7, self, neck)
        arm = Arm (9.0, 35.3,self,trunk)
        forearm= Forearm(7.4, 29.2,self, arm)
        hand= Hand(4.6, 30.0, self, forearm)
        thigh= Thigh(13.4, 35.2, self, trunk)
        leg= Leg(8.6, 37.9, self, thigh)
        foot= Foot(7.2, 24.1, self, leg)
        self.body_parts = [head, neck, trunk, arm, forearm, hand, thigh, leg, foot]

    def Area_tot_scambio(self):
        A = 0
        for i in self.body_parts:
            if i.doppio == 0:
                A += i.area_s()
            else:
                A += 2 * i.area_s()
        return A

    def Area_tot(self):
        A = 0
        for i in self.body_parts:
            if i.doppio == 0:
                A += i.area()
            else:
                A += 2 * i.area()
        return A

    def Vol_tot(self):
        V = 0
        for i in self.body_parts:
            if i.doppio == 0:
                V += i.volume()
            else:
                V += 2 * i.volume()
        return V

    # self.eta = età anagrafica
    def M(self):
        if self.sesso == 1:
            M = 66.5 + 13.8 * self.peso + 5 * self.altezza * 100 - 6.8 * self.eta
        else:
            M = 65.51 + 9.6 * self.peso + 1.8 * self.altezza * 100 - 4.7 * self.eta

        return M * 4184 / 86400

    def Qctot(self):  # calore scambiato per convezione                  #ASHRAE
        Q = 0
        for i in self.body_parts:
            if i.doppio == 0:
                Q += i.Qc()
            else:
                Q += i.Qc() * 2
        return Q

    def Qctot_iter(self, T):  # calore scambiato per convezione                  #ASHRAE
        Q = 0
        for i in self.body_parts:
            if i.doppio == 0:
                Q += i.Qc_iter(T)
            else:
                Q += i.Qc_iter(T) * 2
        return Q

    def Qrtot(self):  # calore scambiato per irraggiamento
        Q = 0
        for i in self.body_parts:
            if i.doppio == 0:
                Q += i.Qr()
            else:
                Q += 2 * i.Qr()
        return Q

    def Qrtot_iter(self, T):  # calore scambiato per irraggiamento
        Q = 0
        for i in self.body_parts:
            if i.doppio == 0:
                Q += i.Qr_iter(T)
            else:
                Q += 2 * i.Qr_iter(T)
        return Q

    def He(self):  # calore scambiato per evaporazione
        H = 0  # nel modello EES la Rcl è 10, non capisco perchè
        for i in self.body_parts:  # essendo a riposo e cercando una T per cui U_dot = 0 pensavo di mettere la w minima
            if i.doppio == 0:
                H += i.He()
            else:
                H += 2 * i.He()
        return H

    def He_iter(self, T):
        H = 0
        for i in self.body_parts:
            if i.doppio == 0:
                H += i.He_iter(T)
            else:
                H += 2 * i.He_iter(T)
        return H

    def m_dot_res(self):
        m_dot_res = 1.433 * self.Atot * self.M() * (10 ** (-5))
        return m_dot_res

    def H_res(self):
        H_res = ((0.0014 * Body().M() * (34 - self.Tamb + 273.15)) + (
                    0.0173 * Body().M() * (5.87 - Pvap(self.Tamb)))) * self.Area_tot_scambio()  # da ASHRAE
        return H_res

    def H_res_iter(self, T):
        H_res = ((0.0014 * Body().M() * (34 - self.Tamb + 273.15)) + (
                    0.0173 * Body().M() * (5.87 - Pvap(T)))) * self.Area_tot_scambio()  # da ASHRAE
        return H_res

    def W(self):
        W = 0  # corpo a riposo
        return W

    def Udot(self):
        Udot = Body().M() - (Body().Qctot() + Body().Qrtot() + Body().He() + Body().H_res()) - Body().W()
        return Udot

    def Udot_iter(self, T):
        Udot = Body().M() - (
                    Body().Qctot_iter(T) + Body().Qrtot_iter(T) + Body().He_iter(T) + Body().H_res_iter(T)) - Body().W()
        return Udot

    def Br(self):
        Br = 0
        for i in self.body_parts:
            B = i.Qr() * (1 - (self.Tamb / i.Tsk()))
            if i.doppio == 0:
                Br += B
            else:
                Br += 2 * B
        return Br

    def Bc(self):
        Bc = 0
        for i in self.body_parts:
            B = i.Qc() * (1 - (self.Tamb / i.Tsk()))
            if i.doppio == 0:
                Bc += B
            else:
                Bc += 2 * B
        return Bc

    def mean_Tsk(self):
        T = 0
        for i in self.body_parts:
            if i.doppio == 0:
                T += i.Tsk()
            else:
                T += 2 * i.Tsk()
        return T / 15

    def Be(self):
        mw_ = 3 * 10 ** (-6) * 1000
        h_lv = 2260
        s_lv = 6.056
        R_w = 0.46151
        Be = mw_ * (h_lv - self.Tamb * s_lv) + mw_ * R_w * self.Tamb * math.log((Pvap(self.mean_Tsk()) / Pvap(self.Tamb)))
        return Be

    def Bres(self):
        R_w = 461.51  # J/kg*K
        Tex = 310.15
        deltaB_air = self.m_dot_res() * (cst.cp_air * (Tex - self.Tamb - self.Tamb * math.log((Tex / self.Tamb))))
        deltaB_wat = self.m_dot_res() * omegax(Pvap(Tex)) * (cst.cp_w * (Tex - self.Tamb - self.Tamb * math.log((Tex / self.Tamb))) + R_w * self.Tamb * math.log((Pvap(Tex) / Pvap(self.Tamb))))
        return deltaB_air + deltaB_wat

    def Bdest(self):
        return self.M() - (self.Bc() + self.Br() + self.Bres() + self.Be()) - self.W()

    def rendimento(self):
        rend = 1 - (Body().Bdest() / Body().M())
        return rend

    def error_function(self, x):

        res = 0
        i = 0  # 1 #2

        for part in self.body_parts:

            if not type(part) == Trunk:
                part.Tint = x[i]
                i = i + 1

        for part in self.body_parts:
            res += part.Udot() ** 2

        return res

    def aggiorna_Tint(self):
        res = opt.minimize(self.error_function, np.array([311.5, 310.5, 309, 308.5, 308, 309, 308.5, 308]))

        i = 0
        for part in self.body_parts:
            if not type(part) == Trunk:
                part.Tint = res.x[i]
                i += 1

    def TC(self, t, T1=310, T2=290):
        T = t
        if math.fabs(self.Udot_iter(t)) > 1:

            if self.Udot_iter(t) < 0:

                T = (t + T1) / 2
                return self.TC(T, T1, t)

            else:

                T = (t + T2) / 2
                return self.TC(T, t, T2)
        else:
            return T

    def w_sk(self, Tamb):  # parametro

        T = self.TC(Tamb)  # 303

        if Tamb <= T:  # in K

            w = 0.006

        else:

            w = 0.006 + 0.009 * (Tamb - T)

        return w


