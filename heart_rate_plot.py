import collections
import cv2
import numpy as np
import random

# Plot values in opencv program
class Plotter:
    def __init__(self, plot_width, plot_height, plot_step_size):
        self.step_size = plot_step_size
        self.plotSize = int(plot_width / plot_step_size)
        self.width = plot_width
        self.height = plot_height
        self.color = (255, 0 ,0)
        self.val = collections.deque(np.zeros(5, dtype=int))
        self.plot = np.ones((self.height, self.width, 3))*255
        self.offset = 50 # for legend, etc...

    # Update new values in plot
    def plot_graph(self, val, label = "plot"):
        self.val.append(int(val))
        while len(self.val) > self.plotSize:
            self.val.popleft()
            self.plot = np.ones(self.plot.shape, self.plot.dtype)*255

        self.show_plot(label)

    # Show plot using opencv imshow
    def show_plot(self, label):
        cv2.line(self.plot, (0, int(self.height/2) ), (self.width, int(self.height/2)), (0,255,0), 1)
        for i in range(len(self.val)-1):
            cv2.line(self.plot, (i * self.step_size, int(self.height/2 - self.val[i])), ((i+1) * self.step_size , int(self.height/2 - self.val[i+1])), self.color, 1)

        cv2.imshow(label, self.plot)
        cv2.waitKey(30)


plotter = Plotter(1200, 300, 10)
# Create dummy values using for loop
while True:
    maxVal = random.randint(50,150)
    for v in range(0,maxVal,10):
    # call ‘plot’ method for realtime plot
        plotter.plot_graph(v)

    for v in range(maxVal, 0 , -10):
    # call ‘plot’ method for realtime plot
        plotter.plot_graph(v)