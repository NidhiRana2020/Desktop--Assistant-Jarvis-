import smtplib
import pyttsx3
import pyjokes
import pyautogui
import re
import random
import pprint
import datetime
import requests
import wikipedia
import urllib.parse
import pywhatkit
import wolframalpha
from PIL import Image
import time
from Jarvis import JarvisAssistant
from Jarvis.config import config
from desktopUi import Ui_MainWindow
from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import QMovie
from PyQt5.QtGui import*
from PyQt5.QtWidgets import*
from PyQt5.QtCore import Qt,QTimer,QTime,QDate
from PyQt5.uic import loadUiType
import desktopAssistant
import os
import webbrowser as web
import sys

class MainThread(QThread):...
obj = JarvisAssistant()

# ================================ MEMORY ===========================================================================================================

GREETINGS = ["hello Manic", "Manic", "wake up Manic", "you there Manic", "time to work Manic", "hey Manic",
             "ok Manic", "are you there"]
GREETINGS_RES = ["always there for you sir", "i am ready sir",
                 "your wish my command", "how can i help you sir?", "i am online and ready sir"]

EMAIL_DIC = {
    'myself': 'nidhirana2020@gmail.com',
    'my official email': 'rananidhi20000@gmail.com',
    'my second email': 'snow64722@gmail.com',

}

CALENDAR_STRS = ["what do i have", "do i have plans", "am i busy"]
# =======================================================================================================================================================


def speak(text):
    obj.tts(text)


app_id = config.wolframalpha_id


def computational_intelligence(question):
    try:
        client = wolframalpha.Client(app_id)
        answer = client.query(question)
        answer = next(answer.results).text
        print(answer)
        return answer
    except:
        speak("Sorry Mam I couldn't fetch your question's answer. Please try again ")
        return None
    
def startup():
    speak("Initializing Manic")
    speak("Starting all systems applications")
    speak("Installing and checking all drivers")
    speak("Caliberating and examining all the core processors")
    speak("Checking the internet connection")
    speak("Wait a moment Mam")
    speak("All drivers are up and running")
    speak("All systems have been activated")
    speak("Now I am online")
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<=12:
        speak("Good Morning")
    elif hour>12 and hour<18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    c_time = obj.tell_time()
    speak(f"Currently it is {c_time}")
    speak("I am Manic. Online and ready mam. Please tell me how may I help you")
    



def wish():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<=12:
        speak("Good Morning")
    elif hour>12 and hour<18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    c_time = obj.tell_time()
    speak(f"Currently it is {c_time}")
    speak("I am Manic. Online and ready sir. Please tell me how may I help you")
# if __name__ == "__main__":


