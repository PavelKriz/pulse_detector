import cv2
import Window
import copy


class FaceLockerComponent:
    def __init__(self, window):
        self.window = window
        self.cap = False
        # Load the cascade
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
        self.locked_face = (0, 0, 0, 0)
        self.face_was_locked = False
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.text_color = (255, 255, 255)
        self.background_color = (20, 20, 20)
        self.forehead = (1,1,1,1)

    def __lock_face_draw_text(self, frame):
        select_camera_str = "To lock the face press: space"
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

    @staticmethod
    def get_subface_coord(face_rect, fh_x, fh_y, fh_w, fh_h):
        x, y, w, h = face_rect
        return [int(x + w * fh_x - (w * fh_w / 2.0)),
                int(y + h * fh_y - (h * fh_h / 2.0)),
                int(w * fh_w),
                int(h * fh_h)]

    @staticmethod
    def draw_rectangle(frame, rectangle, col=(0, 0, 255)):
        x, y, w, h = rectangle
        cv2.rectangle(frame, (x, y), (x + w, y + h), col, 3)

    def set_cap(self, cap):
        self.cap = cap

    def __real_run(self):
        if not self.cap:
            return
        ret, frame = self.cap.read()
        if not ret:
            print("failed to grab frame")
            return False
        frame = cv2.flip(frame, 1)
        drawFrame = copy.deepcopy(frame)
        frame_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.equalizeHist(frame_grey, frame_grey)

        # Detect faces
        faces = self.face_cascade.detectMultiScale(frame_grey, scaleFactor=1.3,
                                              minNeighbors=4,
                                              minSize=(50, 50),
                                              flags=cv2.CASCADE_SCALE_IMAGE)

        for (x, y, w, h) in faces[0:1]:
            if w < 100 or h < 100:
                continue

            cv2.rectangle(drawFrame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # original
            # forehead1 = self.get_subface_coord([x, y, w, h], 0.5, 0.18, 0.25, 0.15)
            # experimental
            self.forehead = self.get_subface_coord([x, y, w, h], 0.5, 0.14, 0.3, 0.2)

            # draw rectangle
            self.draw_rectangle(drawFrame, self.forehead)

            # face rectangle of interest
            faceROI = frame_grey[y:y + h, x:x + w]

        # print
        self.__lock_face_draw_text(drawFrame)
        # Display the frame
        self.window.draw(drawFrame)

        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            return False
        if k % 256 == 32:
            # space pressed
            if len(faces) > 0:
                self.face_was_locked = True
                self.locked_face = faces[0]
            print("Locked:")
            return False

        return True

    def run(self):
        self.face_was_locked = False
        while True:
            ret = self.__real_run()
            if not ret:
                return

    def get_locked_face(self):
        if self.face_was_locked:
            return self.locked_face
        return

    def get_locked_forehead(self):
        if self.face_was_locked:
            return self.forehead
        return

