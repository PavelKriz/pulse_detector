import cv2
import Window


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
        next_camera_str = "For next camera press: n"
        select_camera_str = "To select this camera press: space"
        end_app_str = "To quit press: ESC"

        offset = 5
        text_size1 = cv2.getTextSize(next_camera_str, self.font, 1.0, 1)[0]
        text_size2 = cv2.getTextSize(select_camera_str, self.font, 1.0, 1)[0]
        text_size3 = cv2.getTextSize(end_app_str, self.font, 1.0, 1)[0]
        max_text_size = [max(text_size1[0], text_size3[0], text_size2[0]),
                     max(text_size1[1], text_size3[1], text_size2[1])]

        text_rectangle_size = [max_text_size[0] + 2 * offset, max_text_size[1] * 3 + offset * 4 ]
        cv2.rectangle(frame, (0, 0), text_rectangle_size, self.background_color, -1)

        text_start = [ offset, max_text_size [1] + offset]
        cv2.putText(frame, next_camera_str, text_start,
                    self.font,
                    1.0, self.text_color, 1)

        text_start[1] += max_text_size[1] + offset
        cv2.putText(frame, select_camera_str, text_start,
                    self.font,
                    1.0, self.text_color, 1)

        text_start[1] += max_text_size[1] + offset
        cv2.putText(frame, end_app_str, text_start,
                    self.font,
                    1.0, self.text_color, 1)

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
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                self.cap.set(cv2.CAP_PROP_FPS, 30)
                changed_camera = False
            ret, frame = self.cap.read()
            if not ret:
                if index == 0:
                    print("Any camera wasn't found!")
                    exit(111)
                else:
                    index = 0
                    changed_camera = True
                    continue

            self.__choose_camera_draw_text(frame)
            self.window.draw(frame)

            k = cv2.waitKey(1)
            if k % 256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                cap.release()
                cv2.destroyAllWindows()
                exit(0)
            elif k % 256 == ord('n') or k % 256 == ord('N'):
                # n or N pressed
                changed_camera = True
                index += 1
            elif k % 256 == 32:
                # space was pressed
                self.camera_index = index
                self.camera_chosen = True