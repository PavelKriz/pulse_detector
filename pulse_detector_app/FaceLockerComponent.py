import cv2
import copy
from pulse_detector_app import config


# Components are self running sort of apps that are concerned with some part of the application
# FaceLockerComponent is a class managing the face locking in the application
class FaceLockerComponent:
    # constructor
    def __init__(self, window):
        self.window = window
        self.cap = False
        # Load the cascade
        self.face_cascade = cv2.CascadeClassifier('pulse_detector_app/haarcascade_frontalface_alt.xml')
        self.locked_face = (0, 0, 0, 0)
        self.face_was_locked = False
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.text_color = (255, 255, 255)
        self.background_color = (20, 20, 20)
        self.forehead = (1,1,1,1)
        self.flip = False

    # draw the face locking window description
    def __lock_face_draw_text(self, frame):
        # the description text strings
        select_camera_str = "To lock the face press: space"
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

    # get the sub face coordinates
    @staticmethod
    def get_subface_coord(face_rect, fh_x, fh_y, fh_w, fh_h):
        x, y, w, h = face_rect
        return [int(x + w * fh_x - (w * fh_w / 2.0)),
                int(y + h * fh_y - (h * fh_h / 2.0)),
                int(w * fh_w),
                int(h * fh_h)]

    # draw the rectangle into given frame
    @staticmethod
    def draw_rectangle(frame, rectangle, color=(0, 0, 255)):
        x, y, w, h = rectangle
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 3)

    # method used to set the camera object and flip setting
    def set(self, cap, flip):
        self.cap = cap
        self.flip = flip

    # method that does the job (should be run in a loop checking the return code)
    def __real_run(self):
        # check if the camera object is there
        if not self.cap:
            return

        # get return code and image frame information
        ret, frame = self.cap.read()
        if not ret:
            print("failed to grab frame")
            return False
        # if the frame mirror option was chosen - flip the frame
        if self.flip:
            frame = cv2.flip(frame, 1)
        # create the frame that will be displayed
        # the original one will be used for data scan (so the other image information drawn is not used)
        drawFrame = copy.deepcopy(frame)
        # convert image to greyscale
        frame_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # equalize histogram - for greater range of changes
        cv2.equalizeHist(frame_grey, frame_grey)

        # Detect faces
        faces = self.face_cascade.detectMultiScale(frame_grey, scaleFactor=1.3,
                                              minNeighbors=4,
                                              minSize=(50, 50),
                                              flags=cv2.CASCADE_SCALE_IMAGE)

        # go through the faces
        for (x, y, w, h) in faces[0:1]:
            # neglect some small fake faces (there are created such during the locking)
            if w < 100 or h < 100:
                continue

            # draw the rectangle around the face
            cv2.rectangle(drawFrame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # experimental setup
            self.forehead = self.get_subface_coord([x, y, w, h], 0.5, 0.14, 0.3, 0.2)

            # draw rectangle around forehead
            self.draw_rectangle(drawFrame, self.forehead)

            # face rectangle of interest
            faceROI = frame_grey[y:y + h, x:x + w]

        # print
        self.__lock_face_draw_text(drawFrame)
        # Display the frame
        self.window.draw(drawFrame)

        # get the user input
        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            # close the application
            print("Escape hit, closing...")
            return False

        if k % 256 == 32:
            # space pressed
            # lock the faces
            if len(faces) > 0:
                self.face_was_locked = True
                self.locked_face = faces[0]
                print("Locked...")
            else:
                print("No faces to loc...")
            return False

        return True

    # method  used to run the face locking
    def run(self):
        self.face_was_locked = False
        while True:
            ret = self.__real_run()
            if not ret:
                return

    # returns the locked face
    def get_locked_face(self):
        if self.face_was_locked:
            return self.locked_face
        return

    # returns the forehead of a locked face
    def get_locked_forehead(self):
        if self.face_was_locked:
            return self.forehead
        return

