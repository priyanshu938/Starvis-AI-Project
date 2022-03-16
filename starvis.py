# libraries used : text to speech,datetime,speechRecognition,wikipedia,webbrowser,os,random,smtplib,sys,pywhatkit,getpass,cv2
import time
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import random
import smtplib
import sys
import pywhatkit
import getpass
import cv2

# setting up engines and voices
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices) : this line will print installed voices in your system as a list
# voices[0] is for 'david' and voices[1] is for 'zira' according to my system
engine.setProperty('voice', voices[0].id)

# speak function will speak the audio passed


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# wish command wishes the user


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Starvis Sir. Please tell me how may I help you.")

# take command function to take microphone input from the user and return string output


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1  # sets a pause of 1 second
        audio = r.listen(source)
    try:
        print("Recognising.....")
        # use google engine to recognise voice from microphone
        # query = r.recognize_google(audio, language=code) => provide language code from here -: https://cloud.google.com/speech-to-text/docs/languages
        # I have used English India ,you can choose as per your choice
        query = r.recognize_google(audio, language="en-IN").lower()
        print(f"User said : {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query


# Note : Keep the keys in the following dictionaries all in lower cases
# dictionary to store mail contacts
mailContacts = {
    "priyanshu": "priyanshutiwari6789@gmail.com",
    "tiwari": "tiwaripriyanshu1234@gmail.com",
    "vinita": "vineetat359@gmail.com"
}
# dictionary to store whats app contacts
whatsAppContacts = {
    "ankit": "+916307066590",
    "sachin": "+917393811098",
    "venkatesh": "+919115245454"
}

# to send email


def send_email(to, content):

    # ask sender's email address
    speak("Enter your gmail id ")
    sender = input("Enter your gmail id :")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # tls(transport layer security)for security purpose
    speak("Enter your gmail id password")
    # getpass function to hide the password on the terminal
    password = getpass.getpass("Enter your gmail id password : ")
    # server.login(username, password) write yor mail id and password below
    server.login(sender, password)
    server.sendmail(sender, to, content)
    server.quit()


wishMe()
while True:
    query = take_command()

    if "wikipedia" in query:
        speak("Searching wikipedia...")
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=1)
        speak("According to wikipedia")
        print(results)
        speak(results)

    elif "open youtube" in query:
        print("Opening youtube....")
        speak("Opening youtube....")
        # webbrowser module will open the browser and particular site
        webbrowser.open("youtube.com")

    elif "open google" in query:
        print("Opening google....")
        speak("Opening google....")
        webbrowser.open("google.com")

    elif "open stackoverflow" in query:
        print("Opening stackoverflow....")
        speak("Opening stackoverflow....")
        webbrowser.open("stackoverflow.com")

    elif "play music" in query:
        # provide any directory path with double slash coz of escape sequence
        music_dir = "C:\\Users\\91951\\Desktop\\songs"
        songs = os.listdir(music_dir)  # lists all files in this directory
        # will play a random song from that directory
        # here I have 10 songs in my directory so I have used range 0 to 9
        randomSong = random.randrange(0, 9)
        os.startfile(os.path.join(music_dir, songs[randomSong]))

    elif "the time" in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Sir, the time is {strTime}")

    elif "open vs code" in query:
        # provide path of the application to os module to open any application from your desktop
        path = "C:\\Users\\91951\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        os.startfile(path)

    elif "send email" in query:
        try:
            while True:
                speak("To whom you wish to send email ?")
                to = take_command()  # provide recievers mail
                if to in mailContacts:
                    to = mailContacts[to]
                    break
                else:
                    print("Sorry,contact doesn't exist!")
                    speak("Sorry,contact doesn't exist!")
            speak("What should I message in mail ?")
            content = take_command()
            send_email(to, content)
            speak("Email has been sent!")
        except Exception as e:
            speak("Sorry , Failed to send email!")

    elif "send whatsapp message" in query:
        try:
            to = ""
            while True:
                speak("To whom you wish to send message ?")
                to = take_command()  # provide recievers mail
                if to in whatsAppContacts:
                    to = whatsAppContacts[to]
                    break
                else:
                    print("Sorry,contact doesn't exist!")
                    speak("Sorry,contact doesn't exist!")
            speak("What should I message ?")
            message = take_command()
            # pywhatkit.sendwhatmsg_instantly("phone number on which to send number with country code", message)
            pywhatkit.sendwhatmsg_instantly(to, message)
            speak("Successfully Sent!")
        except Exception as e:
            speak("Sorry , Failed to send message!")

    elif "search google" in query:
        try:
            speak("What should I search ?")
            content = take_command()
            pywhatkit.search(content)
        except Exception as e:
            speak("Sorry , Failed to search!")

    elif "search topic" in query:
        try:
            speak("What should I search ?")
            content = take_command()
            # pywhatkit.info(content, lines=n) : provide n as number of lines you want to fetch
            pywhatkit.info(content, lines=2)
        except Exception as e:
            speak("Sorry , Failed to search!")

    elif "open team" in query:
        path = "C:\\Users\\91951\\AppData\\Local\\Microsoft\\Teams\\current\\Teams.exe"
        try:
            os.startfile(path)
        except Exception as e:
            print(e)

    elif "photo" in query:
        cam_port = 0
        cam = cv2.VideoCapture(cam_port)
        # reading the input using the camera
        result, image = cam.read()
        # If image will detected without any error, show resu
        if result:

            # showing result, it take frame name and image
            # output
            cv2.imshow("Photo", image)
            time.sleep(0.1)  # If you don't wait, the image will be dark
            # If keyboard interrupt occurs, destroy image window
            cv2.waitKey(0)
            cv2.destroyWindow("Photo")

            # saving image
            img = input("Write file name to save image :")
            cv2.imwrite(img+".png", image)
        else:
            print("No image detected. Please! try again")

    elif "bye" in query:
        speak("Ok sir, have a good day!")
        sys.exit(0)
