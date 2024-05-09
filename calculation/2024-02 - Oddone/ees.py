import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'serif'
plt.rcParams['figure.dpi'] = 300


df = pd.read_table('Table 2.txt', header=None)
df.columns = ['Temperature', 'skin wettedness', 'Convection', 'Radiation', 'Evaporation', 'Respiration', 'Metabolism',
              'Blood', 'Net energy', 'Exergy convection', 'Exergy radiation', 'Exergy evaporation', 'Exergy respiration',
              'Exergy blood', 'Exergy destruction', 'Efficiency exergy indestructible', 'Efficiency exergy destruction']

df.plot(x='Temperature', y=['Convection', 'Radiation', 'Evaporation', 'Respiration', 'Blood'])
plt.xticks(ticks=np.linspace(df['Temperature'][0], df['Temperature'].iloc[-1], 8), labels=list(range(5, 41, 5)), rotation=0)
plt.xlabel('Temperature ($^{\circ}$C)')
plt.ylabel('Rate of energy exchange (W)')
plt.show()
