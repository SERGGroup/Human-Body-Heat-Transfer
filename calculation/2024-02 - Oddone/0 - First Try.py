# %% ----- IMPORT MODULES -----
from main_code.cylinder_model import cylinder
from main_code.cylinder_model.cylinder import Cylinder, CylinderGeometry, CylinderCoefficients, EnvironmentalConditions
from main_code.body_class import Body
from matplotlib import pyplot as plt
import numpy as np
import matplotlib as mpl

# mpl.use(backend='Qt5Py')
# plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'serif'
plt.rcParams['figure.dpi'] = 300


# && ----- PLOTS -----

def simulate_temperature_evolution(body: Body, cylinder: Cylinder, delta_t: float, max_steps: int = 10):
    times = []
    temperatures = []
    q_conds, q_convs, q_irrs, e_sks, q_bloods, q_ress = [], [], [], [], [], []

    current_time = 0
    while current_time < max_steps:
        times.append(current_time + delta_t)  # Time in seconds
        temperatures.append(body.T_int)
        q_conds.append(cylinder.Q_cond())
        q_convs.append(cylinder.Q_conv())
        q_irrs.append(cylinder.Q_irr())
        e_sks.append(cylinder.E_sk())
        q_bloods.append(cylinder.Q_blood())
        q_ress.append(cylinder.Q_res())

        cylinder.energy_balance(delta_t)

        current_time += delta_t

    return times, temperatures, q_conds, q_convs, q_irrs, e_sks, q_bloods, q_ress


# %% ----- OBJECT'S CREATION
subjects: list[Body] = [Body(height=1.80, weight=76, gender=1, age=25, T_skin=273.15 + 33, T_cl=273.15 + 24, T_int=273.15 + 37,
               internal_heat_source=100, work=w_) for w_ in range(0, 301, 100)]

