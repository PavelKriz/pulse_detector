import copy

import cv2
import io
import time
import heart_rate_plot as hrp
import app


app = app.App()
app.run()


'''
def get_subface_coord(face_rect, fh_x, fh_y, fh_w, fh_h):
    x, y, w, h = face_rect
    return [int(x + w * fh_x - (w * fh_w / 2.0)),
            int(y + h * fh_y - (h * fh_h / 2.0)),
            int(w * fh_w),
            int(h * fh_h)]


def draw_rectangle(frame, rectangle, col = (0, 0, 255)):
    x, y, w, h = rectangle
    cv2.rectangle(frame, (x, y), (x + w, y + h), col, 3)


# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

img_counter = 0

# TODO - Add function to choose camera at the beggining
cap = cv2.VideoCapture(2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)


plotter = hrp.Plotter(1200, 350, 10)
plotter.add_graph(0, "Avg Vals", (0, 255, 0))

detectFaces = True

# main loop
while(True):
    ret, frame = cap.read()
    if not ret:
        print("failed to grab frame")
        break
    drawFrame = copy.deepcopy( frame)
    frame_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.equalizeHist(frame_grey, frame_grey)

    # Detect faces
    faces = face_cascade.detectMultiScale(frame_grey,   scaleFactor=1.3,
                                                        minNeighbors=4,
                                                        minSize=(50, 50),
                                                        flags=cv2.CASCADE_SCALE_IMAGE)

    # Detect faces
    # faces = face_cascade.detectMultiScale(frame_grey)
    for (x,y,w,h) in faces:
        if w < 100 or h < 100:
            continue

        cv2.rectangle(drawFrame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        forehead1 = get_subface_coord([x, y, w, h], 0.5, 0.18, 0.25, 0.15)



        #draw rectangle
        draw_rectangle(drawFrame, forehead1)

        # face rectangle of interest
        faceROI = frame_grey[y:y+h,x:x+w]
        fx, fy, fw, fh = forehead1
        foreheadColorROI = frame[fy:fy+fh, fx:fx+fw, 0:3]
        foreheadColorROI[:, :, 0] = 0
        foreheadColorROI[:, :, 2] = 0
        foreheadGreenROI = foreheadColorROI[:,:, 1]
        mean = foreheadGreenROI.mean()
        print(mean)
        plotter.update(0,mean)
        cv2.imshow('forehead', foreheadColorROI)

        #-- In each face, detect eyes
        #eyes = eye_cascade.detectMultiScale(faceROI)
        #cv2.imshow('Crop', faceROI)

        #for (x2,y2,w2,h2) in eyes:
        #    eye_center = (x + x2 + w2//2, y + y2 + h2//2)
        #    radius = int(round((w2 + h2)*0.25))
        #    cv2.circle(drawFrame, eye_center, radius, (255, 0, 0 ), 2)


    # Display the frame
    cv2.imshow('Pulse detector', drawFrame)
    plotter.plot_graphs()

    k = cv2.waitKey(1)
    if k % 256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k % 256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cap.release()
cv2.destroyAllWindows()

'''