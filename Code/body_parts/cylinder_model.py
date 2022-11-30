import math

class Cylinder:
    def __init__(self, d, h, prev=None):
        self.r = d / 200
        self.h = h/ 100
        self.delta=0.90

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