total_energies: list[list] = []
for k in range(len(subjects)):
    env_conds: list[EnvironmentalConditions] = [EnvironmentalConditions(body=subjects[k], temperature=273.15 + temp,
                                                                        pressure=101325, humidity=0.5, v_air=0.3,
                                                                        fluid='water') for temp in range(5, 41, 1)]
    # subject_env_conditions = EnvironmentalConditions(body=subject, temperature=273.15 + 28, pressure=101325, humidity=0.4,
    #                                                  v_air=0.2, fluid='water')
    # tommaso_env_conditions.set_conditions(temperature=273.15 + 0.1, pressure=101325, humidity=1)

    [env_cond.calculate_properties() for env_cond in env_conds]
    # subject_env_conditions.calculate_properties()
    cyl_coeffs: list[CylinderCoefficients] = [CylinderCoefficients(body=subjects[k], environmental_conditions=env_cond) for
                                              env_cond in env_conds]
    # coefficient_cylinder = CylinderCoefficients(subject, subject_env_conditions)
    # geometry_cylinder = CylinderGeometry(d=0.5, h=1.80, s=0.2)
    geometry = {'head':    {'d': 0.146, 'h': 0.207},
                'neck':    {'d': 0.114, 'h': 0.083},
                'trunk':   {'d': 0.260, 'h': 0.798},
                'arm':     {'d': 0.090, 'h': 0.353},
                'forearm': {'d': 0.074, 'h': 0.292},
                'hand':    {'d': 0.046, 'h': 0.300},
                'thigh':   {'d': 0.134, 'h': 0.352},
                'leg':     {'d': 0.086, 'h': 0.379},
                'foot':    {'d': 0.072, 'h': 0.241}
                }

    Q_cond_nets, Q_conv_nets, Q_irr_nets, E_sk_nets, Q_blood_nets, Q_res_nets = [], [], [], [], [], []
    totals = []
    for env_cond, cyl_coeff in zip(env_conds, cyl_coeffs):
        parts = []
        for i, geo in enumerate(geometry.values()):
            part_geometry = CylinderGeometry(d=geo['d'], h=geo['h'], s=0.2)
            parts.append(Cylinder(geometry=part_geometry, body=subjects[k], coefficients=cyl_coeff,
                                  environmental_conditions=env_cond))

        Q_cond_net, Q_conv_net, Q_irr_net, E_sk_net, Q_blood_net, Q_res_net = 0, 0, 0, 0, 0, 0
        for geom, part in zip(geometry.keys(), parts):
            if geom in ['head', 'neck', 'trunk']:
                pair = 1
            else:
                pair = 2
            Q_cond_net += pair * part.Q_cond()
            Q_conv_net += pair * part.Q_conv()
            Q_irr_net += pair * part.Q_irr()
            E_sk_net += pair * part.E_sk()
            Q_blood_net += pair * part.Q_blood()
            # t_cls += part.calculate_Tcl()
            if geom == 'head':
                Q_res_net += pair * part.Q_res()

        Q_cond_nets.append(Q_cond_net), Q_conv_nets.append(Q_conv_net), Q_irr_nets.append(Q_irr_net)
        E_sk_nets.append(E_sk_net), Q_blood_nets.append(Q_blood_net), Q_res_nets.append(Q_res_net)

        af_ = env_cond.calculate_area_factor(vector_a=env_cond.get_vector_a(),
                                             vector_b=env_cond.get_vector_b(),
                                             vector_c=env_cond.get_vector_c())
        T_mr_ = env_cond.calculate_T_mr(area_factor=af_, T_surf=env_cond.get_vector_T_surf())
        print(f'Area factors: {af_}, T_mr: {T_mr_}')
        print(
            f"{Q_cond_net=:.4f}\n{Q_conv_net=:.4f}\n{Q_irr_net=:.4f}\n{E_sk_net=:.4f}\n{Q_blood_net=:.4f}\n{Q_res_net=:.4f}\n"
            f"{subjects[k].M_shiv()=:.4f}\n{env_cond.M_act()=:.4f}\n{subjects[k].work=:.4f}\n"
            f"{cyl_coeff.calculate_hr()=:.4f}\n"
            f"{env_cond.calculate_T_mr(area_factor=af_, T_surf=env_cond.get_vector_T_surf())=:.4f}\n"
            f"{cyl_coeff.calculate_fcl()=:.4f}\n{cyl_coeff.calculate_to()-273.15=:.4f}\n")

        print((subjects[k].T_cl - cyl_coeff.calculate_to()) / (subjects[k].T_skin - cyl_coeff.calculate_to()))

        total_energy_balance = (env_cond.M_act() + subjects[k].M_shiv() + subjects[k].internal_heat_source -
                                (subjects[k].work + Q_cond_net + Q_conv_net + Q_irr_net + E_sk_net + Q_blood_net + Q_res_net))
        if total_energy_balance < subjects[k].internal_heat_source:
            total_energy_balance = subjects[k].internal_heat_source
        totals.append(total_energy_balance)
        print(f'Total energy balance: {total_energy_balance:.4f}')

    if k == 0:
        for net, label in zip([Q_cond_nets, Q_conv_nets, Q_irr_nets, E_sk_nets, Q_blood_nets, Q_res_nets,
                               # [env_cond.M_act() for env_cond in env_conds]
                               ],
                              ['Conduction', 'Convection', 'Radiation', 'Evaporation', 'Blood', 'Respiration',
                               # 'Metabolism'
                               ]):
            # print(len(range(10, 46, 5)), len(net))
            plt.plot(np.arange(5, 41, 1), np.array(net), label=label)
            # plt.plot(np.linspace(0, 1, 11), np.array(net), label=label)
        plt.legend(), plt.xlabel('Temperature ($^{\circ}$C)'), plt.ylabel('Energy exchange (W)')
        plt.title('Various energy exchange rates with temperature', fontdict={'fontsize': 12}, fontweight='bold')
        plt.show()
    total_energies.append(totals)

for k, total_energy in enumerate(total_energies):
    plt.plot(np.arange(5, 41, 1), np.array(total_energy), label=f'Work: {k * 100} (W)')
