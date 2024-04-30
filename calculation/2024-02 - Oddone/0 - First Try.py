# %% ----- IMPORT MODULES -----

from main_code.cylinder_model.cylinder import Cylinder, CylinderGeometry, CylinderCoefficients, EnvironmentalConditions
from main_code.body_class import Body
from matplotlib import pyplot as plt
import numpy as np


# && ----- PLOTS -----

def simulate_temperature_evolution(cylinder, delta_t, max_steps=10):
    times = []
    temperatures = []
    q_cond_list = []

    current_time = 0
    while current_time < max_steps:
        times.append(current_time + delta_t)  # Tempo in secondi
        temperatures.append(cylinder.T_int)
        q_cond_list.append(cylinder.Q_cond())

        cylinder.energy_balance(delta_t)

        current_time += delta_t

    return times, temperatures, q_cond_list


# %% ----- OBJECT'S CREATION
tommaso = Body(height=1.80, weight=76, gender=1, age=25, T_skin=273.15 + 25, T_cl=273.15 + 22)
tommaso_env_conditions = EnvironmentalConditions(tommaso)
tommaso_env_conditions.set_conditions(temperature=273.15 + 25, pressure=101325, humidity=0.60)
tommaso_env_conditions.calculate_properties()
coefficient_cylinder = CylinderCoefficients(tommaso, tommaso_env_conditions)
geometry_cylinder = CylinderGeometry(d=0.2, h=0.8, s=0.2)
trunk = Cylinder(geometry_cylinder, tommaso, coefficient_cylinder, tommaso_env_conditions, T_int=36.0 + 273.15,
                 internal_heat_source=100)

delta_t = 1  # Intervallo di tempo in secondi
times, temperatures, q_cond_list = simulate_temperature_evolution(trunk, delta_t, max_steps=60 * 60 * 24)

plt.plot(times, np.array(temperatures) - 273.15, linestyle='-')
plt.xticks(np.arange(0, len(times) + 1, step=60 * 60 * 2), labels=np.arange(0, 25, 2))
plt.xlabel('Time (hr)')
plt.ylabel('Internal Temperature ($\degree$C)')
plt.title('Change in internal temperature over time')
plt.grid(True)
plt.show()

plt.plot(times, np.array(q_cond_list), linestyle='-')
plt.xticks(np.arange(0, len(times) + 1, step=60 * 60 * 2), labels=np.arange(0, 25, 2))
plt.xlabel('Time (hr)')
plt.ylabel('Conduction heat (W/m$^2$)')
plt.title('Change in conduction heat over time')
plt.grid(True)
plt.show()

# %% ---- TEST CODE -----

print(f'Heat exchanged by conduction: {trunk.Q_cond()=:.4f} [W]')
print(f'Heat exchanged by convection: {trunk.Q_conv()=:.4f} [W]')
print(f'Heat exchanged by radiation: {trunk.Q_irr()=:.4f} [W]')
print(f'Heat lost through evaporation: {trunk.E_sk()=:.4f} [W]')
print(f'Heat exchanged through the blood: {trunk.Q_blood()=:.4f} [W]')
print(f'Work done to pump blood:{trunk.W_pump_blood()=:.4f} [W]')
print(f'Internal Temperature at the last instant: {trunk.energy_balance(delta_t=60 * 60) - 273.15=:.4f} [$\degree$C]')
