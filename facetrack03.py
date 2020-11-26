#Written by RoboticsbyTk (roboticsbytk.blogspot.com)
#Date: 26/11/2020
#This code takes in a video stream from a USB camera and uses the Haar Cascades
#to detect front facing faces and profiles shots.
#It establishes a Serial Communication with an Arduino Board and sends the coordinates
#of the detected faces to the Board.

#This code was inspired mostly by the project written by Harsh Dethe 
# link: https://create.arduino.cc/projecthub/WolfxPac/face-tracking-using-arduino-b35b6b



import cv2
import sys
import serial
#Path to the Pretrained Classifier XML files are loaded
#path-> Detects Frontal Face
#path2 -> Profile Face
path="haarcascade_frontalface_default.xml"
path2="haarcascade_profileface.xml"
#loading the class with the path
facecascade=cv2.CascadeClassifier(path)
profcascade=cv2.CascadeClassifier(path2)

#Accesses the stream from the DSLR/USB camera
#if you want to use your laptop camera use -> "/dev/video0"
video=cv2.VideoCapture("/dev/video1")

#Establishes Serial Link with the arduino
arduino = serial.Serial('/dev/ttyACM0', 38400) #Check your Serial Port's name using the Arduino IDE
signal=0 #this variable is used to make sure only either the front face or profile face is sent once
print("Connected to arduino...")

while True:
	ret,frame=video.read() #Stores each incoming frame to frame
	frame=cv2.resize(frame,(0,0),fx=0.5,fy=0.5) #Makes the image size smaller
	frame=cv2.flip(frame,1) #Flips the image
	
	#uncomment line below if you want to size of image	
	#print("Height:{}, Width:{}".format(frame.shape[0],frame.shape[1]))
	gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) #Converts to grayscale
	 
	#Starts the detection of front facing faces and profile shots
	#Notice the tuned variables
	faces=facecascade.detectMultiScale(gray,scaleFactor=1.5,minNeighbors=6,minSize=(15,15))
	profile=profcascade.detectMultiScale(gray,scaleFactor=1.5,minNeighbors=3,minSize=(10,10))
	
	#Code below is used to draw all the faces ( above a certain area threshold) onto the frame
	for (x,y,w,h) in faces:
		 
		
		if w*h>2910:
			#Creates boundary box around face
			cv2.rectangle(frame,(x,y),(x+w,y+h),(0,155,255),2)
			cv2.putText(frame,"Human Being?",(x,y-10),0,0.5,(0,155,255),2)
			 
			#Stores X-Y coordinate
			xx = int(x+(x+h))/2
			yy = int(y+(y+w))/2
			center = (int(xx),int(yy))
			#Encodes the data in a certain format "X__Y__Z" 
			data = "X{0:d}Y{1:d}Z".format(int(xx), int(yy))
			 
			
			 
			arduino.write(data.encode()) #Writes to Serial Port
			signal=1 #Once Data is sent we set signal to high
			print ("output = '" +data+ "'")
		else:
			signal=0

	#Does the ssame thing for Profile shots
	for (x,y,w,h) in profile:
			 
		if w*h>4000:
			
			xx = int(x+(x+h))/2
			yy = int(y+(y+w))/2
			center = (int(xx),int(yy))
			#If no face coordinates were sent previously, then we can send the coordinates to the Arduino and draw the boundary around the person			 
			if signal==0:
		
				cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
				cv2.putText(frame,"Profile View",(x,y-10),0,0.5,(0,255,255),2)
				data = "X{0:d}Y{1:d}Z".format(int(xx), int(yy))
				 
				arduino.write(data.encode())
				 
				
	 
	signal=0 #Sets it to low after each iteration
	cv2.imshow("Frame",frame) #Display frame with detected faces labelled
	#The code below is written so that you can exit the window using "q" 
	ch=cv2.waitKey(1)
	if ch &0x0FF==ord('q'):
		break
video.release()
cv2.destroyAllWindows()
