import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt

#import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

import collections


class DataGiver:
    def cpu(self):
        return 40

    def ram(self):
        return 40

class data_plot():
    def __init__(self):
        # start collections with zeros
        self.cpu = collections.deque(np.zeros(10))
        self.dg = DataGiver()

    def animate_func(self, i):
        # get data
        self.cpu.popleft()
        self.cpu.append(self.dg.cpu())

        # clear axis

        self.ax.cla()
        self.ax.plot(self.cpu)
        self.ax.scatter(len(self.cpu) - 1, self.cpu[-1])
        self.ax.text(len(self.cpu) - 1, self.cpu[-1] + 2, "{}%".format(self.cpu[-1]))
        self.ax.set_ylim(0, 100)

    def start(self):
        # define and adjust figure
        self.fig = plt.figure(figsize=(12, 6), facecolor='#DEDEDE')
        self.ax = plt.subplot()
        self.ax.set_facecolor('#DEDEDE')

        # animate
        self.ani = FuncAnimation(self.fig, self.animate_func, interval=1000)
        print("beforeplot")
        plt.show(block = False)
        print("afterplot")