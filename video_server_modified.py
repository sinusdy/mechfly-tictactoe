import io
import socket
import struct
from PIL import Image
import cv2
import numpy as np
import sys
#Choose which algorithm to run. Comment out the unused one
from TicTacToeModified import *
# from minimax import *

kernal = np.ones((5,5),np.uint8)

#Greenmask Values
l_bgreen = np.array([40, 50, 50])
u_bgreen = np.array([70, 255, 255])
#Whitemask Values
l_bwhite = np.array([0,0,240])
u_bwhite = np.array([255,15,255])
#Bluemask Values
l_bblue = np.array([110, 50, 50])
u_bblue = np.array([130, 255, 255])

#Tic Tac Toe Box
datalist = []           #list of all the data in combined tuple. Tuple order = x, y, colour, w, h
final_list = []         #list of the sorted data in combined tuple
arrangedcolour = []     #tic tac toe board represented as -1, 0, and 1
#Colours wanted
white = 0
red = -1
green = 1
#Contour Count
contour_count = 0

def exclude_repeated(x,y,colour,w,h):
    distinct = True
    if (len(datalist)) != 0:
        for i in range(len(datalist)):
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
    if (len(datalist) == 9):
        datalist = sorted(datalist,key=lambda x: (x[1], x[0]))
        # Double check the sorted array in y coordinate
        row = 0
        while row < 3:
            rowcorrect = True
            col = 0
            while col < 2 :
                index = row * 3 + col
                if (datalist[index][0] > datalist[index + 1][0] and (abs(datalist[index][1] - datalist[index + 1][1]) < 0.1 * datalist[index][4])):
                    rowcorrect = False
                    break
                col += 1
            if (rowcorrect == False):
                current_row = []
                col = 0
                while col < 3:
                    current_row.append(datalist[row * 3 + col])
                    col += 1
                sorted_row = sorted(current_row, key = lambda x: (x[0]))
                for box in sorted_row :
                    final_list.append(box)
            else :
                col = 0
                while col < 3:
                    final_list.append(datalist[row * 3 + col])
                    col += 1
            row += 1
        for i in final_list:
            arrangedcolour.append(i[2])
        print(arrangedcolour)    
        return True    
    else:
        return False

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

        #Convert frame to hsv
        hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

        # Blue Mask = Red Mask
        maskblue = cv2.inRange(hsv, l_bblue, u_bblue)

        # Green Mask
        maskgreen = cv2.inRange(hsv, l_bgreen, u_bgreen)

        # White Mask
        maskwhite = cv2.inRange(hsv, l_bwhite, u_bwhite)

        # Further Image Processing
        dilategreen = cv2.dilate(maskgreen, kernal, iterations=5)
        closegreen = cv2.morphologyEx(dilategreen, cv2.MORPH_CLOSE, kernal, iterations=1)

        dilateblue = cv2.dilate(maskblue, kernal, iterations=5)
        closeblue = cv2.morphologyEx(dilateblue, cv2.MORPH_CLOSE, kernal, iterations=1)

        dilatewhite = cv2.dilate(maskwhite, kernal, iterations=5)
        closewhite = cv2.morphologyEx(dilatewhite, cv2.MORPH_CLOSE, kernal, iterations=1)

        # Find and place contours for red & green mask
        contoursblue, hierarchyblue = cv2.findContours(closeblue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contoursgreen, hierachrygreen = cv2.findContours(closegreen, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contourswhite, hierachrywhite = cv2.findContours(closewhite, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contoursgreen:
            (x, y, w, h) = cv2.boundingRect(contour)
            if cv2.contourArea(contour) > 2000:
                exclude_repeated(x, y, green, w, h)
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        for contour in contoursblue:
            (x, y, w, h) = cv2.boundingRect(contour)
            if cv2.contourArea(contour) > 2000:
                exclude_repeated(x, y, red, w, h)
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

        for contour in contourswhite:
            (x, y, w, h) = cv2.boundingRect(contour)
            if cv2.contourArea(contour) > 2000:
                exclude_repeated(x, y, white, w, h)
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 255), 2)

        # Sort and modify list
        if (sort_list(datalist)== True ):
            print('Current State:')
            print(arrangedcolour)
            print("AI Suggestion:")
            suggest_move_pos = suggest_move(arrangedcolour)
            print(suggest_move_pos)
            # Display Game Over for this condition
            if (suggest_move_pos == -1):
                text = "GAME OVER"
                data = final_list[0]
            else:         
                # Display suggested move position with payload name text
                data = final_list[suggest_move_pos]
                cv2.rectangle(image, (data[0], data[1]),
                        (data[0] + data[3], data[1] + data[4]),
                        (0, 255, 255), 3)
                text = payloadname(suggest_move_pos)
            cv2.putText(image, text, (data[0] - 5, data[1] - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255))
            # Display video
            cv2.imshow('Video',frame)
        else:
            print('Align properly')
        datalist.clear()
        final_list.clear()
        arrangedcolour.clear()    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
finally:
    connection.close()
    server_socket.close()
