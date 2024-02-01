#%% ----- IMPORT MODULES -----

from main_code.cylinder_model.cylinder import Cylinder, CylinderGeometry, CylinderCoefficients
from main_code.body_class import Body

#%% ----- OBJECTS' CREATION -----
tommaso = Body()
coefficenti_cilindro = CylinderCoefficients(tommaso)
geometria_tronco = CylinderGeometry(d=0.2,h=0.8,s=0.2)
tronco = Cylinder(geometria_tronco, tommaso, coefficenti_cilindro)

#%% ---- TEST CODE -----

print('la temperatura prima dello scambio termico vale: ', tronco.T_int)
print ('il valore del calore scambiato per conduzione vale: ',tronco.Q_cond())
print('il valore del calore scambiato per convezione vale: ', tronco.Q_conv())
print('il valore del calore scambiato per irraggiamento vale: ', tronco.Q_irr())
print('il valore finale della T_int è: ', tronco.energy_balance(delta_t=10))

#the final value of T_int is negative

















