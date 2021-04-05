from vidgear.gears import NetGear
import cv2
import numpy as np
import io
import socket
import struct
from PIL import Image
import sys

# define various tweak flags
options = {"flag": 0, "copy": False, "track": False, "max_retries": 5, "request_timeout": 20}

# Define Netgear Client at given IP address and define parameters 
# !!! change following IP address '192.168.x.xxx' with yours !!!
client = NetGear(
    address=sys.argv[1],
    port=sys.argv[2],
    protocol="tcp",
    pattern=1,
    receive_mode=True,
    logging=True,
    **options
)

def nothing(x):
    pass
cv2.namedWindow("Trackbars")
cv2.createTrackbar("LH","Trackbars",0,180,nothing)
cv2.createTrackbar("LS","Trackbars",0,255,nothing)
cv2.createTrackbar("LV","Trackbars",0,255,nothing)
cv2.createTrackbar("HH","Trackbars",180,180,nothing)
cv2.createTrackbar("HS","Trackbars",0,255,nothing)
cv2.createTrackbar("HV","Trackbars",0,255,nothing)


try:
    while True:
            # message to send over network
        target_data = "Hi, I'm the client."

        # receive frames from network
        frame = client.recv(return_data = target_data)

        # check for received frame if Nonetype
        if frame is None:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

        lbh = cv2.getTrackbarPos("LH",'Trackbars')
        ubh = cv2.getTrackbarPos("HH", 'Trackbars')
        lbs = cv2.getTrackbarPos("LS", 'Trackbars')
        ubs = cv2.getTrackbarPos("HS", 'Trackbars')
        lbv = cv2.getTrackbarPos("LV", 'Trackbars')
        ubv = cv2.getTrackbarPos("HV", 'Trackbars')

        l_b = np.array([lbh,lbs,lbv])
        u_b = np.array([ubh,ubs,ubv])

        mask =cv2.inRange(hsv,l_b,u_b)


        def getposHsv(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                print("HSV is", hsv[y, x])

        cv2.imshow('mask',mask)
        cv2.imshow("Image",frame)
        cv2.setMouseCallback('Image',getposHsv)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
# close output window
cv2.destroyAllWindows()
# safely cllose client
client.close()