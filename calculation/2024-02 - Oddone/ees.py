import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'serif'
# plt.rcParams['font.serif'] = 'Computer Modern Roman'
plt.rcParams['figure.dpi'] = 300
print(plt.rcParams.keys())


# df = pd.read_table('Table 2.txt', header=None)
# df.columns = ['Temperature', 'skin wettedness', 'Convection', 'Radiation', 'Evaporation', 'Respiration', 'Metabolism',
#               'Blood', 'Net energy', 'Exergy convection', 'Exergy radiation', 'Exergy evaporation', 'Exergy respiration',
#               'Exergy blood', 'Exergy destruction', 'Efficiency exergy indestructible', 'Efficiency exergy destruction']
#
# df.plot(x='Temperature', y=['Convection', 'Radiation', 'Evaporation', 'Respiration', 'Blood'])
# plt.xticks(ticks=np.linspace(df['Temperature'][0], df['Temperature'].iloc[-1], 8), labels=list(range(5, 41, 5)), rotation=0)
# plt.xlabel('Temperature ($^{\circ}$C)')
# plt.ylabel('Rate of energy exchange (W)')
# plt.show()
# print(sum([0.667, 0.223, 0.027, 0.027, 0.084, 0.084]))

df = pd.read_table('Table_2.TXT', header=None)
# print(df.head())
Qc_net = df[5] + df[6] + 2 * (df[7] + df[8])
Qr_net = df[9] + df[10] + 2 * (df[11] + df[12])
Hres_net = df[13] + df[14]
He_net = df[15] + df[16] + 2 * (df[17] + df[18])
DeltaH_bl_net = df[23] + df[24] + 2 * (df[25] + df[26])
# dict = {'Temperature': df[0],
#         'Convection': Q, 'Radiation', 'Evaporation', 'Blood', 'Respiration'}
df1 = pd.DataFrame([df[0], Qc_net, Qr_net, He_net, DeltaH_bl_net, Hres_net]).transpose()
df1.columns = ['Temperature', 'Convection', 'Radiation', 'Evaporation', 'Blood', 'Respiration']
print(df1)
df1.plot(x='Temperature', y=['Convection', 'Radiation', 'Evaporation', 'Blood', 'Respiration'], kind='line')
plt.xticks(ticks=np.linspace(df[0][0], df[0].iloc[-1], 9),
           labels=[*range(0, 41, 5)], rotation=0)
plt.xlabel('Temperature ($^{\circ}$C)')
plt.ylabel('Rate of energy exchange (W)')
plt.title('Various energy exchange rates (EES model)', fontdict={'fontsize': 12}, fontweight='bold')
plt.show()
