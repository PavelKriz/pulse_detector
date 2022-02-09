# Pulse Detector
<img src="Pulse_detector.png"
            style="max-width:100%">

## Idea
Main idea is about creating application in Python, that would detect and display the pulse frequency. The output values are between 55 and 170 for one person.
	
## Descritption
The application looks like this:
        <img src="Pulse_detector.png"
            style="max-width:100%">
	
In the previous image can be seen the main part of the application, which is displayed in two windwos. The camera settings is easy and with the face locking mechanism is visible on the next images: 
        <img src="Pulse_detector_camera_setup.jpg"
            style="max-width:100%">
        <img src="Pulse_detector_face_setup.jpg"
            style="max-width:100%">
            
It is good to note, that on first sight unpractical face locking, is actualy important for the accuracy of meassurements.

### Accuracy

  The accuracy was tested with the fitness armband Fitbit Charge 4, which meassures heartrate on the wrist (quite accurate armband at the time). It was shown that the accuracy of the meassurements is only approximate (same as in other seen and tested solutions) and mainly depends on the camera quality and video compression. It was tested on four cameras total on which three gave normal accuracy (among the set) and using one of them the application gave much more accurate results. 

There is one image frm testing which shows happy case, when the detections matches (the real one still might be bit different):
        <img src="happy.jpg"
            style="max-width:50%">
	
On this image the innacuracy is visible. The overall is wrong, but at the moment, the current pulse was meassured correctly (most dominant frequency):
        <img src="not_so_happy.jpg"
            style="max-width:50%">
	
## Installation and run
The `Python 3` is needed with the installed package `opencv-python`. To run the program it is needed to type `python3 ./pulse_detector.py` in the correct folder in terminal.

## Other already created solutions at the time
There are already existing solutions for that, one of them is <a href="https://github.com/thearn/webcam-pulse-detector">webcam-pulse-detector</a>. That one is in Python, but there is also one in <a href="https://github.com/serghov/heartRate">Javascript</a>. Most detectors (our as well) uses forehead as detecting zone, but <a href="https://www.youtube.com/watch?v=IV51CYZsBOU">this one</a> uses cheeks. 



