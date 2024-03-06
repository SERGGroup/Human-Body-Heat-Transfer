# %% ----- IMPORT MODULES -----

from main_code.cylinder_model.cylinder import Cylinder, CylinderGeometry, CylinderCoefficients, EnvironmentalConditions
from main_code.body_class import Body
from matplotlib import pyplot as plt
import numpy as np


# && ----- PLOTS -----

def simulate_temperature_evolution(cylinder, delta_t, max_steps=10):
    times = []
    temperatures = []

    current_time = 0
    while current_time < max_steps:
        times.append(current_time + delta_t)  # Tempo in secondi
        temperatures.append(cylinder.T_int)

        cylinder.energy_balance(delta_t)

        current_time += delta_t

    return times, temperatures


# %% ----- OBJECT'S CREATION
tommaso = Body()
tommaso_env_conditions = EnvironmentalConditions(tommaso)
tommaso_env_conditions.set_conditions(temperature=299.15, pressure=101325, humidity=0.5)
tommaso_env_conditions.calculate_properties()
coefficient_cylinder = CylinderCoefficients(tommaso, tommaso_env_conditions)
geometry_cylinder = CylinderGeometry(d=0.2, h=0.8, s=0.2)
trunk = Cylinder(geometry_cylinder, tommaso, coefficient_cylinder, tommaso_env_conditions)

delta_t = 1  # Intervallo di tempo in secondi
times, temperatures = simulate_temperature_evolution(trunk, delta_t, max_steps=60 * 60 * 24)

plt.plot(times, temperatures, linestyle='-')
plt.xticks(np.arange(0, len(times) + 1, step=60 * 60 * 2), labels=np.arange(0, 25, 2))
plt.xlabel('Time (hr)')
plt.ylabel('Internal Temperature (K)')
plt.title('Change in internal temperature over time')
plt.grid(True)
plt.show()

# %% ---- TEST CODE -----

print('il valore del calore scambiato per conduzione vale: ', trunk.Q_cond(), '[W]')
print('il valore del calore scambiato per convezione vale: ', trunk.Q_conv(), '[W]')
print('il valore del calore scambiato per irraggiamento vale: ', trunk.Q_irr(), '[W]')
print('il valore del calore perso per evaporazione vale: ', trunk.E_sk(), '[W]')
print('il valore del calore scambiato attraverso il sangue vale: ', trunk.Q_blood(), '[W]')
print('il valore del lavoro utilizzando per pompare il sangue vale: ', trunk.W_pump_blood(), '[W]')
print('il valore finale della T_int è: ', trunk.energy_balance(delta_t=60*60), '[K]')

