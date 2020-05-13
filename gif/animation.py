import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import HTML

fig = plt.figure()
ax = fig.add_subplot(111)
N = 10
x = np.random.rand(N)
y = np.random.rand(N)
z = np.random.rand(N)
c, t, d = ax.plot(x, 'ro', y, 'g^', z, 'b.')

ax.set_ylim(0, 1)
plt.axis('off')

def update(data):
    ax.clear()
    # c.set_ydata(data[0])
    # t.set_ydata(data[1])
    # ax.text(0.3, 0.4, data[0], fontdict=None, withdash=False)
    # ax.text(0.3, 0.5, data[1], fontdict=None, withdash=False)
    # ax.text(0.3, 0.5, data, fontdict=None, withdash=False)
    ax.text(0.5, 0.5, data, transform=ax.transAxes, size=46, ha='right', weight=800)

    # return c, t


def generated():
    while True:
        yield np.random.rand(N)


def initNumble():
    for i in range(1001):
        save_path = "{:>04d}".format(i)
        # n = 'n' + str(i)
        yield save_path


# anim = animation.FuncAnimation(fig, update, generated, interval=150)
# anim = animation.FuncAnimation(fig, update, frames=(1968, 2018), interval=150)
# anim = animation.FuncAnimation(fig, update, frames=(1968, 0,2018))
anim = animation.FuncAnimation(fig, update, initNumble, interval=6)
# anim = animation.FuncAnimation(fig, update, np.linspace(0, 10, 10), interval=1500)
HTML(anim.to_jshtml())
anim.to_html5_video()
anim.save('1.mp4')
plt.show()
