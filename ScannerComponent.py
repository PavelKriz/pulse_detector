import cv2
import numpy as np
import time
import collections
import BPMPlotter


import Window
import copy
import heart_rate_plot as hrp

class BPMData:
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


    def put(self, data_val):
        self.dataBuffer.append(data_val)
        self.timeBuffer.append(time.time() - self.t0)
        if len(self.dataBuffer) > self.bufferSize:
            self.dataBuffer.popleft()
            self.timeBuffer.popleft()

    def initial_conditions(self):
        length = len(self.timeBuffer)
        if length < 40:
            return False
        return True

    def analyze(self):
        if not self.initial_conditions():
            return

        length = len(self.timeBuffer)
        time_elapsed = self.timeBuffer[length - 1] - self.timeBuffer[0]
        self.fps = float(length) / time_elapsed
        #print("length: %f time end: %f time begin: %f" % (float(length), self.timeBuffer[-1], self.timeBuffer[0]))
        #print("fps %f" % self.fps)

        data = np.array(self.dataBuffer)
        equidist_times = np.linspace(self.timeBuffer[0], self.timeBuffer[-1], length)
        equidist_data = np.interp(equidist_times, self.timeBuffer, data)
        # interpolated2 = np.hamming(length) * interpolated
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

        print("     fps: %f" % self.fps)
        print("     bpm: %f" % bpm)
        print("self.bpm: %f" % self.bpm)

    def plot(self):
        if not self.initial_conditions():
            return
        self.bpm_plotter.plot(self.bpm,
                              self.dataBuffer,
                              self.interesting_amplitudes,
                              self.interesting_frequencies)

class ScannerComponent:
    def __init__(self, window):
        self.window = window
        self.bufferSize = 250
        self.cap = False
        self.face = False
        self.forehead = False
        self.plotter = hrp.Plotter(1200, 350, int(1200 / self.bufferSize))
        self.plotter.add_graph(0, "Avg Vals", (0, 255, 0))
        self.bpm_data = BPMData()
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.text_color = (255, 255, 255)
        self.background_color = (20, 20, 20)

    def __scan_face_draw_text(self, frame):
        select_camera_str = "To lock new face press: N"
        end_app_str = "To quit press: ESC"

        offset = 5
        text_size1 = cv2.getTextSize(select_camera_str, self.font, 1.0, 1)[0]
        text_size2 = cv2.getTextSize(end_app_str, self.font, 1.0, 1)[0]
        max_text_size = [max(text_size1[0], text_size2[0]),
                     max(text_size1[1], text_size2[1])]

        text_rectangle_size = [max_text_size[0] + 2 * offset, max_text_size[1] * 2 + offset * 3 ]
        cv2.rectangle(frame, (0, 0), text_rectangle_size, self.background_color, -1)

        text_start = [ offset, max_text_size [1] + offset]
        cv2.putText(frame, select_camera_str, text_start,
                    self.font,
                    1.0, self.text_color, 1)

        text_start[1] += max_text_size[1] + offset
        cv2.putText(frame, end_app_str, text_start,
                    self.font,
                    1.0, self.text_color, 1)

    def set(self, cap, face, forehead):
        self.cap = cap
        self.face = face
        self.forehead = forehead

    def scan(self):
        self.__reset()

        if not self.cap:
            return

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("failed to grab frame")
                return

            frame = cv2.flip(frame, 1)

            fx, fy, fw, fh = self.forehead
            foreheadROI = frame[fy:fy + fh, fx:fx + fw, 0:3]
            foreheadROI[:, :, 0] = 0
            foreheadROI[:, :, 2] = 0

            average = np.average(foreheadROI)

            self.plotter.update(0, average)
            #foreheadGreenROI = foreheadColorROI[:, :, 1]
            self.bpm_data.put(average)
            self.bpm_data.analyze()
            self.bpm_data.plot()

            x, y, w, h = self.face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            self.__scan_face_draw_text(frame)
            self.window.draw(frame)

            self.plotter.plot_graphs()

            k = cv2.waitKey(1)

            if k % 256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                return 0
            elif k % 256 == ord('n') or k % 256 == ord('N'):
                return 1

    def __reset(self):
        # the data are needed to be reset
        self.bpm_data = BPMData()

