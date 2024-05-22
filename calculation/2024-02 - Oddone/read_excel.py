import pandas as pd
from datetime import datetime
from matplotlib import pyplot as plt
import matplotlib as mpl

from main_code.body_class import Body
plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'serif'
plt.rcParams['figure.dpi'] = 300

vo2 = pd.read_excel(io='example_test_VO2max.xlsx', sheet_name='Dati')
vo21 = vo2.copy()
vo21.drop(index=[0, 1], inplace=True)
vo21['t'] = pd.to_datetime(vo21['t'], format='%H:%M:%S')
vo21['VO2'].astype('float64')
print(vo21['t'][:5])
print(vo21['VO2'][:5])

# vo21.plot(x='t', y='VO2', kind='line')
fig, ax = plt.subplots()
plt.plot_date(vo21['t'], vo21['VO2'] / 60, '-', label='VO2max')
plt.xlabel('Time (MM:SS)'), plt.ylabel('VO$_2$ (mL/s)')
plt.title('Volume of Oxygen inhaled', fontdict={'fontsize': 12}, fontweight='bold')
ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%M:%S'))
plt.axvspan(datetime(1900, 1, 1, 0, 6, 45),
            datetime(1900, 1, 1, 0, 20, 0),
            facecolor='yellow', alpha=0.5, hatch='/', edgecolor='red', linewidth=2)
# plt.axvspan(datetime(1900, 1, 1, 0, 7, 5),
#             datetime(1900, 1, 1, 0, 20, 19),
#             facecolor='green', alpha=0.5, hatch='/', edgecolor='red', linewidth=2)
plt.text(datetime(1900, 1, 1, 0, 3, 0),
         90, 'REST', ha='center', va='center')
plt.text(datetime(1900, 1, 1, 0, 13, 0),
         90, 'EXERCISE', ha='center', va='center')
plt.text(datetime(1900, 1, 1, 0, 21, 0),
         90, 'RECOVERY', ha='center', va='center')
plt.show()

fig, ax = plt.subplots()
plt.plot_date(vo21['t'], vo21['RQ'], '-', label='VO2max')
plt.xlabel('Time (MM:SS)'), plt.ylabel('RQ (-)')
plt.title('Respiratory Quotient', fontdict={'fontsize': 12}, fontweight='bold')
ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%M:%S'))
plt.axvspan(datetime(1900, 1, 1, 0, 6, 45),
            datetime(1900, 1, 1, 0, 20, 0),
            facecolor='yellow', alpha=0.5, hatch='/', edgecolor='red', linewidth=2)
# plt.axvspan(datetime(1900, 1, 1, 0, 7, 5),
#             datetime(1900, 1, 1, 0, 20, 19),
#             facecolor='green', alpha=0.5, hatch='/', edgecolor='red', linewidth=2)
plt.text(datetime(1900, 1, 1, 0, 3, 0),
         1.3, 'REST', ha='center', va='center')
plt.text(datetime(1900, 1, 1, 0, 13, 0),
         1.3, 'EXERCISE', ha='center', va='center')
plt.text(datetime(1900, 1, 1, 0, 21, 0),
         1.3, 'RECOVERY', ha='center', va='center')
plt.show()

M = 21 * (0.23 * vo21['RQ'] + 0.77) * vo21['VO2'] / (60 * Body(height=1.815, weight=58.5).DuBois_surface())
fig, ax = plt.subplots()
plt.plot_date(vo21['t'], M, '-', label='VO2max')
plt.xlabel('Time (MM:SS)'), plt.ylabel('M (W/m$^2$)')
plt.title('Metabolism during exercise', fontdict={'fontsize': 12}, fontweight='bold')
ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%M:%S'))
plt.axvspan(datetime(1900, 1, 1, 0, 6, 45),
            datetime(1900, 1, 1, 0, 20, 0),
            facecolor='yellow', alpha=0.5, hatch='/', edgecolor='red', linewidth=2)
# plt.axvspan(datetime(1900, 1, 1, 0, 7, 5),
#             datetime(1900, 1, 1, 0, 20, 19),
#             facecolor='green', alpha=0.5, hatch='/', edgecolor='red', linewidth=2)
plt.text(datetime(1900, 1, 1, 0, 3, 0),
         1050, 'REST', ha='center', va='center')
plt.text(datetime(1900, 1, 1, 0, 13, 0),
         1050, 'EXERCISE', ha='center', va='center')
plt.text(datetime(1900, 1, 1, 0, 21, 0),
         1050, 'RECOVERY', ha='center', va='center')
plt.show()