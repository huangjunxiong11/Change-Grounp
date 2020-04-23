import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
from IPython.display import HTML

fig, ax = plt.subplots(figsize=(15, 8))


def draw_barchart(year):
    ax.clear()
    ax.text(1, 0.4, year, transform=ax.transAxes, size=46, ha='right', weight=800)
    plt.box(False)

draw_barchart(2018)

animator = animation.FuncAnimation(fig, draw_barchart, frames=(1968, 2018))
HTML(animator.to_jshtml())
animator.to_html5_video()
animator.save('1.gif')
