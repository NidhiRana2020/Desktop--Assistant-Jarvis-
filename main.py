import pyttsx3
import speech_recognition as sr
import random
import webbrowser
import datetime
from plyer import notification
import pyautogui
import wikipedia
from wikipedia.exceptions import DisambiguationError
import pywhatkit as pwk
import user_config
import smtplib, ssl
from email.message import EmailMessage
import openai_request as ai
import image_generation
import mtranslate

# print(user_config.gmail_password)

engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 170)


def speak(audio):
    audio = mtranslate.translate(audio, to_language="hi", from_language="en-in")
    print(audio)
    engine.say(audio)
    engine.runAndWait()


def command():
    content = " "
    while content == " ":
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say Something!")
            audio = r.listen(source)

        try:
            content = r.recognize_google(audio, language="en-in")
            print("you said....." + content)
            content = mtranslate.translate(content, to_language="en-in")
            print("you said....." + content)
        except Exception as e:
            print("please try again...")

    return content


def main_process():
    jarvis_chat = []
    while True:
        request = command().lower()
        if "hello" in request:
            speak("Welcome, How can i help you.")
        elif "play music" in request:
            speak("playing Music")
            song = random.randint(1, 5)
            if song == 1:
                webbrowser.open(
                    "https://www.youtube.com/watch?v=mzoxRKF447M&list=PLRBp0Fe2GpgnIh0AiYKh7o7HnYAej-5ph&index=1&pp=iAQB"
                )
            elif song == 2:
                webbrowser.open(
                    "https://www.youtube.com/watch?v=iAgoObHN3T8&list=PLRBp0Fe2GpgnIh0AiYKh7o7HnYAej-5ph&index=2&pp=iAQB"
                )
            elif song == 3:
                webbrowser.open(
                    "https://www.youtube.com/watch?v=8k-KhejOoSc&list=PLRBp0Fe2GpgnIh0AiYKh7o7HnYAej-5ph&index=5&pp=iAQB"
                )
            elif song == 4:
                webbrowser.open(
                    "https://www.youtube.com/watch?v=PIYHgVDsYGA&list=PLRBp0Fe2GpgnIh0AiYKh7o7HnYAej-5ph&index=11&pp=iAQB0gcJCYYJAYcqIYzv"
                )
            elif song == 5:
                webbrowser.open(
                    "https://www.youtube.com/watch?v=a7P0UO8TANk&list=PLRBp0Fe2GpgnIh0AiYKh7o7HnYAej-5ph&index=12&pp=iAQB"
                )

        elif "say time" in request:
            now_time = datetime.datetime.now().strftime("%H:%M")
            speak("Current time is " + str(now_time))
        elif "say date" in request:
            now_time = datetime.datetime.now().strftime("%d:%m")
            speak("Current date is " + str(now_time))

        elif "new task" in request:
            task = request.replace("new task", "")
            task = task.strip()
            if task != "":
                speak("adding task : " + task)
                with open("todo.txt", "a") as file:
                    file.write(task + "\n")

        elif "speak task" in request:
            with open("todo.txt", "r") as file:
                speak("Work we have to do today is : " + file.read())
        elif "show work" in request:
            with open("todo.txt", "r") as file:
                tasks = file.read()
            notification.notify(title="Today's work", message=tasks)
        elif "open Youtube" in request:
            webbrowser.open("www.youtube.com")

        elif "open" in request:
            query = request.replace("open", "")
            pyautogui.press("super")
            pyautogui.typewrite(query)
            pyautogui.sleep(2)
            pyautogui.press("enter")

        # elif "wikipedia" in request:
        #     request= request.replace("jarvis", "")
        #     request= request.replace("search wikipedia ", "")
        #     print(request)
        #     result=wikipedia.summary("request", sentences=2)
        #     print(result)
        #     speak(result)
        elif "search in wikipedia about" in request:
            query = request.replace("search in wikipedia about", "").strip()
            if query:
                try:
                    result = wikipedia.summary(query, sentences=2)
                    print(result)
                    speak(result)
                except wikipedia.exceptions.DisambiguationError as e:
                    print("Too many topics found. Please be more specific.")
                    speak("Too many topics found. Please be more specific.")
                    print("Some options are:", e.options[:5])
                except wikipedia.exceptions.PageError:
                    print("No matching page found on Wikipedia.")
                    speak("No matching page found.")
            else:
                print("I didn't catch the topic. Please try again.")
                speak("I didn't catch the topic. Please try again.")

        elif "search wikipedia about" in request:
            query = request.replace("search wikipedia about", "").strip()
            if query:
                try:
                    result = wikipedia.summary(query, sentences=2)
                    print(result)
                    speak(result)
                except wikipedia.exceptions.DisambiguationError as e:
                    print("Too many topics found. Please be more specific.")
                    speak("Too many topics found. Please be more specific.")
                except wikipedia.exceptions.PageError:
                    print("No matching page found on Wikipedia.")
                    speak("No matching page found.")
            else:
                print("Please say what to search.")
                speak("Please say what to search.")

        elif "search google" in request:
            request = request.replace("jarvis", "")
            request = request.replace("search google ", "")
            webbrowser.open("https://www.google.com/search?q=" + request)

        elif "send whatsapp" in request:
            pwk.sendwhatmsg("+918603678500", "Hi.how are you", 9, 13, 30)

        # elif "send email" in request:
        #     pwk.send_mail(
        #         "nidhirana2020@gmail.com",
        #         user_config.gmail_password,
        #         "Hello" "Hi.how are you",
        #         "smita40321@gmail.com",
        #     )
        #     speak("Email sent")
        elif "send email" in request:
            s = smtplib.SMTP("smtp.gmail.com", 587)
            s.starttls()
            s.login("nidhirana2020@gmail.com", user_config.gmail_password)
            message = """this is the message ."""
            s.sendmail("nidhirana2020@gmail.com" "smita40321@gmail.com", message)
            s.quit()
            speak("Email sent")
        # elif "image" in request:
        #     request = request.replace("jarvis", "")
        #     image_generation.generate_image(request)
        elif "ask ai" in request:
            jarvis_chat = []
            request = request.replace("jarvis", "")
            request = request.replace("ask ai", "")
            jarvis_chat.append({"role": "user", "content": request})
            response = ai.send_request(jarvis_chat)
            speak(response)

        elif "clear chat" in request:
            jarvis_chat = []
            speak("chat cleared")
        else:
            request = request.replace("jarvis", "")

            jarvis_chat.append({"role": "user", "content": request})
            response = ai.send_request(jarvis_chat)

            jarvis_chat.append({"role": "user", "content": request})
            speak(response)


if __name__ == "__main__":
    main_process()