# plt.plot(np.linspace(0, 1, 11), np.array(totals), label='Net energy')
plt.legend(), plt.xlabel('Temperature ($^{\circ}$C)'), plt.ylabel('Net energy (W)')
plt.title('Net energy during workout', fontdict={'fontsize': 12}, fontweight='bold')
plt.show()

# P_s_sk_ = np.array([env_cond.get_properties()['Water Vapor Pressure Skin'] for env_cond in env_conds])
# P_s_ = np.array([env_cond.get_properties()['Water Vapor Pressure'] for env_cond in env_conds])
# plt.plot(np.arange(10, 41, 2), P_s_sk_, label='P_sk_s')
# plt.plot(np.arange(10, 41, 2), P_s_, label='P_s')
# plt.legend(), plt.show()
# plt.plot(np.arange(10, 41, 2), (P_s_sk_ - P_s_), label='Skin')
# plt.legend(), plt.show()
#
# hr_ = np.array([cyl_coeff.calculate_hr() for cyl_coeff in cyl_coeffs])
# plt.plot(np.arange(10, 41, 2), hr_ , label='hr')
# plt.legend(), plt.show()
# for geom, part in zip(geometry.keys(), parts):
#     # times, temperatures, q_conds, q_convs = [], [], [], []
#     times, temperatures, q_conds, q_convs, q_irrs, e_sks, q_bloods, q_ress = simulate_temperature_evolution(
#         body=subject, cylinder=part, delta_t=60 * 60, max_steps=60 * 60 * 24)
#     plt.plot(np.array(times), np.array(temperatures) - 273.15, label=f'{geom.capitalize()}')
# plt.xticks(np.arange(0, times[-1] + 1, step=60 * 60 * 2), labels=np.arange(0, 25, 2))
# print(times[-1], temperatures[-1], q_conds[-1], q_convs[-1], q_irrs[-1], e_sks[-1], q_bloods[-1], q_ress[-1])
# plt.title(f'Temperature evolution for subject')
# plt.xlabel('Time (hr)'), plt.ylabel('Temperature ($^{\circ}$C)')
# plt.legend()
# plt.show()

# for geom, part in zip(geometry.keys(), parts):
#     times, temperatures, q_conds, q_convs = [], [], [], []
#     times, temperatures, q_conds, q_convs = simulate_temperature_evolution(body=subject, cylinder=part, delta_t=60 * 60, max_steps=60 * 60 * 24)
#     plt.plot(np.array(times), np.array(temperatures) - 273.15, label=f'{geom.capitalize()}')
# plt.xticks(np.arange(0, times[-1] + 1, step=60 * 60 * 2), labels=np.arange(0, 25, 2))
# print(times[-1], temperatures[-1], q_conds[-1], q_convs[-1])
# plt.title(f'Temperature evolution for subject')
# plt.xlabel('Time (hr)'), plt.ylabel('Temperature ($^{\circ}$C)')
# plt.legend()
# plt.show()

