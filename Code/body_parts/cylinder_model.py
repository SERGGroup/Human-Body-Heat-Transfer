from Code.constants import Constants as cst, Pvap
import math

class Cylinder:

    def __init__(self, d, h, body, prev=None, delta=0.9):

        self.r = d / 200
        self.h = h / 100
        self.delta = delta
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
        if self.body.v_air<= 0.2:
            Qc = self.hc * self.area_s() * (self.Tsk() - self.body.Tamb) * cst.fcl
        else:
            hc= 8.3 * (self.body.v_air**0.5)                  #ASHRAE
            Qc = hc * self.area_s() * (self.Tsk() - self.body.Tamb) * cst.fcl
        return Qc

    def Qc_iter (self,T):
        if self.body.v_air <= 0.2:
            Qc = self.hc * self.area_s() * (self.Tsk() - T) * cst.fcl
        else:
            hc = 8.3 * (self.body.v_air ** 0.5)  # ASHRAE
            Qc = hc * self.area_s() * (self.Tsk() - T) * cst.fcl
        return Qc

    def Qr(self):
        sigma= 5.67*(10**(-8))
        eps_pelle= 0.95
        Qr =  sigma * self.area_s() * eps_pelle * ((self.Tsk()**4) - (self.body.Tamb**4)) * cst.fcl * 0.73                 #termine preso da Fagner,
        return Qr                                                                                   #è il rapporto tra l'area effettivamente sottoposta
                                                                                                    # a scambio termico per radiazione e l'area di DuBois
    def Qr_iter (self,T):
        sigma = 5.67 * (10 ** (-8))
        eps_pelle = 0.95
        Qr = sigma * self.area_s() * eps_pelle * ((self.Tsk() ** 4) - (T ** 4)) * cst.fcl * 0.73
        return Qr

    def He(self):
        P1 = Pvap(self.Tsk())
        P2 = Pvap(self.body.Tamb)
        w = self.body.w_sk(self.body.Tamb)
        if self.body.v_air <= 0.2:
            he= 16.5 * self.hc
        else:
            he= 8.3 * (self.body.v_air**0.5) * 16.5
        He = self.area_s() * (P1 - (self.body.phi * P2)) * w / ((cst.Rcl + (1 / (cst.fcl * he))))
        return He

    def He_iter(self,T):
        P1 = Pvap(self.Tsk())
        P2 = Pvap(T)
        w = 0.006
        if self.body.v_air <= 0.2:
            he= 16.5 * self.hc
        else:
            he= 8.3 * (self.body.v_air**0.5) * 16.5
        He = self.area_s() * (P1 - (self.body.phi * P2)) * w / ((cst.Rcl + (1 / (cst.fcl * he))))
        return He

    def H_res(self):

        return 0.

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
        delta= -(0.001 * self.v_dot_bl /60) * cst.rho_bl * cst.cp_ve * DT * self.eps
        return delta

    def M_i(self):
        return self.body.M() * self.volume() / self.body.Vol_tot()

    def Udot(self):
        Udot = self.M_i() - (self.Qc() + self.Qr() + self.He() + self.H_res()) + self.DeltaH_bl()
        return Udot
