import pyttsx3
import datetime
import speech_recognition as sr
import pyaudio
import wikipedia
import webbrowser
import os
import pygame
import math
import random
import threading
import sys

# KIRA: Knowledgeful Interactive Resourceful Assistant
# made by Aman Kr Singh
# Initialize the speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)    

    if hour >= 0 and hour < 12:
        speak("Good Morning")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon")

    else:
        speak("Good Evening")

    speak("I am KIRA, How can I help you?")

thresh = 0  
def takeCommand():
    global thresh
    if thresh >= 6:
        # print("Threshold reached. Exiting program.")
        speak("Terminating programme")
        pygame.quit()
        sys.exit()

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print("Please say that again..")
        thresh += 1 
        # print(f"thresh is: {thresh}")
        return "None"
    
    
    return query



# code for the visuals
def run_visual():
    pygame.init()
    width, height = 300, 300
    # works best at values 450 ,450
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('KIRA Sphere')

    clock = pygame.time.Clock()
    running = True

    num_points = 1000  # Number of points in the sphere
    sphere_radius = 125  # Radius of the sphere
    point_radius = 1.5  # Radius of each point
    background_color = (0, 0, 0)  # Background color
    center = (width // 2, height // 2)

    # Rotation parameters
    rotation_speed = 0.02
    angle_x = 0
    angle_y = 0

    # Distortion parameters
    distortion_factor = 3 # Intensity of distortion

    def project_3d_to_2d(x, y, z):
        scale = 500 / (500 + z)  # Perspective scale factor
        x2 = center[0] + x * scale
        y2 = center[1] - y * scale
        return int(x2), int(y2)

    def generate_sphere_points(num_points, radius):
        points = []
        for _ in range(num_points):
            theta = random.uniform(0, 2 * math.pi)
            phi = random.uniform(0, math.pi)
            x = radius * math.sin(phi) * math.cos(theta)
            y = radius * math.sin(phi) * math.sin(theta)
            z = radius * math.cos(phi)
            points.append([x, y, z])
        return points

    def rotate_point(x, y, z, angle_x, angle_y):
        x1 = x
        y1 = y * math.cos(angle_x) - z * math.sin(angle_x)
        z1 = y * math.sin(angle_x) + z * math.cos(angle_x)

        x2 = x1 * math.cos(angle_y) + z1 * math.sin(angle_y)
        y2 = y1
        z2 = -x1 * math.sin(angle_y) + z1 * math.cos(angle_y)

        return x2, y2, z2

    def apply_distortion(x, y, z, distortion_factor):
        distortion = math.sin(x * 0.1) * distortion_factor
        x_distorted = x + distortion
        y_distorted = y + distortion
        z_distorted = z + distortion
        return x_distorted, y_distorted, z_distorted

    def calculate_fading_color(distance, max_distance):
        fade_factor = max(0, 255 - int(255 * (distance / max_distance)))
        return (255, 255, 255, fade_factor)

    sphere_points = generate_sphere_points(num_points, sphere_radius)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        angle_x += rotation_speed
        angle_y += rotation_speed

        screen.fill(background_color)

        for (x, y, z) in sphere_points:
            x_rot, y_rot, z_rot = rotate_point(x, y, z, angle_x, angle_y)
            x_distorted, y_distorted, z_distorted = apply_distortion(x_rot, y_rot, z_rot, distortion_factor)
            x2, y2 = project_3d_to_2d(x_distorted, y_distorted, z_distorted)
            distance = math.sqrt(x_distorted**2 + y_distorted**2 + z_distorted**2)
            color = calculate_fading_color(distance, sphere_radius)
            pygame.draw.circle(screen, color, (x2, y2), point_radius)

        pygame.display.flip()
        clock.tick(20)  # 30 frames per second

    # pygame.quit()

   

  
if __name__ == "__main__":
    wishMe()

    # Run the video in a separate thread
    visual_thread = threading.Thread(target=run_visual)
    visual_thread.start()


    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
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
            speak(f"Sir, the time is {strTime}")

        elif 'open code' in query:
            codePath = "C:\\Users\\amans\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            if os.path.exists(codePath):
                os.startfile(codePath)
                speak("Opening Visual Studio Code")
            else:
                speak("Visual Studio Code is not installed on this system.")
 

        elif 'kira stop' in query or 'stop kira' in query or 'stop' in query:
            speak("Terminating programme")
            # pygame.quit()
          # Close the pygame window
            sys.exit()

    
    '''    elif 'remind me' in query:
            reminder = query.replace("remind me to", "").strip()
            set_reminder(reminder)  
            # Implement set_reminder function to handle reminders
            speak(f"Reminder set to: {reminder}")
    '''

    '''
     elif 'what is the weather' in query:
            city = query.replace("what is the weather in", "").strip()
            weather_info = get_weather_info(city)  # Implement get_weather_info function with an API call
            speak(f"The weather in {city} is {weather_info}")

    '''