import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

BFN, c_dil, S_tr = 6.3, 50, 0.5

# q_blood = [
#     [(BFN + c_dil * (t_cr - 37)) / (1 + S_tr * (34 - t_sk)) for t_cr in range(18, 43) if t_cr >= 37]
#     for t_sk in range(28, 42) if t_sk <= 34]

q_blood = []
for t_cr in range(18, 43):
    q_bl = []
    for t_sk in range(28, 42):
        delta_Tcr, delta_Tsk = t_cr - 37, 34 - t_sk
        if delta_Tcr < 0:
            delta_Tcr = 0
        if delta_Tsk < 0:
            delta_Tsk = 0
        q_bl.append((BFN + c_dil * delta_Tcr) / (1 + S_tr * delta_Tsk))
    q_blood.append(q_bl)
df = pd.DataFrame(q_blood, columns=range(28, 42), index=range(18, 43))
print(df)

# ax = plt.figure().add_subplot(projection='3d')

# X, Y = np.meshgrid(range(18, 43), range(28, 42), indexing='ij')
# Z = np.array(q_blood)
#
# ax.plot_surface(X, Y, Z, edgecolor='royalblue', lw=0.5, rstride=2, cstride=2,
#                 alpha=0.3)
# ax.contourf(X, Y, Z, zdir='z', offset=-10, cmap='jet')
# ax.contourf(X, Y, Z, zdir='x', offset=15, cmap='jet')
# ax.contourf(X, Y, Z, zdir='y', offset=45, cmap='jet')
#
# ax.set(xlim=(15, 45), ylim=(25, 45), zlim=(-10, 275),
#        xlabel='Skin temperature [$\degree$C]',
#        ylabel='Core temperature [$\degree$C]',
#        zlabel='Skin blood flow rate [L/(h*m$^2$)]')
df.plot(kind='line')
plt.xlabel('Skin temperature [$\degree$C]')
plt.ylabel('Skin blood flow rate [L/(h*m$^2$)]')
plt.show()
