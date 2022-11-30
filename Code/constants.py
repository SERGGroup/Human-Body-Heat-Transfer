import math


class Constants:

    Pamb = 101325
    fcl = 1  # (corpo nudo)
    Rcl = 0
    cp_air = 1005  # assumo come costante
    cp_bl = 3850  # [J/kg*K]
    rho_bl = 1059  # [kg/m^3]
    cp_w = 1900
    cp_ve = cp_bl

def omegax(Px):
    omega = 0.622 * ((Px) / (Constants.Pamb - Px))
    return omega


def Pvap(T):
    P = (math.exp(18.956 - (4030.18 / (T - 38.15)))) / 10  # eq Antoine, conversione da Human Thermal enviroment pag 15
    return P

