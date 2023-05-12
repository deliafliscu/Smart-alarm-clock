"""
Objects and face detection on images

Installation:
go to https://pytorch.org/get-started/locally/ and select the options suitable for installing pytorch in your computer then copy the command and run it.
type:
git clone https://github.com/ultralytics/yolov5  #for cloning yolov5
cd yolov5
pip install -r requirements.txt  # installing dependencies
"""

from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.pickers import MDTimePicker
from kivy.clock import Clock
import datetime
import pygame
import speech_recognition as sr
import pyttsx3
import random
import torch

Window.size = (350, 600)


class ImageDetection:

    def __init__(self, image):
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path='final.pt', force_reload=True)
        self.results = self.model(image)

    def checking(self):
        if self.results.pandas().xyxy[0].value_counts('name').empty:
            return False
        return True

    def re(self):
        return ImageDetection("selfie.png").checking()


class Alarm(MDApp):
    # x = True
    #
    # def truth(self):
    #     x = False
    #     return x

    def det(self):
        print("I am here")
        detection = ImageDetection("selfie.png")
        print(detection.re())
        if detection.checking():
            self.root.current = "voice_screen"


    pygame.init()
    sound = pygame.mixer.Sound("alarm.mp3")
    volume = 0

    def time_picker(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.get_time, on_save=self.schedule)
        time_dialog.open()

    def get_time(self, instance, time):
        self.root.ids.alarm_time.text = str(time)

    def schedule(self, *args):
        Clock.schedule_once(self.alarm, 1)

    def alarm(self, *args):
        while True:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            if self.root.ids.alarm_time.text == str(current_time):
                self.start()
                self.root.current = "camera_screen"
                break

    def set_volume(self, *args):
        self.volume += 0.05
        if self.volume < 0.5:
            Clock.schedule_interval(self.set_volume, 10)
            self.sound.set_volume(self.volume)
            print(self.volume)
        else:
            self.sound.set_volume(0.5)
            print("Reached max volume")

    def start(self, *args):
        self.sound.play(-1)
        self.set_volume()

    def stop(self):
        self.sound.stop()
        Clock.unschedule(self.set_volume)
        self.volume = 0

    def change_screen(self):
        self.root.current = "camera_screen"

    def change_screen_2(self):
        self.root.current = "voice_screen"

    def listen(self):
        # the code will read the lines from the saved text file
        lines = []
        dispfile = open("lines.txt", "r")
        content = dispfile.read()
        content = content.split("\n")
        dispfile.close()
        for i in content:
            lines.append(i)

        # A random line is chosen from the text file
        random_line = random.choice(lines)
        print(random_line)
        mytext = random_line
        mytext2 = str(mytext)

        # the function to say the line aloud by the program
        # def SpeakText(self):
        #     engine = pyttsx3.init()
        #     engine.say(self)
        #     engine.runAndWait()
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source2:
                engine = pyttsx3.init()
                engine.say("Repeat the following sentence, " + mytext2)
                engine.runAndWait()
                # self.SpeakText(mytext2)  # SpeakText is used to make the program say whatever we want

                # while True:
                print("Say it now")

                # the code to ask the user to say the sentence
                r.adjust_for_ambient_noise(source2, duration=0.9)
                audio2 = r.listen(source2)
                Myvoice = r.recognize_google(audio2)
                Myvoice = Myvoice.lower()
                print(Myvoice)

                # checking whether the sentence matches what the user said
                if (Myvoice == mytext2):
                    engine = pyttsx3.init()
                    engine.say("it is correct")
                    engine.runAndWait()
                    self.stop()
                    self.root.current = "alarm_screen"
                    # self.SpeakText("it is correct")
                    # break  # the code stops when the sentence matches
                else:
                    engine = pyttsx3.init()
                    engine.say("it is wrong")
                    engine.runAndWait()
                    # self.SpeakText(
                    #     "it is wrong. try again")  # the code repeats and the user tries again if the sentence does not match

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("unknown error occurred")

    def build(self):
        return Builder.load_string('''
ScreenManager:
    id: screen_manager
    AlarmScreen:
        name: 'alarm_screen'
        id: alarm_screen
        MDFloatLayout:
            md_bg_color: 1, 1, 1, 1
            Image:
                source: 'Fonts/wallpaper2.png'
                pos_hint: {"center_x": .50, "center_y": .565}
            MDIconButton:
                icon: "plus"
                pos_hint: {"center_x": .50, "center_y": .30}
                md_bg_color: 0, 0, 0, 1
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                on_release: app.time_picker()  
            MDLabel:
                id: alarm_time
                text: ""
                pos_hint: {"center_y": .7}
                halign: "center"
                font_size: "30sp"
                bold: True
    CameraScreen:
        name: 'camera_screen'
        id: camera_screen
        MDFloatLayout:
        Camera:
            id: camera
            resolution: (640, 640)
            play: True
        MDIconButton:
            icon: "camera"
            pos_hint: {"center_x": .50, "center_y": .05}
            md_bg_color: 0, 0, 0, 1
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            on_press:
                camera.export_to_png('selfie.png')
                app.det()
    OptionScreen:
        name: 'option_screen'
        id: option_screen
        MDFloatLayout:
            md_bg_color: 1, 1, 1, 1
            Image:
                source: 'Fonts/secondscreenwallpaper2.png'
                pos_hint: {"center_x": .50, "center_y": .565}
            
            MDIconButton:
                icon: "camera"
                pos_hint: {"center_x": .50, "center_y": .15}
                md_bg_color: 0, 0, 0, 1
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                on_press: 
                    app.change_screen()
            
    VoiceScreen:
        name: 'voice_screen'
        id: 'voice_screen'
        MDFloatLayout:
            md_bg_color: 1, 1, 1, 1
            Image:
                source: 'Fonts/voicebg.png'
                pos_hint: {"center_x": .50, "center_y": .565}
            MDIconButton:
                icon: "speak"
                pos_hint: {"center_x": .50, "center_y": .15}
                md_bg_color: 0, 0, 0, 1
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                on_press: 
                    app.listen()


        
'''

                                   )


class AlarmScreen(Screen):
    pass


class CameraScreen(Screen):
    pass


class OptionScreen(Screen):
    pass


class VoiceScreen(Screen):
    pass


# sm = ScreenManager()
# sm.add_widget(AlarmScreen(name='alarmscreen'))
# sm.add_widget(CameraScreen(name='camerascreen'))
# sm.add_widget(OptionScreen(name='option_screen'))

Alarm().run()