class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.TaskExecution()

    def TaskExecution(self):
        startup()
        wish()

        while True:
            command = obj.mic_input()

            if re.search('date', command):
                date = obj.tell_me_date()
                print(date)
                speak(date)

            elif "time" in command:
                time_c = obj.tell_time()
                print(time_c)
                speak(f"Sir the time is {time_c}")

            elif re.search('launch', command):
                dict_app = {
                    'chrome': 'C:/Program Files/Google/Chrome/Application/chrome'
                }

                app = command.split(' ', 1)[1]
                path = dict_app.get(app)

                if path is None:
                    speak('Application path not found')
                    print('Application path not found')

                else:
                    speak('Launching: ' + app + 'for you sir!')
                    obj.launch_any_app(path_of_app=path)

            elif command in GREETINGS:
                speak(random.choice(GREETINGS_RES))

            elif re.search('open', command):
                domain = command.split(' ')[-1]
                open_result = obj.website_opener(domain)
                speak(f'Alright sir !! Opening {domain}')
                print(open_result)

            elif re.search('weather', command):
                city = command.split(' ')[-1]
                weather_res = obj.weather(city=city)
                print(weather_res)
                speak(weather_res)

            elif re.search('tell me about', command):
                topic = command.split(' ')[-1]
                if topic:
                    wiki_res = obj.tell_me(topic)
                    print(wiki_res)
                    speak(wiki_res)
                else:
                    speak(
                        "Sorry mam. I couldn't load your query from my database. Please try again")

            elif "buzzing" in command or "news" in command or "headlines" in command:
                news_res = obj.news()
                speak('Source: The Times Of India')
                speak('Todays Headlines are..')
                for index, articles in enumerate(news_res):
                    pprint.pprint(articles['title'])
                    speak(articles['title'])
                    if index == len(news_res)-2:
                        break
                speak('These were the top headlines, Have a nice day Sir!!..')

            elif 'search google for' in command:
                obj.search_anything_google(command)
            
            elif "play music" in command or "hit some music" in command:
                music_dir = ("C:\\Users\\admin\\Music\\Playlists")
                songs = os.listdir(music_dir)
                for song in songs:
                    os.startfile(os.path.join(music_dir, song))

            elif 'youtube' in command:
                video = command.split(' ')[1]
                speak(f"Okay sir, playing {video} on youtube")
                pywhatkit.playonyt(video)

            elif "email" in command or "send email" in command:
                sender_email = config.email
                sender_password = config.email_password

                try:
                    speak("Whom do you want to email mam ?")
                    recipient = obj.mic_input()
                    receiver_email = EMAIL_DIC.get(recipient)
                    if receiver_email:

                        speak("What is the subject mam ?")
                        subject = obj.mic_input()
                        speak("What should I say?")
                        message = obj.mic_input()
                        msg = 'Subject: {}\n\n{}'.format(subject, message)
                        obj.send_mail(sender_email, sender_password,
                                      receiver_email, msg)
                        speak("Email has been successfully sent")
                        time.sleep(2)

                    else:
                        speak(
                            "I coudn't find the requested person's email in my database. Please try again with a different name")

                except:
                    speak("Sorry mam. Couldn't send your mail. Please try again")

            elif "calculate" in command:
                question = command
                answer = computational_intelligence(question)
                speak(answer)

            
            elif "what is" in command or "who is" in command:
                question = command
                answer = computational_intelligence(question)
                speak(answer)

            elif "what do i have" in command or "do i have plans" or "am i busy" in command:
                obj.google_calendar_events(command)

            if "make a note" in command or "write this down" in command or "remember this" in command:
                speak("What would you like me to write down?")
                note_text = obj.mic_input()
                obj.take_note(note_text)
                speak("I've made a note of that")

            elif "close the note" in command or "close notepad" in command:
                speak("Okay mam, closing notepad")
                os.system("taskkill /f /im notepad++.exe")

            if "joke" in command:
                joke = pyjokes.get_joke()
                print(joke)
                speak(joke)

            elif "system" in command:
                sys_info = obj.system_info()
                print(sys_info)
                speak(sys_info)

            elif "where is" in command:
                place = command.split('where is ', 1)[1]
                current_loc, target_loc, distance = obj.location(place)
                city = target_loc.get('city', '')
                state = target_loc.get('state', '')
                country = target_loc.get('country', '')
                time.sleep(1)
                try:

                    if city:
                        res = f"{place} is in {state} state and country {country}. It is {distance} km away from your current location"
                        print(res)
                        speak(res)

                    else:
                        res = f"{state} is a state in {country}. It is {distance} km away from your current location"
                        print(res)
                        speak(res)

                except:
                    res = "Sorry mam, I couldn't get the co-ordinates of the location you requested. Please try again"
                    speak(res)

            elif "ip address" in command:
                ip = requests.get('https://api.ipify.org').text
                print(ip)
                speak(f"Your ip address is {ip}")

            elif "switch the window" in command or "switch window" in command:
                speak("Okay sir, Switching the window")
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.keyUp("alt")

            elif "where i am" in command or "current location" in command or "where am i" in command:
                try:
                    city, state, country = obj.my_location()
                    print(city, state, country)
                    speak(
                        f"You are currently in {city} city which is in {state} state and country {country}")
                except Exception as e:
                    speak(
                        "Sorry mam, I coundn't fetch your current location. Please try again")

            elif "take screenshot" in command or "take a screenshot" in command or "capture the screen" in command:
                speak("By what name do you want to save the screenshot?")
                name = obj.mic_input()
                speak("Alright mam, taking the screenshot")
                img = pyautogui.screenshot()
                name = f"{name}.png"
                img.save(name)
                speak("The screenshot has been succesfully captured")

            elif "show me the screenshot" in command:
                try:
                    img = Image.open('D://JARVIS//JARVIS_2.0//' + name)
                    img.show(img)
                    speak("Here it is mam")
                    time.sleep(2)

                except IOError:
                    speak("Sorry mam, I am unable to display the screenshot")

            elif "hide all files" in command or "hide this folder" in command:
                os.system("attrib +h /s /d")
                speak("Mam, all the files in this folder are now hidden")

            elif "visible" in command or "make files visible" in command:
                os.system("attrib -h /s /d")
                speak("Mam, all the files in this folder are now visible to everyone. I hope you are taking this decision in your own peace")

            # if "calculate" in command or "what is" in command:
            #     query = command
            #     answer = computational_intelligence(query)
            #     speak(answer)

            

            elif "goodbye" in command or "offline" in command or "bye" in command:
                speak("Alright mam, going offline. It was nice working with you")
                sys.exit()

