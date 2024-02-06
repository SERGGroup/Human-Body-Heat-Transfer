#%% ----- IMPORT MODULES -----

from main_code.cylinder_model.cylinder import Cylinder, CylinderGeometry, CylinderCoefficients
from main_code.body_class import Body
import matplotlib.pyplot as plt

#&& ----- PLOTS -----

def simulate_temperature_evolution(cylinder, delta_t, max_steps=10):
    times = []
    temperatures = []

    current_time = 0
    while current_time < max_steps:
        times.append(current_time * delta_t)  # Tempo in secondi
        temperatures.append(cylinder.T_int)

        cylinder.energy_balance(delta_t)
        current_time += 1

    return times, temperatures

#%% ----- OBJECT'S CREATION
tommaso = Body()
coefficent_cylinder = CylinderCoefficients(tommaso)
geometry_cylinder = CylinderGeometry(d=0.2,h=0.8,s=00.2)
trunk = Cylinder(geometry_cylinder, tommaso, coefficent_cylinder)

delta_t = 60  # Intervallo di tempo in secondi
times, temperatures = simulate_temperature_evolution(trunk, delta_t)

plt.plot(times, temperatures, marker='o', linestyle='-')
plt.xlabel('Tempo (secondi)')
plt.ylabel('Temperatura interna (K)')
plt.title('Variazione della temperatura interna nel tempo')
plt.grid(True)
plt.show()

#%% ---- TEST CODE -----

print ('il valore del calore scambiato per conduzione vale: ',trunk.Q_cond())
print('il valore del calore scambiato per convezione vale: ', trunk.Q_conv())
print('il valore del calore scambiato per irraggiamento vale: ', trunk.Q_irr())
print('il valore finale della T_int è: ', trunk.energy_balance(delta_t=60*60))



















