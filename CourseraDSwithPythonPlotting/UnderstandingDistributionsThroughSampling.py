import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import matplotlib.animation as animation
from matplotlib.widgets import Slider, Button, RadioButtons

if __name__ == '__main__':
    x1 = np.random.normal(-2.5, 1, 10000)
    x2 = np.random.gamma(2, 1.5, 10000)
    x3 = np.random.exponential(2, 10000) + 7
    x4 = np.random.uniform(14, 20, 10000)

    names = ['Nomral', 'Gamma', 'Exponential', 'Uniform']

    x = [x1, x2, x3, x4]

    b1 = np.arange(-7,2,0.25)
    b2 = np.arange(0, 16, 0.25)
    b3 = np.arange(6, 28, 0.25)
    b4 = np.arange(13, 21, 0.25)
    bins = [b1, b2, b3, b4]

    a1 = [-7, 2, 0, 0.6]
    a2 = [0, 16, 0, 0.6]
    a3 = [6, 28, 0, 0.6]
    a4 = [13, 21, 0, 0.6]

    annoation = [(1, 0.5),(14, 0.5),(25, 0.5),(19, 0.5)]

    aa = [a1, a2, a3, a4]

    fig = plt.figure()
    gspec = gridspec.GridSpec(2, 2)

    normalPlot = plt.subplot(gspec[0, 0])
    gamaPlot = plt.subplot(gspec[1, 0])
    exponentialPlot = plt.subplot(gspec[0, 1])
    uniformPlot = plt.subplot(gspec[1, 1])

    axes = [normalPlot, gamaPlot, exponentialPlot, uniformPlot]

    n = 10000
    multiplier = 100

    def update(curr):
        # check if animation is at the last frame, and if so, stop the animation a
        curr = curr * multiplier
        # print(curr)
        if curr == n:
            a.event_source.stop()

        print(' curr = {}'.format(curr))
        for i in range(0, len(axes)):
            axes[i].clear()
            axes[i].hist(x[i][:curr], bins=bins[i], normed=True)
            axes[i].axis(aa[i])
            axes[i].set_title('Sampling the {} Distribution'.format(names[i]))
            axes[i].set_ylabel('Frequency')
            axes[i].set_xlabel('Value')
            axes[i].annotate('n = {}'.format(curr), xy=annoation[i])


    def updateSlider(val):
        global multiplier
        print(str(sldr.val))
        multiplier = sldr.val
        fig.canvas.draw_idle()

    a = animation.FuncAnimation(fig, update, interval=10)

    slidAxes = plt.axes([0.4, 0.02, 0.2, 0.01], facecolor='red')
    sldr = Slider(slidAxes, 'Number of samples per run', 100, 1000, valstep=50)
    sldr.on_changed(updateSlider)

    plt.show()
    # print('hi')



