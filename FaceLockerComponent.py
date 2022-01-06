import cv2
import Window
import copy


class FaceLockerComponent:
    def __init__(self, window):
        self.window = window
        self.cap = False
        # Load the cascade
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

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
        drawFrame = copy.deepcopy(frame)
        frame_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.equalizeHist(frame_grey, frame_grey)

        # Detect faces
        faces = self.face_cascade.detectMultiScale(frame_grey, scaleFactor=1.3,
                                              minNeighbors=4,
                                              minSize=(50, 50),
                                              flags=cv2.CASCADE_SCALE_IMAGE)

        for (x, y, w, h) in faces:
            if w < 100 or h < 100:
                continue

            cv2.rectangle(drawFrame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            forehead1 = self.get_subface_coord([x, y, w, h], 0.5, 0.18, 0.25, 0.15)

            # draw rectangle
            self.draw_rectangle(drawFrame, forehead1)

            # face rectangle of interest
            faceROI = frame_grey[y:y + h, x:x + w]

        # Display the frame
        self.window.draw(drawFrame)

        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            return False

        return True

    def run(self):
        while True:
            ret = self.__real_run()
            if not ret:
                return
