import cv2
import numpy as np
import time
import collections


import Window
import copy
import heart_rate_plot as hrp

class ScannerComponent:
    def __init__(self, window):
        self.window = window
        self.cap = False
        self.face = False
        self.forehead = False
        self.plotter = hrp.Plotter(1200, 350, 3)
        self.plotter.add_graph(0, "Avg Vals", (0, 255, 0))
        self.t0 = time.time()
        self.bufferSize = 250
        self.timeBuffer = collections.deque([])
        self.dataBuffer = collections.deque([])

    def set(self, cap, face, forehead):
        self.cap = cap
        self.face = face
        self.forehead = forehead

    def scan(self):
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
            self.dataBuffer.append(average)
            self.timeBuffer.append(time.time() - self.t0)
            if len(self.dataBuffer) > self.bufferSize:
                self.dataBuffer.popleft()
                self.timeBuffer.popleft()

            print(average)
            self.plotter.update(0, average)
            #foreheadGreenROI = foreheadColorROI[:, :, 1]


            x, y, w, h = self.face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.dft()


            self.window.draw(frame)
            self.plotter.plot_graphs()

            k = cv2.waitKey(1)

            if k % 256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                return False


