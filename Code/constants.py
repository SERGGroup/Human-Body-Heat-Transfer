import math


class Constants:
    def __init__(self):
        self.Pamb = 101325
        self.fcl = 1  # (corpo nudo)
        self.Rcl = 0
        self.cp_air = 1005  # assumo come costante
        self.cp_bl = 3850  # [J/kg*K]
        self.rho_bl = 1059  # [kg/m^3]
        self.cp_w = 1900

    def omegax(self,Px):
        omega = 0.622 * ((Px) / (self.Pamb - Px))
        return omega

    def Pvap(self, T):
        P = (math.exp(18.956 - (4030.18 / (T - 38.15)))) / 10  # eq Antoine, conversione da Human Thermal enviroment pag 15
        return P

    def TC(self, t, T1=310, T2=290):
        T = t
        if math.fabs(body.Udot_iter(t)) > 1:
            if body.Udot_iter(t) < 0:
                T = (t + T1) / 2
                return self.TC(T, T1, t)


            else:
                T = (t + T2) / 2
                return self.TC(T, t, T2)
        else:
            return T

    def w_sk(self,Tamb):  # parametro
        T = self.TC(Tamb)  # 303
        if Tamb <= T:  # in K
            w = 0.006
        else:
            w = 0.006 + 0.009 * (Tamb - T)
        return w
