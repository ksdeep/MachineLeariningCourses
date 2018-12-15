import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


if __name__=='__main__':
    np.random.seed(12345)

    df = pd.DataFrame([np.random.normal(32000, 200000, 3650),
                       np.random.normal(43000, 100000, 3650),
                       np.random.normal(43500, 140000, 3650),
                       np.random.normal(48000, 70000, 3650)],
                      index=[1992, 1993, 1994, 1995])

    df = df.T
    barWidth = 0.3
    y = 42000

    bars = np.array([np.mean(df[1992]), np.mean(df[1993]), np.mean(df[1994]), np.mean(df[1995])])
    yer = [1.96 * np.std(df[1992]) / np.sqrt(3650), 1.96 * np.std(df[1993]) / np.sqrt(3650),
           1.96 * np.std(df[1994]) / np.sqrt(3650), 1.96 * np.std(df[1995]) / np.sqrt(3650)]
    barsMax = np.array([a_i + b_i for a_i, b_i in zip(bars, yer)])
    barsMin = np.array([a_i - b_i for a_i, b_i in zip(bars, yer)])

    clrMp = pd.Series([(y - mn) / (max - mn) for mn, max in zip(barsMin, barsMax)])
    clrMp = clrMp.apply(lambda x: 1 if x < 0 else 0 if x > 1 else x)

    r1 = np.arange(len(bars))


    fig = plt.figure()

    plt.clf()

    plot = plt.scatter(clrMp, clrMp, c=clrMp, cmap='RdBu_r')
    plt.clf()
    plt.colorbar(plot)
    my_cmap = plt.cm.get_cmap('RdBu_r')
    colors = my_cmap(clrMp)

    plt.bar(r1, bars, width=barWidth, color=colors, edgecolor='black', yerr=yer, capsize=7, label='poacee')
    plt.axhline(y, color="b", linestyle='-')
    plt.xticks([r for r in range(len(bars))], df.columns)
    plt.yticks(list(plt.yticks()[0]) + [y])


    def calcuateAndPlot(event):
        global y, clrMp, max, mn, barsMax, barsMin , r1, my_cmap, colors
        y = event.ydata
        clrMp = pd.Series([(y - mn) / (max - mn) for mn, max in zip(barsMin, barsMax)])
        clrMp = clrMp.apply(lambda x: 1 if x < 0 else 0 if x > 1 else x)

        plot = plt.scatter(clrMp, clrMp, c=clrMp, cmap='RdBu_r')
        plt.clf()
        plt.colorbar(plot)
        my_cmap = plt.cm.get_cmap('RdBu_r')
        colors = my_cmap(clrMp)

        plt.bar(r1, bars, width=barWidth, color=colors, edgecolor='black', yerr=yer, capsize=7, label='poacee')
        plt.axhline(y, color="b", linestyle='-')
        plt.xticks([r for r in range(len(bars))], df.columns)
        plt.yticks(list(plt.yticks()[0]) + [y])
        plt.show()
        return None

    fig.canvas.mpl_connect('button_press_event', calcuateAndPlot)
    plt.show()