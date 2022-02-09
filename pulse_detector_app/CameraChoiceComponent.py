import cv2
import numpy as np
from pulse_detector_app import config


# Components are self running sort of apps that are concerned with some part of the application
# CameraChoiceComponent represents component taking care of choosing the correct camera
class CameraChoiceComponent:
    def __init__(self, window):
        self.window = window
        self.camera_chosen = False
        self.camera_index = 0
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.text_color = (255, 255, 255)
        self.background_color = (20, 20, 20)
        self.cap = False
        self.flip = False

    def __choose_camera_draw_text(self, frame):
        # the description text strings
        next_camera_str = "For next camera press: N"
        next_camera_res_str = "For webcam resolution change press: R"
        used_width = config.RESOLUTIONS[config.USED_RESOLUTION_INDEX]['width']
        used_height = config.RESOLUTIONS[config.USED_RESOLUTION_INDEX]['height']
        camera_res_str = "Webcam resolution is: %d x %d" % (used_width, used_height)
        select_camera_str = "To select this camera press: SPACE"
        toggle_mirror_str = "To toggle mirror on/off the camera press: F"
        end_app_str = "To quit press: ESC"

        # size of a text offset in pixels
        offset = 5

        # get the sizes of the texts in given order
        font_scale = config.RESOLUTIONS[config.USED_RESOLUTION_INDEX]['font_scale']
        text_size1 = cv2.getTextSize(next_camera_str, self.font, font_scale, 1)[0]
        text_size2 = cv2.getTextSize(next_camera_res_str, self.font, font_scale, 1)[0]
        text_size3 = cv2.getTextSize(camera_res_str, self.font, font_scale, 1)[0]
        text_size4 = cv2.getTextSize(select_camera_str, self.font, font_scale, 1)[0]
        text_size5 = cv2.getTextSize(toggle_mirror_str, self.font, font_scale, 1)[0]
        text_size6 = cv2.getTextSize(end_app_str, self.font, font_scale, 1)[0]
        max_text_size = [max(text_size1[0], text_size3[0], text_size2[0], text_size4[0], text_size5[0], text_size6[0]),
                     max(text_size1[1], text_size3[1], text_size2[1], text_size4[1], text_size5[1], text_size6[1])]

        # get the size of the maximal possible text + some offset
        text_rectangle_size = [max_text_size[0] + 2 * offset, max_text_size[1] * 6 + offset * 7 ]
        cv2.rectangle(frame, (0, 0), text_rectangle_size, self.background_color, -1)

        # draw text
        text_start = [ offset, max_text_size [1] + offset]
        cv2.putText(frame, next_camera_str, text_start,
                    self.font,
                    font_scale, self.text_color, 1)

        # draw text
        text_start[1] += max_text_size[1] + offset
        cv2.putText(frame, next_camera_res_str, text_start,
                    self.font,
                    font_scale, self.text_color, 1)

        # draw text
        text_start[1] += max_text_size[1] + offset
        cv2.putText(frame, camera_res_str, text_start,
                    self.font,
                    font_scale, self.text_color, 1)

        # draw text
        text_start[1] += max_text_size[1] + offset
        cv2.putText(frame, select_camera_str, text_start,
                    self.font,
                    font_scale, self.text_color, 1)

        # draw text
        text_start[1] += max_text_size[1] + offset
        cv2.putText(frame, toggle_mirror_str, text_start,
                    self.font,
                    font_scale, self.text_color, 1)

        # draw text
        text_start[1] += max_text_size[1] + offset
        cv2.putText(frame, end_app_str, text_start,
                    self.font,
                    font_scale, self.text_color, 1)

    # return chosen camera object
    def get_cap(self):
        if not self.cap:
            return
        return self.cap

    # method used to run the camera choosing window
    def choose_camera(self):
        index = 0
        changed_camera = True
        # run the loop until camera is chosen or application closed
        while not self.camera_chosen:
            # set up the camera
            if changed_camera:
                self.cap = cv2.VideoCapture(index)
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.RESOLUTIONS[config.USED_RESOLUTION_INDEX]['width'])
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.RESOLUTIONS[config.USED_RESOLUTION_INDEX]['height'])
                self.cap.set(cv2.CAP_PROP_FPS, config.FPS)
                changed_camera = False
            # get return code and image frame information
            ret, frame = self.cap.read()
            # handle not working indices (no camera connected)
            if not ret:
                if index == 0:
                    frame = np.zeros((config.RESOLUTIONS[config.USED_RESOLUTION_INDEX]['height'],
                            config.RESOLUTIONS[config.USED_RESOLUTION_INDEX]['width'],
                            3), dtype=np.uint8)
                else:
                    index = 0
                    changed_camera = True
                    continue

            # if the frame mirror option was chosen - flip the frame
            if self.flip:
                frame = cv2.flip(frame, 1)

            # draw the descriptions
            self.__choose_camera_draw_text(frame)
            # draw the frame
            self.window.draw(frame)

            # handle input
            k = cv2.waitKey(1)
            if k % 256 == 27:
                # ESC pressed
                # close application
                print("Escape hit, closing...")
                self.cap.release()
                cv2.destroyAllWindows()
                exit(0)
            elif k % 256 == ord('n') or k % 256 == ord('N'):
                # n or N pressed
                # change to next camera
                changed_camera = True
                index += 1
            elif k % 256 == ord('r') or k % 256 == ord('R'):
                # r or R pressed
                # change the resolution of the camera
                changed_camera = True
                config.USED_RESOLUTION_INDEX = (1 + config.USED_RESOLUTION_INDEX) % len(config.RESOLUTIONS)
            elif k % 256 == ord('f') or k % 256 == ord('F'):
                # f or F pressed
                # change the mirror setting
                if self.flip:
                    self.flip = False
                else:
                    self.flip = True
            elif k % 256 == 32:
                # space was pressed
                # choose this camera
                self.camera_index = index
                self.camera_chosen = True