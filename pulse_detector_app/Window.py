import cv2

class Window:
    def __init__(self, label):
        self.label = label

    def draw(self, frame):
        cv2.imshow(self.label, frame)
