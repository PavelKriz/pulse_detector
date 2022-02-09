import time
import collections
import numpy as np
from pulse_detector_app import BPMPlotter


# class that works with scanned data - stores them (it is a sort of buffer container) and analysis them
class BPMData:
    # constructor, size is the size of data buffer
    def __init__(self, size=250):
        self.t0 = time.time()
        self.bufferSize = size
        self.timeBuffer = collections.deque([])
        self.interesting_amplitudes = []
        self.interesting_frequencies = []
        self.dataBuffer = collections.deque([])
        self.fps = 0
        self.bpm = 0
        self.bpm_plotter = BPMPlotter.BPMPlotterWrapper()

    # method that is supposed to be used to insert data and remove old ones
    def put(self, data_val):
        self.dataBuffer.append(data_val)
        self.timeBuffer.append(time.time() - self.t0)
        if len(self.dataBuffer) > self.bufferSize:
            self.dataBuffer.popleft()
            self.timeBuffer.popleft()

    # checking the minimal length for analysis
    def initial_conditions(self):
        length = len(self.timeBuffer)
        if length < 40:
            return False
        return True

    # the analysis of the data
    def analyze(self):
        if not self.initial_conditions():
            return

        # calc the time data
        length = len(self.timeBuffer)
        time_elapsed = self.timeBuffer[length - 1] - self.timeBuffer[0]
        self.fps = float(length) / time_elapsed

        data = np.array(self.dataBuffer)
        equidist_times = np.linspace(self.timeBuffer[0], self.timeBuffer[-1], length)
        equidist_data = np.interp(equidist_times, self.timeBuffer, data)
        # because of what says the Shannon theorem length / 2 + 1 frequencies bin is return
        # Oficial doc: If n is even, the length of the transformed axis is (n/2)+1. If n is odd, the length is (n+1)/2.
        np_fft = np.fft.rfft(equidist_data)
        np_fft_len = len(np_fft)
        # phase = np.phase(raw)

        # here we get the amplitudes - making them smaller appropriately
        amplitudes = 2 / length * np.abs(np_fft)
        # i tried following line but it would have to be cut
        # frequencies = np.fft.fftfreq(length) * length * 1 / time_elapsed * 60
        # creating the frequencies "manually"
        frequencies = float(self.fps) / length * np.arange(np_fft_len)
        # scale them to minutes - heart rate is usually measured per minute
        frequencies = 60. * frequencies

        # let's cut of the frequencies to range 55-170 per minute (typical range for pulse)
        indices = np.where((frequencies > 55) & (frequencies < 170))
        # get the interesting frequencies and amplitudes as well
        self.interesting_amplitudes = amplitudes[indices]
        self.interesting_frequencies = frequencies[indices]

        # find the most common
        bpm_index = np.argmax(self.interesting_amplitudes)
        bpm = self.interesting_frequencies[bpm_index]

        # smooth the bpm and ignore begining when it is zero
        if self.bpm < 0.1:
            self.bpm = bpm
        else:
            self.bpm = 0.99 * self.bpm + 0.01 * bpm

    # plotting the data individually in separate window
    def plot(self):
        if not self.initial_conditions():
            return
        self.bpm_plotter.plot(self.bpm,
                              self.dataBuffer,
                              self.interesting_amplitudes,
                              self.interesting_frequencies)