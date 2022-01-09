import cv2
import numpy as np
from numpy import interp
from pulse_detector_app import Window


class BPMPlotterWrapper:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.plotter = BPMPlotter()
        self.window = Window.Window("Plot2")
        self.frame = np.ones((height, width, 3)) * 255

    def plot(self, bpm, raw_data, amplitudes, frequencies):
        self.plotter.font_scale = 1.0
        self.frame = np.ones((self.height, self.width, 3)) * 255
        self.plotter.plot(self.frame, bpm, raw_data, amplitudes, frequencies)
        self.window.draw(self.frame)


# Plot values in opencv program
class BPMPlotter:
    def __init__(self, color=(255, 0, 0), data_relative_height=0.4, freq_ampl_relative_height=0.4):
        self.color = color
        self.data_relative_height = data_relative_height
        self.freq_ampl_relative_height = freq_ampl_relative_height
        self.freq_ampl_legend_relative_height = 0.09
        self.legend_relative_height = 0.09
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 1.0

    def plot(self, frame_to_draw, bpm, raw_data, amplitudes, frequencies):
        min_val = min(raw_data)
        max_val = max(raw_data)

        height = len(frame_to_draw)
        width = len(frame_to_draw[0])

        raw_data_bottom = int(height * self.data_relative_height)
        raw_step_size = width / len(raw_data)

        freq_ampl_top = raw_data_bottom
        freq_ampl_bottom = raw_data_bottom + int(height * self.freq_ampl_relative_height)

        min_ampl = min(amplitudes)
        max_ampl = max(amplitudes)

        min_freq = frequencies[0]
        min_freq_str = "%0.00f bpm" % min_freq
        max_freq = frequencies[-1]
        max_freq_str = "%0.00f bpm" % max_freq
        freq_step_size = int(width / len(frequencies))

        freq_ampl_legend_top = freq_ampl_bottom
        freq_ampl_legend_bottom = freq_ampl_legend_top + int(height * self.freq_ampl_legend_relative_height)
        cv2.putText(frame_to_draw, min_freq_str, (5, freq_ampl_legend_bottom),
                    self.font,
                    self.font_scale, self.color, 1)

        text_size = cv2.getTextSize(max_freq_str, self.font, 1.0, 1)[0]
        cv2.putText(frame_to_draw, max_freq_str, (width - text_size[0] - 5, freq_ampl_legend_bottom),
                    self.font,
                    self.font_scale, self.color, 1)

        # bpm
        legend_top = freq_ampl_legend_bottom
        legend_bottom = legend_top + int(height * self.legend_relative_height)
        bpm_str = "Your pulse is: %d bpm" % bpm
        cv2.putText(frame_to_draw, bpm_str, (5, legend_bottom),
                    self.font,
                    self.font_scale, self.color, 1)

        for i in range(len(amplitudes) -1):
            first = int(interp(amplitudes[i], [min_ampl, max_ampl], [freq_ampl_top, freq_ampl_bottom]))
            second = int(interp(amplitudes[i + 1], [min_ampl, max_ampl], [freq_ampl_top, freq_ampl_bottom]))
            cv2.line(frame_to_draw, (i * freq_step_size, freq_ampl_top + int(freq_ampl_bottom - first)),
                     ((i + 1) * freq_step_size, freq_ampl_top + int(freq_ampl_bottom - second)), self.color, 1)

        for i in range(len(raw_data) - 1):
            first = int(interp(raw_data[i], [min_val, max_val], [0, raw_data_bottom]))
            second = int(interp(raw_data[i + 1], [min_val, max_val], [0, raw_data_bottom]))
            cv2.line(frame_to_draw, (int(i * raw_step_size), int(raw_data_bottom - first)),
                     (int((i + 1) * raw_step_size), int(raw_data_bottom - second)), self.color, 1)
        return

    '''
    def add_graph(self, graph_id, label, color):
        self.graphs.update([(graph_id, GraphData(self.plot_size, label, color))])

    def update(self, graph_id, val):
        self.graphs.get(graph_id).put(val)
    

    # Update new values in plot
    def plot_graphs(self, label="Plot"):
        self.plot = np.ones(self.plot.shape, self.plot.dtype) * 255
        self.__draw_plot(label)

    # Show plot using opencv imshow
    def __draw_plot(self, label):
        cv2.line(self.plot, (0, int(self.graph_bottom)), (self.width, int(self.graph_bottom)), (0, 0, 255), 1)

        textOffset = 0
        for gd in self.graphs.values():
            cv2.putText(self.plot, gd.label, (textOffset, self.height - self.bottom_text_offset),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0, gd.color, 1)
            textSize = cv2.getTextSize(gd.label, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 1)
            textOffset += textSize[0][0] + self.labelOffsets
            for i in range(len(gd.data) - 1):
                first = int(interp(gd.data[i], [gd.min_val, gd.max_val], [0, self.graph_bottom]))
                second = int(interp(gd.data[i + 1], [gd.min_val, gd.max_val], [0, self.graph_bottom]))
                cv2.line(self.plot, (i * self.step_size, int(self.graph_bottom - first)), ((i + 1) * self.step_size,
                                                                                          int(self.graph_bottom - second)),
                                     gd.color, 1)

        cv2.imshow(label, self.plot)
        cv2.waitKey(1)
    '''

'''
array = []
maxVal = random.randint(50, 150)
for v in range(0, maxVal, 10):
    # call ‘plot’ method for realtime plot
    array.append(v)

for v in range(maxVal, 0, -10):
    # call ‘plot’ method for realtime plot
    array.append(v)

freqs = [55, 65, 75, 85, 95, 105, 115, 125, 135, 145, 155, 165]
ampls = [6, 20, 30, 25, 15, 3, 14, 12, 15, 6, 2, 1]


frame = np.ones((480, 640, 3)) * 255
bpmPlotter = BPMPlotter()
bpmPlotter.plot(frame, array, ampls, freqs)
cv2.imshow("TestPlot", frame)
cv2.waitKey(10000)
'''