import socket
import threading
import sys
import struct
import numpy
import threading
import pickle
import cv2
import json
import twitter, time
import tweepy
import os

def Main():
    consumer_key = 'xxxx'
    consumer_secret = 'xxxx'
    access_token_key = 'xxxx'
    access_token_secret = 'xxxx'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)
    HOST= socket.gethostbyname( '0.0.0.0' )
    PORT=int(5000)

    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #create socket (family,type)
    print ('Socket created')

    s.bind(('',5000)) #bind socket to adress
    print ('Socket bind complete')
    s.listen(1) #listen to the connections made to the socket
    print ('Socket now listening')

    conn,addr=s.accept() #accept a conection-conn is a new socket object , address bound to the socket on the other end of the connection
    mess= "Thank you for connecting"
    conn.send(mess.encode())
    data = b'' #bites literal

    c=0
    payload_size = struct.calcsize("L") #unsigned long size
    while True:
        while len(data) < payload_size:
            data += conn.recv(4096)  #recv data from socket - 4096 max amount of data
            c=c+1
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0] #unpack according to the str
        while len(data) < msg_size:
            data += conn.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        img= pickle.loads(frame_data, encoding='latin1') #read a pickled object hierarchy from a string
        face_cascade= cv2.CascadeClassifier('C:/Users/Alex/Desktop/face.txt') #load face cascade
        eye_cascade= cv2.CascadeClassifier('C:/Users/Alex/Desktop/eye.txt') #load eye cascade
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert data from camera to gray
        faces = face_cascade.detectMultiScale(gray)  #Detects faces of different sizes in the input image returned as a list of rectangles
        if len(faces)>0:
            api = tweepy.API(auth)
            t = time.strftime("%d-%m-%Y %H:%M:%S", time.gmtime())
            facess=str(faces)
            msg = "Alert !! Face detected at " + t + " : " + facess
#            api.update_status(msg)
            cv2.imwrite('opencv.png', img)
            api.update_with_media('opencv.png',msg)
            os.system("shutdown.exe /l")
        for (x, y, w, h) in faces:
            if c < 5:
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2) #draw rectangle (x,y) start point, end point, blue, alignment
                roi_gray = gray[y:y+h, x:x+w] #start point, end point
                roi_color = img[y:y+h, x:x+w] #for reimpose
                eyes = eye_cascade.detectMultiScale(roi_gray) #Detects eyes of different sizes in the input image returned as a list of rectangles
                print(c)
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2) #draw green rectangle
        cv2.imshow('img', img)

        k = cv2.waitKey(30)&0xff #waits for specified milliseconds for any keyboard event (esc)
        if k == 27:
            break

    cv2.destroyALLWindows() #destroys all of the opened HighGUI windows


if __name__ == '__main__':
    Main()
'''
class Server:
    socket_s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def __init__(self):
        host = '0.0.0.0'
        port = 5000
        self.socket_s.bind((host, port))
        self.socket_s.listen(1)
    def run(self):
        while True:
            conn, addr= self.socket_s.accept()
            Thread_s= threading.Thread(target= self.handler, args= (conn,addr))
            Thread_s.daemon= True
            Thread_s.start()

    def handler(self, conn, addr):
            data = b''
            payload_size = struct.calcsize("L")
            while True:
                while len(data) < payload_size:
                    data += conn.recv(4096)
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("L", packed_msg_size)[0]
                while len(data) < msg_size:
                    data += conn.recv(4096)
                frame_data = data[:msg_size]
                data = data[msg_size:]

                img= pickle.loads(frame_data)
                face_cascade= cv2.CascadeClassifier('C:/Users/Alex/Desktop/face.txt')
                eye_cascade= cv2.CascadeClassifier('C:/Users/Alex/Desktop/eye.txt')
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    roi_gray = gray[y:y+h, x:x+w]
                    roi_color = img[y:y+h, x:x+w]
                    eyes = eye_cascade.detectMultiScale(roi_gray)
                    for (ex, ey, ew, eh) in eyes:
                        cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
                cv2.imshow('img', img)
                k = cv2.waitKey(30)&0xff
                if k == 27:
                    break
            cv2.destroyALLWindows()


server= Server()
server.run()
'''
