import cv2
import numpy as np

from pulse_detector_app import config


class CameraChoiceComponent:
    def __init__(self, window):
        self.window = window
        self.camera_chosen = False
        self.camera_index = 0
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.text_color = (255, 255, 255)
        self.background_color = (20, 20, 20)
        self.cap = False

    def __choose_camera_draw_text(self, frame):
        next_camera_str = "For next camera press: N"
        next_camera_res_str = "For webcam resolution change press: R"
        used_width = config.RESOLUTIONS[config.USED_RESOLUTION_INDEX]['width']
        used_height = config.RESOLUTIONS[config.USED_RESOLUTION_INDEX]['height']
        camera_res_str = "Webcam resolution is: %d x %d" % (used_width, used_height)
        select_camera_str = "To select this camera press: SPACE"
        end_app_str = "To quit press: ESC"

        offset = 5
        font_scale = config.RESOLUTIONS[config.USED_RESOLUTION_INDEX]['font_scale']
        text_size1 = cv2.getTextSize(next_camera_str, self.font, font_scale, 1)[0]
        text_size2 = cv2.getTextSize(next_camera_res_str, self.font, font_scale, 1)[0]
        text_size3 = cv2.getTextSize(camera_res_str, self.font, font_scale, 1)[0]
        text_size4 = cv2.getTextSize(select_camera_str, self.font, font_scale, 1)[0]
        text_size5 = cv2.getTextSize(end_app_str, self.font, font_scale, 1)[0]
        max_text_size = [max(text_size1[0], text_size3[0], text_size2[0], text_size4[0], text_size5[0]),
                     max(text_size1[1], text_size3[1], text_size2[1], text_size4[1], text_size5[1])]

        text_rectangle_size = [max_text_size[0] + 2 * offset, max_text_size[1] * 5 + offset * 6 ]
        cv2.rectangle(frame, (0, 0), text_rectangle_size, self.background_color, -1)

        text_start = [ offset, max_text_size [1] + offset]
        cv2.putText(frame, next_camera_str, text_start,
                    self.font,
                    font_scale, self.text_color, 1)

        text_start[1] += max_text_size[1] + offset
        cv2.putText(frame, next_camera_res_str, text_start,
                    self.font,
                    font_scale, self.text_color, 1)

        text_start[1] += max_text_size[1] + offset
        cv2.putText(frame, camera_res_str, text_start,
                    self.font,
                    font_scale, self.text_color, 1)

        text_start[1] += max_text_size[1] + offset
        cv2.putText(frame, select_camera_str, text_start,
                    self.font,
                    font_scale, self.text_color, 1)

        text_start[1] += max_text_size[1] + offset
        cv2.putText(frame, end_app_str, text_start,
                    self.font,
                    font_scale, self.text_color, 1)

    def get_cap(self):
        if not self.cap:
            return
        return self.cap

    def choose_camera(self):
        index = 0
        changed_camera = True
        while not self.camera_chosen:
            if changed_camera:
                self.cap = cv2.VideoCapture(index)
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.RESOLUTIONS[config.USED_RESOLUTION_INDEX]['width'])
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.RESOLUTIONS[config.USED_RESOLUTION_INDEX]['height'])
                self.cap.set(cv2.CAP_PROP_FPS, config.FPS)
                changed_camera = False
            ret, frame = self.cap.read()
            if not ret:
                if index == 0:
                    frame = np.zeros((config.RESOLUTIONS[config.USED_RESOLUTION_INDEX]['width'],
                            config.RESOLUTIONS[config.USED_RESOLUTION_INDEX]['height'],
                            3))
                else:
                    index = 0
                    changed_camera = True
                    continue

            frame = cv2.flip(frame, 1)
            self.__choose_camera_draw_text(frame)
            self.window.draw(frame)

            k = cv2.waitKey(1)
            if k % 256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                self.cap.release()
                cv2.destroyAllWindows()
                exit(0)
            elif k % 256 == ord('n') or k % 256 == ord('N'):
                # n or N pressed
                changed_camera = True
                index += 1
            elif k % 256 == ord('r') or k % 256 == ord('R'):
                # r or R pressed
                changed_camera = True
                config.USED_RESOLUTION_INDEX = (1 + config.USED_RESOLUTION_INDEX) % len(config.RESOLUTIONS)
            elif k % 256 == 32:
                # space was pressed
                self.camera_index = index
                self.camera_chosen = True