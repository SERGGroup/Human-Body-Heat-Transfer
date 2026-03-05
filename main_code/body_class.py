class Body:
    def __init__(
            self,
            height: float = 1.73,
            weight: float = 76,
            gender: int = 1,
            age: float = 25,
            T_skin: float = 273.15 + 36.85,
            T_cl: float = 273.15 + 33.85,
            T_int: float = 309,
            internal_heat_source: float = 100,
            work: float = 0):
        self.height = height  # [m]
        self.weight = weight  # [kg]
        self.gender = gender  # [male=1; female=0]
        self.age = age
        self.T_skin = T_skin
        self.T_cl = T_cl
        self.T_int = T_int
        self.internal_heat_source = internal_heat_source
        self.work = work

    def DuBois_surface(self):
        return 0.202 * (self.weight ** 0.425) * (self.height ** 0.725)  # [m^2]

    def BMI(self) -> float:
        return self.weight / (self.height ** 2)

    def BF(self) -> float:
        if self.gender:
            if 20 <= self.age <= 39:
                return (0.19 - 0.08) / (39 - 20) * (self.age - 20) + 0.08
            elif 40 <= self.age <= 59:
                return (0.21 - 0.11) / (59 - 40) * (self.age - 40) + 0.11
            elif 60 <= self.age <= 79:
                return (0.24 - 0.13) / (79 - 60) * (self.age - 60) + 0.13
        else:
            if 20 <= self.age <= 39:
                return (0.32 - 0.21) / (39 - 20) * (self.age - 20) + 0.21
            elif 40 <= self.age <= 59:
                return (0.33 - 0.23) / (59 - 40) * (self.age - 40) + 0.23
            elif 60 <= self.age <= 79:
                return (0.35 - 0.24) / (79 - 60) * (self.age - 60) + 0.24
        # return 1.39 * self.BMI() + 0.16 * self.body.age - 10.8 * self.body.gender - 9

    def M_shiv(self) -> float:
        if (37 - (self.T_int - 273.15)) > 0:
            T_int_ = (37 - (self.T_int - 273.15))
        else:
            T_int_ = 0
        if (33 - (self.T_skin - 273.15)) > 0:
            T_skin_ = (33 - (self.T_skin - 273.15))
        else:
            T_skin_ = 0
        return (155.5 * T_int_ + 47.0 * T_skin_ - 1.57 * (T_skin_ ** 2)) / (self.BF() ** 0.5)

    def M_gender(self) -> float:
        if self.gender:
            return 66.4730 + 13.7516 * self.weight + 5.0033 * self.height - 6.7550 * self.age
        else:
            return 655.0955 + 9.5634 * self.weight + 1.8496 * self.height - 4.6756 * self.age


if __name__ == '__main__':
    import numpy as np
    import pandas as pd
    import seaborn as sns
    from matplotlib import pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    plt.rcParams['text.usetex'] = True
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['figure.dpi'] = 300

    met = [Body(height=height, weight=weight, gender=1, age=age, T_skin=273.15 + 33, T_cl=273.15 + 28,
                T_int=273.15 + 37, internal_heat_source=100, work=0).M_gender() for age in range(20, 71, 10)
           for weight in range(30, 125, 10) for height in range(150, 201, 10)]

    met.extend([Body(height=height, weight=weight, gender=0, age=age, T_skin=273.15 + 33, T_cl=273.15 + 28,
                     T_int=273.15 + 37, internal_heat_source=100, work=0).M_gender() for age in range(20, 71, 10)
                for weight in range(30, 125, 10) for height in range(150, 201, 10)])

    miii = pd.MultiIndex.from_product(iterables=[['Male', 'Female'],
                                                 [*range(150, 201, 10)],
                                                 [*range(30, 125, 10)],
                                                 [*range(20, 71, 10)]],
                                      names=['Gender', 'Height', 'Weight', 'Age'])
    # print(miii)

    met_df = pd.DataFrame(met, index=miii, columns=['Metabolism'])
    # print(met_df)
    # print(met_df['Metabolism'])
    # print(np.array(met))
    # met_df.plot(x='Height', y='Metabolism', )
    # plt.plot(met_df['Age'], met_df['Metabolism'])
    # plt.show()
    # print(met_df.index[1])
    # sns.barplot(data=met_df, x='Age', y='Metabolism', hue='Gender', alpha=0.7)
    # sns.relplot(data=met_df, x='Age', y='Metabolism', hue='Gender', style='Height', size='Weight', alpha=0.7)
    sns.catplot(data=met_df, x='Age', y='Metabolism', hue='Gender', row='Height', col='Weight')
    plt.ylabel('Basal metabolism (kcal/day)'), plt.xlabel('Age (years)')
    plt.title('Basal metabolism', y=1.0, fontdict={'fontsize': 12}, fontweight='bold')
    plt.show()

    # sns.jointplot(data=met_df, x='Age', y='Metabolism', hue='Gender')
    # plt.ylabel('Metabolism (kcal/day)')
    # plt.show()

    # df = met_df.unstack(level=0).reset_index()
    # df.columns = ['Gender', 'Height', 'Weight', 'Age', 'Metabolism']
    # print(df.Metabolism.Male)
    # X, Y = np.meshgrid(range(150, 201, 10), range(30, 125, 10))
    # df1 = pd.DataFrame({'x': df.Height, 'y': df.Weight, 'z': df.Metabolism.Male})
    # print(df1)
    # fig = plt.figure()
    # ax = Axes3D(fig)
    # ax.plot_trisurf(df1.x, df1.y, df1.z, cmap='jet', linewidth=0.2)
    # ax.plot_surface(X, Y, Body(height=X, weight=Y, gender=1).M_gender(), rstride=1, cstride=1, cmap='jet',
    #                 linewidth=0, antialiased=False)
    # plt.show()
    # print(Body(height=X, weight=Y, gender=1).M_gender())
    # print(len(df.Height), len(df.Weight), len(df.Metabolism.Male))