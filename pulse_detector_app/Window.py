import cv2


# class used to represent window
# here with the opencv is the window represented with just a string (label)
class Window:
    def __init__(self, label):
        self.label = label

    #draw a frame into a window
    def draw(self, frame):
        cv2.imshow(self.label, frame)
