import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import matplotlib.animation as animation

x1 = np.random.normal(-2.5, 1, 10000)
x2 = np.random.gamma(2, 1.5, 10000)
x3 = np.random.exponential(2, 10000) + 7
x4 = np.random.uniform(14, 20, 10000)

b1 = np.arange(-7, 2, 0.25)
b2 = np.arange(0, 16, 0.25)
b3 = np.arange(6, 28, 0.25)
b4 = np.arange(13, 21, 0.25)

a1 = [-7, 2, 0, 0.6]
a2 = [0, 16, 0, 0.6]
a3 = [6, 28, 0, 0.6]
a4 = [13, 21, 0, 0.6]

font = {'family': 'serif',
        'color': 'darkred',
        'weight': 'normal',
        'size': 8,
        }
Writer = animation.writers['imagemagick']
writer = Writer(fps=15, metadata=dict(artist='Me'),  bitrate=1800)
fig = plt.figure()
gspec = gridspec.GridSpec(2, 2)

normalPlot = plt.subplot(gspec[0, 0])

gamaPlot = plt.subplot(gspec[1, 0])

exponentialPlot = plt.subplot(gspec[0, 1])

uniformPlot = plt.subplot(gspec[1, 1])

# plt.subplots_adjust(bottom=0.2, right=0.8, top=0.9)

fig.tight_layout()

axes = [normalPlot, gamaPlot, exponentialPlot, uniformPlot]

n = 10000
factor = 500

def update(curr):
    # check if animation is at the last frame, and if so, stop the animation a
    curr = curr * factor
    if curr == n:
        a.event_source.stop()
    normalPlot.clear()
    normalPlot.axis(a1)
    normalPlot.hist(x1[: curr], bins=b1, normed=True)
    normalPlot.annotate('n = {}'.format(curr), [-1, 0.5])
    normalPlot.set_title('Sampling the Normal Distribution', fontdict=font)
    normalPlot.set_ylabel('Frequency', fontdict=font)

    gamaPlot.clear()
    gamaPlot.axis(a2)
    gamaPlot.hist(x2[: curr], bins=b2, normed=True)
    gamaPlot.annotate('n = {}'.format(curr), [10, 0.5])
    gamaPlot.set_title('Sampling the Gamma Distribution', fontdict=font)
    gamaPlot.set_ylabel('Frequency', fontdict=font)
    gamaPlot.set_xlabel('Value', fontdict=font)

    exponentialPlot.clear()
    exponentialPlot.axis(a3)
    exponentialPlot.set_title('Sampling the Exponential Distribution', fontdict=font)
    exponentialPlot.hist(x3[: curr], bins=b3, normed=True)
    exponentialPlot.annotate('n = {}'.format(curr), [20, 0.5])

    uniformPlot.clear()
    uniformPlot.axis(a4)
    uniformPlot.set_title('Sampling the Uniform Distribution', fontdict=font)
    uniformPlot.set_xlabel('Value', fontdict=font)
    uniformPlot.hist(x4[: curr], bins=b4, normed=True)
    uniformPlot.annotate('n = {}'.format(curr), [18, 0.5])

a = animation.FuncAnimation(fig, update, interval=100, frames=(int(n/factor)+1))
a.save('C:\\Users\\ksdee\\Documents\\practice_assignment3.gif', writer=writer)
plt.show()