# trunks = []
# for work in range(0, 301, 100):
#     trunks.append(Cylinder(geometry_cylinder, tommaso, coefficient_cylinder, tommaso_env_conditions,
#                            T_int=37.0 + 273.15, internal_heat_source=100, work=work))
#
# delta_t = 1  # Time interval in seconds
# times_list, temp_list, cond_list, conv_list = [], [], [], []
# for trunk in trunks:
#     temp_var = simulate_temperature_evolution(trunk, delta_t, max_steps=60 * 60 * 24)
#     times_list.append(temp_var[0]), temp_list.append(temp_var[1])
#     cond_list.append(temp_var[2]), conv_list.append(temp_var[3])
#
# exercises = ['Resting', 'Walking', 'Running', 'Heavy lifting']
# markers, markers_on = ['o', 'v', 'd', '*'], range(0, 60*60*24, 60*60*2-1)
#
# def plot_agaist_time(xs, ys, title, ylabel):
#     for x, y, w, marker in zip(xs, ys, exercises, markers):
#         plt.plot(np.array(x), np.array(y), marker=marker, linestyle='-', markevery=markers_on, label=f'{w}')
#     plt.xticks(np.arange(0, len(times_list[0]) + 1, step=60 * 60 * 2), labels=np.arange(0, 25, 2))
#     plt.xlabel('Time (hours)')
#     plt.ylabel(ylabel)
#     plt.title(title)
#     plt.grid(True)
#     plt.legend()
#     plt.show()
#
#
# def plot_against_temperature(xs, ys, title, ylabel):
#     for x, y, w, marker in zip(xs, ys, exercises, markers):
#         plt.plot(np.array(x), np.array(y), marker=marker, linestyle='-', fillstyle='none', markevery=markers_on, label=f'{w}')
#     # plt.xticks(np.arange(0, len(times) + 1, step=60 * 60 * 2), labels=np.arange(0, 25, 2))
#     plt.xlabel('Temperature ($^{\circ}$C)')
#     plt.ylabel(ylabel)
#     plt.title(title)
#     plt.grid(True)
#     plt.legend()
#     plt.show()
#
#
# # for time, temp, w in zip(times_list, temp_list, exercises):
# #     plt.plot(np.array(time), np.array(temp) - 273.15, label=f'{w}')
# # plt.xlabel('Time (hour)')
# # plt.ylabel('Internal Temperature ($\degree$C)')
# # plt.title('Change in internal temperature over time for various physical activities')
# # plt.grid(True)
# # plt.legend()
# # plt.xticks(np.arange(0, len(times_list[0]) + 1, step=60 * 60 * 2), labels=np.arange(0, 25, 2))
# # plt.show()
#
# # for time, temp, cond, conv in temp_list:
# plot_agaist_time(xs=times_list, ys=np.array(temp_list) - 273.15, title='Change in internal temperature over time',
#                  ylabel='Internal Temperature ($^{\circ}$C)')
# plot_agaist_time(xs=times_list, ys=cond_list, title='Change in heat conduction over time',
#                  ylabel='Conduction heat (W/m$^2$)')
# plot_agaist_time(xs=times_list, ys=np.array(conv_list), title='Change in heat convection  over time',
#                  ylabel='Convection heat (W/m$^2$)')
#
# plot_against_temperature(xs=np.array(temp_list) - 273.15, ys=np.array(cond_list),
#                          title='Change in conduction heat over temperature', ylabel='Conduction heat (W/m$^2$)')
# plot_against_temperature(xs=np.array(temp_list) - 273.15, ys=np.array(conv_list),
#                          title='Change in convection heat over temperature', ylabel='Convecction heat (W/m$^2$)')
#
# # %% ---- TEST CODE -----
#
# print(f'Heat exchanged by conduction: {trunk.Q_cond()=:.4f} [W]')
# print(f'Heat exchanged by convection: {trunk.Q_conv()=:.4f} [W]')
# print(f'Heat exchanged by radiation: {trunk.Q_irr()=:.4f} [W]')
# print(f'Heat lost through evaporation: {trunk.E_sk()=:.4f} [W]')
# print(f'Heat exchanged through the blood: {trunk.Q_blood()=:.4f} [W]')
# print(f'Heat exchanged through the blood: {trunk.Q_res()=:.4f} [W]')
# print(f'Heat exchanged by shivering: {trunk.M_shiv()=:.4f} [W]')
# print(f'Work done to pump blood:{trunk.W_pump_blood()=:.4f} [W]')
# print(f'Internal Temperature at the last instant: {trunk.energy_balance(delta_t=60 * 60) - 273.15=:.4f} [deg C]')
# # af_ = tommaso_env_conditions.calculate_area_factor(vector_a=tommaso_env_conditions.get_vector_a(),
# #                                                    vector_b=tommaso_env_conditions.get_vector_b(),
# #                                                    vector_c=tommaso_env_conditions.get_vector_c())
# # print(f'Area factors: {af_}')
# # print(f'Mean radiant temperature: {tommaso_env_conditions.calculate_T_mr(area_factor=af_, T_surf=tommaso_env_conditions.get_vector_T_surf())=:.4f} [deg C]')
# # print(f'hr: {coefficient_cylinder.calculate_hr()}')
# # print(f'Properties: {tommaso_env_conditions.get_properties()}')
