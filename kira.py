import pyttsx3
import datetime
import speech_recognition as sr
import pyaudio
import wikipedia
import webbrowser
import os

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice' , voices[1].id)
# print(voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)    

    if hour >= 0 and hour <12:
        speak("Good Morning")

    elif hour>=12 and hour < 18:
        speak("Good Afternoon")

    else:
        speak("Good Evening")

    speak("I am Kira, How can i help you ?")


def takeCommand():
    # it takes microphone input and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language = 'en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)
        print("Please say that again..")
        return "None"
    return query




if __name__ == "__main__":
    wishMe()

    while True:
        query = takeCommand().lower()
         # logic for executing tasks based on query 

        if 'wikipedia' in query:
            speak('Searching Wikipedia')
            query = query.replace("wikipedia" , "")
            results = wikipedia.summary(query,sentences=2)
            speak("According to wikipedia")
            print(results)
            speak(results)


        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open gmail' in query:
            webbrowser.open("gmail.com")

        elif 'open linkedin' in query:
            webbrowser.open("linkedin.com")

        elif 'play music' in query:
            webbrowser.open("https://music.youtube.com/watch?v=ulZQTrV8QlQ&list=PL0Z9ll4kWTuaoxSnMHW-u0ZIZyOog3bsi")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir , the time is {strTime}")

        elif 'open code' in query:
            codePath = "C:\\Users\\amans\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)
            
        elif 'kira stop' in query:
            speak("Terminating programme")
            exit()

         


        
        



