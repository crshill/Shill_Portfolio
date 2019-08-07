import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('./Rates/NC_Water_Rates_in_v_out_CSV.csv')#, header = 0, names = {'city', 'pop', 'roe', '0in', '0out',
                        #'3in', '3out', '4in', '4out', '5in', '5out', '10in', '10out', '15in', '15out', 'in vs out'})

AA = {'pop': df['pop'], 'roe': df['roe'], 'in v out': df['in vs out']}

rates = pd.DataFrame(data = AA)

print(df.tail(10))

###########################################################################
def plot_something(df, X, Y, xmax, path) :

    ax = df.plot.scatter(x = X, y = Y)
    ax.set_xlim(0, xmax)
    plt.show()
    plt.savefig(path)

plot_something(rates, 'pop', 'roe', 75000, './Plots/pop_vs_roe.png')
#plot_something(rates, 'in v out', 'roe', 3, './Plots/inout_vs_roe.png')

same = df.loc[df['0out']==0]
diff = df.loc[df['0out']>0]

plot_something(same, 'pop', 'roe', 50000, './Plots/pop_v_roe_same.png')
plot_something(diff, 'pop', 'roe', 50000, './Plots/pop_v_roe_diff.png')

