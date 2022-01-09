import pulse_detector_app as pda
import cv2
from pulse_detector_app import Window
from pulse_detector_app import CameraChoiceComponent as ccp
from pulse_detector_app import FaceLockerComponent as flc
from pulse_detector_app import ScannerComponent as sc


class App:
    def __init__(self):
        self.main_window = pda.Window.Window('Pulse detector')
        self.cameraChoiceComponent = ccp.CameraChoiceComponent(self.main_window)
        self.faceLockerComponent = flc.FaceLockerComponent(self.main_window)
        self.scannerComponent = sc.ScannerComponent(self.main_window)

    def run(self):
        ret = self.cameraChoiceComponent.choose_camera()
        if ret == 0:
            self.__clear()
            return

        self.faceLockerComponent.set_cap(self.cameraChoiceComponent.get_cap())
        while True:
            self.faceLockerComponent.face_was_locked = False
            while not self.faceLockerComponent.face_was_locked:
                ret = self.faceLockerComponent.run()
                if ret == 0:
                    self.__clear()
                    return

            self.scannerComponent.set(self.cameraChoiceComponent.get_cap(),
                                      self.faceLockerComponent.get_locked_face(),
                                      self.faceLockerComponent.get_locked_forehead())
            ret = self.scannerComponent.scan()
            if ret == 0:
                self.__clear()
                return

        # TODO rescan option

    def __clear(self):
        self.cameraChoiceComponent.get_cap().release()
        cv2.destroyAllWindows()




