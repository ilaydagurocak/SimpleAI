from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader
import speech_recognition as sr
from gtts import gTTS
from SimpleAI import SimpleAI  # Now importing from SimpleAI.py

class ChatApp(App):

    def build(self):
        self.recognizer = sr.Recognizer()
        self.ai = SimpleAI()

        layout = BoxLayout(orientation='vertical')

        self.output_label = Label(text='Hello! How can I assist you today?', size_hint=(1, 0.2))
        layout.add_widget(self.output_label)

        self.user_input = TextInput(hint_text="Type here...", size_hint=(0.8, 0.1))
        layout.add_widget(self.user_input)

        button_layout = BoxLayout()

        self.send_button = Button(text="Send", size_hint=(0.4, 0.1))
        self.send_button.bind(on_press=self.send_message)
        button_layout.add_widget(self.send_button)

        self.voice_button = Button(text="Speak", size_hint=(0.4, 0.1))
        self.voice_button.bind(on_press=self.voice_input)
        button_layout.add_widget(self.voice_button)

        layout.add_widget(button_layout)

        return layout

    def send_message(self, instance):
        user_message = self.user_input.text
        response = self.ai.get_response(user_message)
        self.output_label.text = response

    def voice_input(self, instance):
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source)
            try:
                voice_text = self.recognizer.recognize_google(audio)
                response = self.ai.get_response(voice_text)
                self.output_label.text = response
                self.generate_response_audio(response)
            except sr.UnknownValueError:
                self.output_label.text = "I'm sorry, I didn't catch that."
            except sr.RequestError:
                self.output_label.text = "Sorry, the speech service is down."
            except Exception as e:
                self.output_label.text = str(e)

    def generate_response_audio(self, response):
        tts = gTTS(text=response, lang='en')
        tts.save("ai_response.mp3")

        sound = SoundLoader.load("ai_response.mp3")
        if sound:
            sound.play()

if __name__ == "__main__":
    ChatApp().run()
