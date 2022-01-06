import cv2
import Window
import CameraChoiceComponent as ccp
import FaceLockerComponent as flc

class App:
    def __init__(self):
        self.main_window = Window.Window('Pulse detector')
        self.cameraChoiceComponent = ccp.CameraChoiceComponent(self.main_window)
        self.faceLockerComponent = flc.FaceLockerComponent(self.main_window)

    def run(self):
        self.cameraChoiceComponent.choose_camera()
        self.faceLockerComponent.set_cap(self.cameraChoiceComponent.get_cap())
        self.faceLockerComponent.run()





