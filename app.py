import Window
import cv2
import CameraChoiceComponent as ccp
import FaceLockerComponent as flc
import ScannerComponent as sc


class App:
    def __init__(self):
        self.main_window = Window.Window('Pulse detector')
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