startExe =MainThread()

class Gui_start(QMainWindow):

    def __init__(self):

        super().__init__()

        self.gui=Ui_MainWindow()
        self.gui.setupUi(self)

        self.gui.pushButton_Start.clicked.connect(self.startTask)
        self.gui.pushButton_Exit.clicked.connect(self.close)
        self.gui.pushButton_Youtube.clicked.connect(self.Youtube_app)
        self.gui.pushButton_Chrome.clicked.connect(self.Chrome_app)
        self.gui.pushButton_Whatsapp.clicked.connect(self.Whatsapp_app)
        self.gui.pushButton_Google.clicked.connect(self.Google_app)
        self.gui.pushButton_VSCode.clicked.connect(self.VSCode_app)
        self.gui.pushButton_Temperature.clicked.connect(self.Temperature_app)
        
    def Youtube_app(self):
        desktopAssistant.speak("opening Youtube...")
        web.open("https://www.youtube.com/")    


    def Chrome_app(self):
        desktopAssistant.speak("opening Chrome...")
        os.startfile("C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")

    def Whatsapp_app(self):
        desktopAssistant.speak("opening Whatsapp...")
        web.open("C:\ProgramData\admin\WhatsApp\WhatsApp.exe")

    def Google_app(self):
        desktopAssistant.speak("opening Google...")
        web.open("https//web.Google.com")


    def VSCode_app(self):
        web.open("VSCode App")


    def Temperature_app(self):
        web.open("https//web.temperature.com")

    def Task_Gui(self):
        os.startfile("desktop.py")

    def startTask(self):
      
        self.gui.Bg_1=QtGui.QMovie("../project images/girl assistant.gif")
        self.gui.gif_2.setMovie(self.gui.Bg_1)
        self.gui.Bg_1.start()


        self.gui.Bg_3=QtGui.QMovie("../project images/200.gif")
        self.gui.gif_3.setMovie(self.gui.Bg_3)
        self.gui.Bg_3.start()

        self.gui.bg_4=QtGui.QMovie("project images//audio.gif")
        self.gui.gif_4.setMovie(self.gui.bg_4)
        self.gui.bg_4.start()

        self.gui.bg_5=QtGui.QMovie("../project images/giphy.gif")
        self.gui.gif_1.setMovie(self.gui.bg_5)
        self.gui.bg_5.start()

        self.gui.bg_6=QtGui.QMovie("../project images/initial.gif")
        self.gui.gif_5.setMovie(self.gui.bg_6)
        self.gui.bg_6.start()

        timer =QTimer(self)
        timer.timeout.connect(self.showTimeLive)
        timer.start(999)
        startExe.start()

        startExe.start()

    def showTimeLive(self):
        t_ime=QTime.currentTime()
        time =t_ime.toString()
        D_ate=QDate.currentDate()
        date=D_ate.toString()
        d_ay=QDateTime.currentDateTime()
        day=d_ay.toString()
        Lable_day="Day:"+day
        Lable_time="Time:" +time
        lable_date ="Date:" +date

        self.gui.Text_day.setText(Lable_day)
        self.gui.Text_time.setText(Lable_time)
        self.gui.Text_date.setText(lable_date)


Gui_App =QApplication(sys.argv)
Gui_desktop = Gui_start()
Gui_desktop.show()
exit(Gui_App.exec_())



