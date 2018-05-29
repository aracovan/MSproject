import cv2
import numpy as np
import socket
import sys
import pickle #serialize/deserialize structure
import struct
import threading

def Main():

        host = socket.gethostbyname('AlexPC')
        port = 5000
        cap=cv2.VideoCapture(0)
        socket_c= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_c.connect((host,port))
        print (host)
        while True:
            ret, img=cap.read()  #ret- true, false- from getting the camera frame  img- the next frame
            data = pickle.dumps(img, protocol=2) #return the pickled representation of the object as a string
            socket_c.sendall(struct.pack("L", len(data))+data) #send data to the socket

if __name__ == '__main__':
    Main()
