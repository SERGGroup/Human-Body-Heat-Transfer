from main_code.cylinder_model.cylinder import Cylinder


class Blood:
    def __init__(self, cylinder: Cylinder):
        self.cylinder = cylinder
        # super().__init__()

    def get_volumetric_bood_rate(self):
        return ((10 * self.cylinder.T_int) + (
                    1 * self.body.T_skin)) / 60000000  #[m^3/s]: correlation founded in an article on the internet

    def get_rho_blood(self):
        return 1050  # [Kg/m^3]; assuming blood is an incompressible fluid

    def calculate_mass_blood_rate(self):
        return self.get_rho_blood() * self.get_volumetric_bood_rate()  # [Kg/s]

    def get_blood_delta_P(self):
        return 16000  # [Pa]

    def calculate_blood_delta_h(self):  # dH = Cv*dT + V*dP ;assuming an isotermal increase of pressure
        return (self.get_rho_blood()) ** (-1) * self.get_blood_delta_P()  # [J/Kg]

    def efficiency_pump(self):
        return 0.25


if __name__ == '__main__':
    blood = Blood(cylinder=Cylinder())
    print(blood.get_volumetric_blood_rate())
