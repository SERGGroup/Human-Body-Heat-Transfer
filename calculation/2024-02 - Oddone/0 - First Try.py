# %% IMPORT MODULES
from main_code import Body, Cylinder


# %% INIT CALCULATIONS
person = Body()
trunk = Cylinder(d=0.2, h=0.6, body=person, T_int=309, internal_heat_source=100)

# simulaiton of energy balance for 60 seconds:

# %% EVALUATE
delta_time = 60  # secondi
final_T_int = trunk.energy_balance(delta_time)
heat_lost_w = trunk.dissipated_energy_watt()
heat_lost_j = trunk.dissipated_energy_joule(delta_time)

print(f'Final T_int: {final_T_int} [K]')
print(f'Heat lost: {heat_lost_w} [W]')
print(f'Heat lost: {heat_lost_j} [j]')