import cv2
import numpy as np
from numpy import interp
from pulse_detector_app import Window


# wrapper around the plotter that wraps the plotter and adds the plotting into Window
class BPMPlotterWrapper:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.plotter = BPMPlotter()
        self.window = Window.Window("Pulse plot")
        self.frame = np.ones((height, width, 3)) * (20 / 255)

    def plot(self, bpm, raw_data, amplitudes, frequencies):
        self.plotter.font_scale = 1.0
        self.frame = np.ones((self.height, self.width, 3)) * (20 / 255)
        self.plotter.plot(self.frame, bpm, raw_data, amplitudes, frequencies)
        self.window.draw(self.frame)


# Plot values in opencv program
class BPMPlotter:
    def __init__(self, color=(240, 240, 240)):
        self.color = color
        self.raw_data_relative_height = 0.3
        self.raw_data_legend__relative_height = 0.1
        self.freq_ampl_relative_height = 0.3
        self.freq_ampl_legend_relative_height = 0.18
        self.legend_relative_height = 0.09
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 1.0

    # plotting the data into a given frame (frame_to_draw)
    # bpm - number, estimated pulse
    # raw_data - scanned averages from the face
    # amplitudes, frequencies - data for the interesting part to plot (something around 55-170)
    # amplitudes are given for their frequencies
    def plot(self, frame_to_draw, bpm, raw_data, amplitudes, frequencies):
        min_val = min(raw_data)
        max_val = max(raw_data)

        height = len(frame_to_draw)
        width = len(frame_to_draw[0])

        # draw raw data
        raw_data_bottom = int(height * self.raw_data_relative_height)
        raw_step_size = width / len(raw_data)

        for i in range(len(raw_data) - 1):
            first = int(interp(raw_data[i], [min_val, max_val], [0, raw_data_bottom]))
            second = int(interp(raw_data[i + 1], [min_val, max_val], [0, raw_data_bottom]))
            cv2.line(frame_to_draw, (int(i * raw_step_size), int(raw_data_bottom - first)),
                     (int((i + 1) * raw_step_size), int(raw_data_bottom - second)), self.color, 1)

        # draw raw data legend
        raw_data_legend_top = raw_data_bottom
        raw_data_legend_bottom = raw_data_bottom + int(height * self.raw_data_legend__relative_height)
        cv2.putText(frame_to_draw, "Record of measured data from your face.",
                    (5, raw_data_legend_bottom - 5),
                    self.font,
                    self.font_scale * 0.6, self.color, 1)
        cv2.line(frame_to_draw, (0, raw_data_legend_bottom), (width, raw_data_legend_bottom), self.color, 1)

        # draw amplitudes for the interesting frequencies
        freq_ampl_top = raw_data_legend_bottom
        freq_ampl_bottom = freq_ampl_top + int(height * self.freq_ampl_relative_height)

        min_ampl = min(amplitudes)
        max_ampl = max(amplitudes)
        freq_step_size = int(width / len(frequencies))
        for i in range(len(amplitudes) -1):
            first = int(interp(amplitudes[i], [min_ampl, max_ampl], [freq_ampl_top, freq_ampl_bottom]))
            second = int(interp(amplitudes[i + 1], [min_ampl, max_ampl], [freq_ampl_top, freq_ampl_bottom]))
            cv2.line(frame_to_draw, (i * freq_step_size, freq_ampl_top + int(freq_ampl_bottom - first)),
                     ((i + 1) * freq_step_size, freq_ampl_top + int(freq_ampl_bottom - second)), self.color, 1)

        # draw the axis
        freq_ampl_legend_top = freq_ampl_bottom
        freq_ampl_legend_bottom = freq_ampl_legend_top + int(height * self.freq_ampl_legend_relative_height / 2)

        min_freq = frequencies[0]
        max_freq = frequencies[-1]
        freq_legend_step_size = (max_freq - min_freq) / 6
        freq_i = min_freq
        freq_legend_step_size_pixels = width / 7
        width_i = 0
        for i in range(7):
            text_str = "%d" % round(freq_i)
            cv2.putText(frame_to_draw, text_str, (int(width_i), freq_ampl_legend_bottom),
                        self.font,
                        self.font_scale * 0.6, self.color, 1)
            freq_i += freq_legend_step_size
            width_i += freq_legend_step_size_pixels

        # draw legend of amplitude of given frequencies graph
        freq_ampl_legend_bottom2 = freq_ampl_legend_bottom + int(height * self.freq_ampl_legend_relative_height / 2)
        cv2.putText(frame_to_draw, "The estimated \"probability\" of the bpm to be the correct one",
                    (5, freq_ampl_legend_bottom2 - 5),
                    self.font,
                    self.font_scale * 0.6, self.color, 1)
        cv2.line(frame_to_draw, (0, freq_ampl_legend_bottom2), (width, freq_ampl_legend_bottom2), self.color, 1)

        # draw the bpm number information
        legend_top = freq_ampl_legend_bottom2
        legend_bottom = legend_top + int(height * self.legend_relative_height)
        bpm_str = "Your pulse estimation is: %d bpm" % bpm
        cv2.putText(frame_to_draw, bpm_str, (5, legend_bottom),
                    self.font,
                    self.font_scale, self.color, 1)

        return

'''
TESTING PROCEDURE  
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