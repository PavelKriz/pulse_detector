import pulse_detector_app as pda
import cv2
from pulse_detector_app import Window
from pulse_detector_app import CameraChoiceComponent as ccp
from pulse_detector_app import FaceLockerComponent as flc
from pulse_detector_app import ScannerComponent as sc


# Main class managing the inner loop of switching windows
class App:
    def __init__(self):
        # init the window and components
        self.main_window = pda.Window.Window('Pulse detector')
        self.cameraChoiceComponent = ccp.CameraChoiceComponent(self.main_window)
        self.faceLockerComponent = flc.FaceLockerComponent(self.main_window)
        self.scannerComponent = sc.ScannerComponent(self.main_window)

    def run(self):
        # choose the camera
        ret = self.cameraChoiceComponent.choose_camera()
        if ret == 0:
            self.__clear()
            return

        # set up the locker component
        self.faceLockerComponent.set(self.cameraChoiceComponent.get_cap(), self.cameraChoiceComponent.flip)
        # inner loop that allows locking new faces and scanning them
        while True:
            # try to lock the face until the face is locked
            self.faceLockerComponent.face_was_locked = False
            while not self.faceLockerComponent.face_was_locked:
                ret = self.faceLockerComponent.run()
                # application has to end
                if ret == 0:
                    self.__clear()
                    return

            # set the face scanner
            self.scannerComponent.set(self.cameraChoiceComponent.get_cap(),
                                      self.faceLockerComponent.get_locked_face(),
                                      self.faceLockerComponent.get_locked_forehead(),
                                      self.cameraChoiceComponent.flip)
            # run the scan
            ret = self.scannerComponent.scan()
            # application has to end
            if ret == 0:
                self.__clear()
                return

        # TODO rescan option

    # release allocated resources
    def __clear(self):
        self.cameraChoiceComponent.get_cap().release()
        cv2.destroyAllWindows()




