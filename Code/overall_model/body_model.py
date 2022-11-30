from Code.body_parts.subclasses.head import Head


class Body:
    def __init__(self):

        self.altezza = 1.76
        self.peso = 76
        self.sesso = 1  # 1=maschio,0=femmina
        self.eta = 25
        self.Atot = 1.8

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
        A = 0
        for i in self.l:
            if i.doppio == 0:
                A += i.area_s()
            else:
                A += 2 * i.area_s()
        return A

    def Area_tot(self):
        A = 0
        for i in self.l:
            if i.doppio == 0:
                A += i.area()
            else:
                A += 2 * i.area()
        return A

    def Vol_tot(self):
        V = 0
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

        return M * 4184 / 86400

    def Qctot(self):  # calore scambiato per convezione                  #ASHRAE
        Q = 0
        for i in l:
            if i.doppio == 0:
                Q += i.Qc()
            else:
                Q += i.Qc() * 2
        return Q

    def Qctot_iter(self, T):  # calore scambiato per convezione                  #ASHRAE
        Q = 0
        for i in l:
            if i.doppio == 0:
                Q += i.Qc_iter(T)
            else:
                Q += i.Qc_iter(T) * 2
        return Q

    def Qrtot(self):  # calore scambiato per irraggiamento
        Q = 0
        for i in self.l:
            if i.doppio == 0:
                Q += i.Qr()
            else:
                Q += 2 * i.Qr()
        return Q

    def Qrtot_iter(self, T):  # calore scambiato per irraggiamento
        Q = 0
        for i in self.l:
            if i.doppio == 0:
                Q += i.Qr_iter(T)
            else:
                Q += 2 * i.Qr_iter(T)
        return Q

    def He(self):  # calore scambiato per evaporazione
        H = 0  # nel modello EES la Rcl è 10, non capisco perchè
        for i in self.l:  # essendo a riposo e cercando una T per cui U_dot = 0 pensavo di mettere la w minima
            if i.doppio == 0:
                H += i.He()
            else:
                H += 2 * i.He()
        return H

    def He_iter(self, T):
        H = 0
        for i in self.l:
            if i.doppio == 0:
                H += i.He_iter(T)
            else:
                H += 2 * i.He_iter(T)
        return H

    def m_dot_res(self):
        m_dot_res = 1.433 * self.Atot * self.M() * (10 ** (-5))
        return m_dot_res

    def H_res(self):
        H_res = ((0.0014 * Body().M() * (34 - Tamb + 273.15)) + (
                    0.0173 * Body().M() * (5.87 - Pvap(Tamb)))) * self.Area_tot_scambio()  # da ASHRAE
        return H_res

    def H_res_iter(self, T):
        H_res = ((0.0014 * Body().M() * (34 - Tamb + 273.15)) + (
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
        mw_ = 3 * 10 ** (
            -6) * 1000  # ipotizzata al valore minimo con 0.3*10^-6, valore 3 in linea con articlo di ferreira
        h_lv = 2260  # kJ/K
        s_lv = 6.056  # kJ/kg*K
        R_w = 0.46151  # kJ/kg*K
        Be = mw_ * (h_lv - Tamb * s_lv) + mw_ * R_w * Tamb * math.log((Pvap(self.mean_Tsk()) / Pvap(Tamb)))
        return Be

    def Bres(self):
        R_w = 461.51  # J/kg*K
        Tex = trunk.Tint
        deltaB_air = self.m_dot_res() * (cp_air * (Tex - Tamb - Tamb * math.log(
            (Tex / Tamb))))  # semplificazioni dovute al fatto che T0==Tamb e P0==Pamb
        deltaB_wat = self.m_dot_res() * omegax(Pvap(Tex)) * (
                    cp_w * (Tex - Tamb - Tamb * math.log((Tex / Tamb))) + R_w * Tamb * math.log(
                (Pvap(Tex) / Pvap(Tamb))))  # semplificazioni dovute al fatto che T0==Tamb e P0==Pamb
        return deltaB_air - deltaB_wat

    def Bdest(self):
        return self.M() - (self.Bc() + self.Br() + self.Bres() + self.Be()) - self.W()

    def rendimento(self):
        rend = 1 - (Body().Bdest() / Body().M())
        return rend
