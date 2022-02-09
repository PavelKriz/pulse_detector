import cv2
import numpy as np
from pulse_detector_app import BPMData
from pulse_detector_app import config


# Components are self running sort of apps that are concerned with some part of the application
# ScannerComponent is class that handles the scanning in the application
class ScannerComponent:
    # constructor
    def __init__(self, window):
        self.window = window
        self.bufferSize = 250
        self.cap = False
        self.face = False
        self.forehead = False
        self.bpm_data = BPMData.BPMData()
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.text_color = (255, 255, 255)
        self.background_color = (20, 20, 20)
        self.flip = False

    # method used to draw the description
    def __scan_face_draw_text(self, frame):
        # the description text strings
        select_camera_str = "To lock new face press: N"
        end_app_str = "To quit press: ESC"

        # size of a text offset in pixels
        offset = 5

        # get the sizes of the texts in given order
        font_scale = config.RESOLUTIONS[config.USED_RESOLUTION_INDEX]['font_scale']
        text_size1 = cv2.getTextSize(select_camera_str, self.font, font_scale, 1)[0]
        text_size2 = cv2.getTextSize(end_app_str, self.font, font_scale, 1)[0]
        max_text_size = [max(text_size1[0], text_size2[0]),
                     max(text_size1[1], text_size2[1])]

        # get the size of the maximal possible text + some offset
        text_rectangle_size = [max_text_size[0] + 2 * offset, max_text_size[1] * 2 + offset * 3 ]
        cv2.rectangle(frame, (0, 0), text_rectangle_size, self.background_color, -1)

        # draw text
        text_start = [ offset, max_text_size [1] + offset]
        cv2.putText(frame, select_camera_str, text_start,
                    self.font,
                    font_scale, self.text_color, 1)

        # draw text
        text_start[1] += max_text_size[1] + offset
        cv2.putText(frame, end_app_str, text_start,
                    self.font,
                    font_scale, self.text_color, 1)

    # method used to draw the bpm - with a set style next to the forehead
    def __draw_bpm(self, frame):
        font_scale = config.RESOLUTIONS[config.USED_RESOLUTION_INDEX]['font_scale']
        # get the forehead
        x, y, w, h = self.forehead
        # set the text variables
        text_str = "%d bpm" % self.bpm_data.bpm
        text_size = np.array(cv2.getTextSize(text_str, self.font, font_scale, 1)[0])
        text_rectangle_size = np.array(1.5 * text_size, dtype=int)

        # draw the text and rectangle around
        offset = np.array((text_rectangle_size - text_size)/2, dtype=int)
        width_offset = 20
        pt1 = (x + w + width_offset, y + int(h / 2 - text_rectangle_size[1] / 2))
        pt2 = (pt1[0] + text_rectangle_size[0] + width_offset, pt1[1] + text_rectangle_size[1])
        cv2.rectangle(frame, pt1, pt2, self.background_color, -1)
        cv2.putText(frame, "%d bpm" % self.bpm_data.bpm, (pt1[0] + offset[0], pt2[1] - offset[1])  ,
                    self.font,
                    font_scale, self.text_color, 1)

    # set up the component
    def set(self, cap, face, forehead, flip):
        self.cap = cap
        self.face = face
        self.forehead = forehead
        self.flip = flip

    # run the scanning activity and window
    def scan(self):
        # reset data values
        self.__reset()

        # return if the camera object is not there
        if not self.cap:
            return

        # run the scanning until the application ends or the user wants to lock new face
        while True:
            # get return code and image frame information
            ret, frame = self.cap.read()
            if not ret:
                print("failed to grab frame")
                return

            # if the frame mirror option was chosen - flip the frame
            if self.flip:
                frame = cv2.flip(frame, 1)

            # select the forehead area
            fx, fy, fw, fh = self.forehead
            foreheadROI = frame[fy:fy + fh, fx:fx + fw, 0:3]
            foreheadROI[:, :, 0] = 0
            foreheadROI[:, :, 2] = 0

            # get the average of forehead pixels
            average = np.average(foreheadROI)

            # put data, analyze, plot
            self.bpm_data.put(average)
            self.bpm_data.analyze()
            self.bpm_data.plot()

            # select the face and draw it
            x, y, w, h = self.face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # draw the description
            self.__scan_face_draw_text(frame)
            # draw the bpm next to forehead
            self.__draw_bpm(frame)
            #draw the whole window

            self.window.draw(frame)

            # get the user input
            k = cv2.waitKey(1)
            # check the user input
            if k % 256 == 27:
                # ESC pressed
                # close the application
                print("Escape hit, closing...")
                return 0
            elif k % 256 == ord('n') or k % 256 == ord('N'):
                # the user wants to lock new face... return
                return 1

    def __reset(self):
        # the data are needed to be reset
        self.bpm_data = BPMData.BPMData()

