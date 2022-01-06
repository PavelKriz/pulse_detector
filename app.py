import cv2
import Window
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
        self.cameraChoiceComponent.choose_camera()
        self.faceLockerComponent.set_cap(self.cameraChoiceComponent.get_cap())
        self.faceLockerComponent.run()
        if not self.faceLockerComponent.face_was_locked:
            print("error in face locking")
            exit(125)
        self.scannerComponent.set(self.cameraChoiceComponent.get_cap(),
                                  self.faceLockerComponent.get_locked_face(),
                                  self.faceLockerComponent.get_locked_forehead())
        self.scannerComponent.scan()
        # TODO rescan option





