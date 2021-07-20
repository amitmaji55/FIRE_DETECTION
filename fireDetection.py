import cv2         # Library for openCV
import threading   # Library for threading -- which allows code to run in backend
import playsound   # Library for alarm sound
import smtplib     # Library for email sending

fire_cascade = cv2.CascadeClassifier('fire_detection_cascade_model.xml') # To access xml file which includes positive and negative images of fire. (Trained images)
                                                                         # File is also provided with the code.

vid = cv2.VideoCapture(0) # To start camera this command is used "0" for laptop inbuilt camera and "1" for USB attahed camera for pc
runOnce = False # created boolean

def play_alarm_sound_function(): # defined function to play alarm post fire detection using threading
    playsound.playsound('Alarm Sound.mp3',True) # to play alarm # mp3 audio file is also provided with the code.
    print("Fire alarm end") # to print in console

def send_mail_function(): # defined function to send mail post fire detection using threading
    
    recipientmail = "anirudhamaji67@gmail.com" # recipients mail
    recipientmail = recipientmail.lower() # To lower case mail
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("anirudhamaji67@gmail.com", 'SPEEDISGOOD1') # Senders mail ID and password
        server.sendmail('anirudhamaji2001@gmail.com', recipientmail, "Warning fire accident has been reported") # recipients mail with mail message
        print("Alert mail sent sucesfully to {}".format(recipientmail)) # to print in consol to whome mail is sent
        server.close() ## To close server
        
    except Exception as e:
        print(e) # To print error if any
		
while(True):
    Alarm_Status = False
    ret, frame = vid.read() # Value in ret is True # To read video frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # To convert frame into gray color
    fire = fire_cascade.detectMultiScale(frame, 1.2, 5) # to provide frame resolution

    ## to highlight fire with square 
    for (x,y,w,h) in fire:
        cv2.rectangle(frame,(x-20,y-20),(x+w+20,y+h+20),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        print("Fire alarm initiated")
        threading.Thread(target=play_alarm_sound_function).start()  # To call alarm thread

        if runOnce == False:
            print("Mail send initiated")
            threading.Thread(target=send_mail_function).start() # To call alarm thread
            runOnce = True
        if runOnce == True:
            print("Mail is already sent once")
            runOnce = True

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
