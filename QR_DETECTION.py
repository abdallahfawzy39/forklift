import cv2 
from cv2 import aruco


capture = cv2.VideoCapture(0) #This creates a video capture object and assigns it to the variable named capture
while True: #Our loop for video streaming
    ret, frame = capture.read() #reads frame from the camera stream and saves it into the variable "Capturing"
    cv2.imshow('camera', frame) #imshow is used to show the captured frame, the function takes a window name and a frame to show
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
    cv2.imshow('Aruco', frame_markers)
    if ids==None:
        print ("No markers detected")
    elif ids[0]==1:
        print ("This is marker 1")
    elif ids[0]==2:
        print ("This is marker 2")
    elif ids[0]==3:
        print("This is marker 3")
        
    # Check if the user has pressed Esc key, this is to break from the while true loop 
    c = cv2.waitKey(1)
    if c == 27:
        break

# Close the capturing device, releases the capture object as a resource to be used by other apps/scripts
capture.release()

# Close all windows
cv2.destroyAllWindows()