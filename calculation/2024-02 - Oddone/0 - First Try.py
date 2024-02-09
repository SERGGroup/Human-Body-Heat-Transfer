#%% ----- IMPORT MODULES -----

from main_code.cylinder_model.cylinder import Cylinder, CylinderGeometry, CylinderCoefficients, EnvironmentalConditions
from main_code.body_class import Body
# from main_code.cylinder_model.support.environmental_conditions import EnvironmentalConditions
import matplotlib.pyplot as plt


#&& ----- PLOTS -----

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

#%% ----- OBJECT'S CREATION
tommaso_env_conditions = EnvironmentalConditions()
tommaso_env_conditions.set_conditions(temperature=288, pressure = 101325, humidity = 0.5)
tommaso = Body()
coefficent_cylinder = CylinderCoefficients(tommaso)
geometry_cylinder = CylinderGeometry(d=0.2, h=0.61, s=0.2)
trunk = Cylinder(geometry_cylinder, tommaso, coefficent_cylinder, tommaso_env_conditions)

delta_t = 1  # Intervallo di tempo in secondi
times, temperatures = simulate_temperature_evolution(trunk, delta_t, max_steps=60*60*24)


plt.plot(times, temperatures, marker='o', linestyle='-')
plt.xlabel('Time (s)')
plt.ylabel('Internal Temperature (K)')
plt.title('Change in internal temperature over time')
plt.grid(True)
plt.show()

#%% ---- TEST CODE -----

print ('il valore del calore scambiato per conduzione vale: ',trunk.Q_cond())
print('il valore del calore scambiato per convezione vale: ', trunk.Q_conv())
print('il valore del calore scambiato per irraggiamento vale: ', trunk.Q_irr())
print('il valore finale della T_int è: ', trunk.energy_balance(delta_t=60*60))



















