import io
import socket
import struct
from PIL import Image
import cv2
import numpy as np
import sys
from TicTacToeModified import *

kernal = np.ones((5,5),np.uint8)

l_b = np.array([0, 125, 125])
u_b = np.array([5, 255, 255])
l_b2 = np.array([175, 125, 125])
u_b2 = np.array([180, 255, 255])
#Greenmask Values
l_bgreen = np.array([55, 50, 50])
u_bgreen = np.array([65, 255, 255])
#Whitemask Values
l_bwhite = np.array([0,0,255])
u_bwhite = np.array([255,15,255])

#Tic Tac Toe Box
xlist = []
ylist = []
colourlist = []
datalist = []   #list of all the data in combined tuple. Tuple order = x, y, colour, w, h
#Colours wanted
white = ' '
red = 'O'
green = 'X'
#Contour Count
contour_count = 0
#Width and Height Average
widthlist = []
heightlist = []

def exclude_repeated(x,y,colour,w,h):
    distinct = True
    if (len(datalist)) != 0:
        for i in range(len(datalist) + 1):
            if ((x < 1.1 * datalist[i][0] and x > 0.9 * datalist[i][0]) and (y < 1.1 * datalist[i][1] and y > 1.1 * datalist[i][1])):
                distinct = False
                break
    if (distinct == True):
        tup = x, y, colour, w, h
        datalist.append(tup)

def payloadname(suggest_move_pos):
    if (suggest_move_pos == 4):
        return "Eraser"
    elif (suggest_move_pos == 0 or suggest_move_pos == 2 or suggest_move_pos == 6 or suggest_move_pos == 8):
        return "Pyramid"
    elif (suggest_move_pos == 1 or suggest_move_pos == 3 or suggest_move_pos == 5 or suggest_move_pos == 7):
        return "Rectangle"

def sort_list(datalist):
    arrangedcolour = []
    sorted(datalist,key=lambda x: (x[0], x[1]))
    for i in range(len(datalist)):
        arrangedcolour[i] = datalist[i][2]
    return arrangedcolour

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind((sys.argv[1], int(sys.argv[2])))  
server_socket.listen(0)
print("Listening")
connection = server_socket.accept()[0].makefile('rb')
try:
    img = None
    while True:
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        image_stream.seek(0)
        image = Image.open(image_stream)
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        maskred1 = cv2.inRange(hsv, l_b, u_b)
        maskred2 = cv2.inRange(hsv, l_b2, u_b2)
        maskred = maskred1 + maskred2

        # Green Mask
        maskgreen = cv2.inRange(hsv, l_bgreen, u_bgreen)

        # White Mask
        maskwhite = cv2.inRange(hsv, l_bwhite, u_bwhite)

        # Further Image Processing
        dilategreen = cv2.dilate(maskgreen, kernal, iterations=5)
        closegreen = cv2.morphologyEx(dilategreen, cv2.MORPH_CLOSE, kernal, iterations=1)

        dilatered = cv2.dilate(maskred, kernal, iterations=5)
        closered = cv2.morphologyEx(dilatered, cv2.MORPH_CLOSE, kernal, iterations=1)

        dilatewhite = cv2.dilate(maskwhite, kernal, iterations=5)
        closewhite = cv2.morphologyEx(dilatewhite, cv2.MORPH_CLOSE, kernal, iterations=1)

        # Find and place contours for red & green mask
        contoursred, hierarchyred = cv2.findContours(closered, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contoursgreen, hierachrygreen = cv2.findContours(closegreen, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contourswhite, hierachrywhite = cv2.findContours(closewhite, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contoursgreen:
            (x, y, w, h) = cv2.boundingRect(contour)
            if cv2.contourArea(contour) > 2000:
                exclude_repeated(x, y, green, w, h)
                widthlist.append(w)
                heightlist.append(h)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        for contour in contoursred:
            (x, y, w, h) = cv2.boundingRect(contour)
            if cv2.contourArea(contour) > 2000:
                exclude_repeated(x, y, red, w, h)
                widthlist.append(w)
                heightlist.append(h)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

        for contour in contourswhite:
            (x, y, w, h) = cv2.boundingRect(contour)
            if cv2.contourArea(contour) > 2000:
                exclude_repeated(x, y, white, w, h)
                widthlist.append(w)
                heightlist.append(h)
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)
        # Sort and modify list
        if len(datalist) <= 9:
            sorted_list = sort_list(datalist)
        elif len(datalist) > 9:
            datalist.clear()
            sorted_list = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
        cv2.imshow('Video',img)
        print('Current State:')
        show_field(sorted_list)
        print("AI Suggestion:")
        suggest_move_pos = suggest_move(sorted_list)
        sorted_list[suggest_move_pos] = 'X'
        # Display suggested move position with payload name text
        boxFrame = cv2.rectangle(img, (datalist[suggest_move_pos][0], datalist[suggest_move_pos][1]), 
                                (datalist[suggest_move_pos][0] + datalist[suggest_move_pos][3], 
                                datalist[suggest_move_pos][1] + datalist[suggest_move_pos][4]), 
                                (0, 0, 0), 3)  
        text = payloadname(suggest_move_pos)         
        cv2.putText(img, text, (datalist[suggest_move_pos][0], datalist[suggest_move_pos][1]), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0))
        # Print field in terminal
        show_field(sorted_list)
        if cv2.waitKey(1) & 0xFF == ord('q'):
           break
    cv2.destroyAllWindows()
finally:
    connection.close()
    server_socket.close()
