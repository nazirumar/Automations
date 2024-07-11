import pyautogui
import time
import psutil
import pygetwindow as gw
import speech_recognition as sr
import pyttsx3


class WhatsAppAutomation:
    """
    Class to automate WhatsApp messaging.
    """
    
    def __init__(self, messages=None):
        self.messages = messages
        self.username = None
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()

    def speak_text(self, text):
        """
        Convert text to speech using pyttsx3.
        """
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)
        self.engine.say(text)
        self.engine.runAndWait()

    def bring_whatsapp_to_foreground(self):
        """
        Bring the WhatsApp window to the foreground.
        """
        windows = gw.getWindowsWithTitle('WhatsApp')
        if windows:
            print(f'Bringing {windows[0].title} to the foreground.')
            windows[0].activate()
        else:
            print('WhatsApp window not found.')
            self.speak_text('WhatsApp window not found.')

    def open_whatsapp(self):
        """
        Open WhatsApp and maximize the window.
        """
        pyautogui.press('win')
        time.sleep(2)
        pyautogui.typewrite('WhatsApp')
        time.sleep(3)
        pyautogui.press('enter')
        time.sleep(5)  # Wait for WhatsApp to open
        pyautogui.hotkey('win', 'up')
        time.sleep(1)

    def is_whatsapp_running(self):
        """
        Check if WhatsApp is running.
        Brings WhatsApp to the foreground if running, else opens WhatsApp.
        """
        for process in psutil.process_iter(['name']):
            if process.info['name'] == 'WhatsApp.exe':
                print('WhatsApp process is running.')
                self.bring_whatsapp_to_foreground()
                return True
        print('WhatsApp process is not running.')
        time.sleep(2)
        self.open_whatsapp()
        return False

    def search_username(self):
        """
        Search for a username in WhatsApp.
        """
        if not self.username:
            self.username = self.get_username_from_speech() or self.get_username_from_text()
        
        pyautogui.hotkey('ctrl', 'f')  # Use 'command' for macOS
        time.sleep(1)
        
        pyautogui.typewrite(self.username)
        time.sleep(2)  # Wait for the search results to appear
        
        # Example coordinates for the first search result (adjust as needed)
        first_result_x, first_result_y = 200, 200
        pyautogui.moveTo(first_result_x, first_result_y)
        pyautogui.click()
        time.sleep(2)  # Wait for the chat to open

    def send_messages(self):
        """
        Send a list of messages one by one.
        """
        if not self.messages:
            print("No messages to send.")
            self.speak_text("No messages to send.")
            return

        for message in self.messages:
            pyautogui.typewrite(message)
            pyautogui.press('enter')
            time.sleep(2)  # Optional: Wait between messages

    def get_username_from_speech(self):
        """
        Capture the username from speech input.
        """
        with sr.Microphone() as source:
            print("Please say the username:")
            self.speak_text("Please say the username.")
            audio = self.recognizer.listen(source)
            try:
                username = self.recognizer.recognize_google(audio)
                print(f'Username recognized: {username}')
                return username
            except sr.UnknownValueError:
                self.speak_text("Sorry, I did not understand the audio.")
                print("Sorry, I did not understand the audio.")
            except sr.RequestError as e:
                self.speak_text(f"Could not request results; {e}")
                print(f"Could not request results; {e}")
        return None

    def get_username_from_text(self):
        """
        Capture the username from text input.
        """
        username = input("Please type the username: ")
        print(f'Username entered: {username}')
        return username

    def run(self):
        """
        Continuously listen for user input and perform actions.
        """
        while True:
            if not self.is_whatsapp_running():
                self.open_whatsapp()
                time.sleep(5)  # Wait for WhatsApp to open

            self.username = self.get_username_from_speech() or self.get_username_from_text()
            if self.username:
                self.search_username()
                self.send_messages()
            time.sleep(5)  #

