import collections
import cv2
import numpy as np
import random


class GraphData:
    def __init__(self, x_size, label, color):
        self.x_size = x_size
        self.data = collections.deque(np.zeros(2, dtype=int))
        self.label = label
        self.color = color

    def put(self, val):
        self.data.append(int(val))
        while len(self.data) > self.x_size:
            self.data.popleft()


# Plot values in opencv program
class Plotter:

    def __init__(self, plot_width, plot_height, plot_step_size):
        self.step_size = plot_step_size
        self.plot_size = int(plot_width / plot_step_size)
        self.width = plot_width
        self.height = plot_height
        self.color = (255, 0 ,0)
        self.plot = np.ones((self.height, self.width, 3))*255
        self.offset = 50 # for legend, etc...
        self.graph_bottom = plot_height - 50
        self.graphs = {}
        self.labelOffsets = 30

        self.bottom_text_offset = 5

    def add_graph(self, graph_id, label, color):
        self.graphs.update([(graph_id, GraphData(self.plot_size, label, color))])

    def update(self, graph_id, val):
        self.graphs.get(graph_id).put(val)

    # Update new values in plot
    def plot_graphs(self, label = "plot"):
        self.plot = np.ones(self.plot.shape, self.plot.dtype)*255
        self.__draw_plot(label)

    # Show plot using opencv imshow
    def __draw_plot(self, label):
        cv2.line(self.plot, (0, int(self.graph_bottom) ), (self.width, int(self.graph_bottom)), (0, 0, 255), 1)

        textOffset = 0
        for gd in self.graphs.values():
            cv2.putText(self.plot, gd.label, (textOffset, self.height - self.bottom_text_offset), cv2.FONT_HERSHEY_SIMPLEX,
                        1.0, gd.color, 1)
            textSize = cv2.getTextSize(gd.label, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 1)
            textOffset += textSize[0][0] + self.labelOffsets
            for i in range(len(gd.data)-1):
                cv2.line(self.plot, (i * self.step_size, int(self.graph_bottom - gd.data[i])), ((i+1) * self.step_size,
                        int(self.graph_bottom - gd.data[i+1])), gd.color, 1)

        cv2.imshow(label, self.plot)
        cv2.waitKey(30)


plotter = Plotter(1200, 300, 10)
plotter.add_graph(0, "Test graph1", (0, 255, 0))
plotter.add_graph(1, "Test graph2", (125, 125, 0))
# Create dummy values using for loop
while True:
    maxVal = random.randint(50,150)
    for v in range(0,maxVal,10):
    # call ‘plot’ method for realtime plot
        plotter.update(0, v)
        plotter.update(1, 50)
        plotter.plot_graphs()

    for v in range(maxVal, 0 , -10):
    # call ‘plot’ method for realtime plot
        plotter.update(0, v)
        plotter.update(1, 20)
        plotter.plot_graphs()