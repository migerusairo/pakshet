import json

import colorama
import numpy as np
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.utils import rgba
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import Snackbar
from tensorflow import keras

colorama.init()

import pickle


# Main application------------------------------------------------------------------------------------------------------
class Command(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_name = "PoppinsEL.otf"
    font_size = 14


class Response(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_name = "PoppinsEL.otf"
    font_size = 14


class TCUAdvisor(MDApp):
    def build(self):

        self.icon = "TCULogo.jpg"

        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.material_style = "M3"

        global screen
        screen = ScreenManager(transition=SlideTransition(duration=.7))
        screen.add_widget(Builder.load_file("Introduction.kv"))
        screen.add_widget(Builder.load_file("Login.kv"))
        screen.add_widget(Builder.load_file("Register.kv"))
        screen.add_widget(Builder.load_file("Admin_login.kv"))
        screen.add_widget(Builder.load_file("Admin_Home-screen.kv"))
        screen.add_widget(Builder.load_file("Welcome-screen.kv"))
        screen.add_widget(Builder.load_file("Home-screen.kv"))
        screen.add_widget(Builder.load_file("Notification-screen.kv"))
        screen.add_widget(Builder.load_file("Profile-screen.kv"))
        screen.add_widget(Builder.load_file("Setting-screen.kv"))
        screen.add_widget(Builder.load_file("About.kv"))
        screen.add_widget(Builder.load_file("Forgot-password.kv"))
        screen.add_widget(Builder.load_file("Terms&Condition.kv"))
        screen.add_widget(Builder.load_file("Terms&Condition1.kv"))

        screen.add_widget(Builder.load_file("add_command.kv"))

        return screen

    def send(self):
        with open("intents.json") as file:
            data = json.load(file)

        # load trained model
        model = keras.models.load_model('chat_model')

        # load tokenizer object
        with open('tokenizer.pickle', 'rb') as handle:
            tokenizer = pickle.load(handle)

        # load label encoder object
        with open('label_encoder.pickle', 'rb') as enc:
            lbl_encoder = pickle.load(enc)

        # parameters
        max_len = 20

        if screen.get_screen('Home-screen').text_input != "":
            inp = screen.get_screen('Home-screen').text_input.text

            screen.get_screen('Home-screen').chat_list.add_widget(
                Command(text=inp, size_hint_x=.5, halign="justify"))

            result = model.predict(
                keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]), truncating='post',
                                                           maxlen=max_len))
            tag = lbl_encoder.inverse_transform([np.argmax(result)])

            for i in data['intents']:
                if i['tag'] == tag:
                    screen.get_screen('Home-screen').chat_list.add_widget(
                        Response(text=np.random.choice(i['responses']), size_hint_x=.5, halign="justify"))

                    screen.get_screen('Home-screen').text_input.text = ""

    # Inputs-------------------------------------------------------------------------------------------------------
    def clear_registration_fields(self):
        screen = self.root.get_screen('Register')
        screen.ids.stud_id.text = ""
        screen.ids.fname.text = ""
        screen.ids.lname.text = ""
        screen.ids.year.text = ""
        screen.ids.course.text = ""
        screen.ids.section.text = ""
        screen.ids.email.text = ""
        screen.ids.password.text = ""
        screen.ids.confirmpassword.text = ""

    def clear_admin_login_fields(self):
        screen = self.root.get_screen('Admin_login')
        screen.ids.admin_id.text = ""
        screen.ids.admin_password.text = ""

    def clear_user_login_fields(self):
        screen = self.root.get_screen('Login')
        screen.ids.email.text = ""
        screen.ids.password.text = ""

    # Admin & User
    # Logout---------------------------------------------------------------------------------------------------

    # other functions--------------------------------------------------------------------------------------------------
    def userlogout(self):
        Snackbar(text="Logged out successful!",
                 snackbar_animation_dir="Top",
                 font_size='12sp',
                 snackbar_x=.1,
                 size_hint_x=.999,
                 size_hint_y=.07,
                 bg_color=(1, 0, 0, 1)
                 ).open()

        self.root.current = 'Login'

    def adminlogout(self):
        Snackbar(text="Logged out successful!",
                 snackbar_animation_dir="Top",
                 font_size='12sp',
                 snackbar_x=.1,
                 size_hint_x=.999,
                 size_hint_y=.07,
                 bg_color=(1, 0, 0, 1)
                 ).open()
        self.root.current = 'Admin_login'

    def carousel_autonext(self):
        screen = self.root.get_screen('Welcome-screen')
        carousel = screen.ids.carousel
        Clock.schedule_interval(carousel.load_next, 4)

        screen = self.root.get_screen('Setting-screen')
        carousel_1 = screen.ids.carousel_1
        carousel_1.loop = True
        Clock.schedule_interval(carousel_1.load_next, 3)

    def current_slide(self, index):
        screen = self.root.get_screen('Welcome-screen')
        for i in range(2):
            if index == i:
                screen.ids[f"slide{index}"].color = rgba(255, 0, 0, 255)
            else:
                screen.ids[f"slide{i}"].color = rgba(170, 170, 170, 255)

        screen = self.root.get_screen('Register')
        for i in range(2):
            if index == i:
                screen.ids[f"slide{index}"].color = rgba(255, 0, 0, 255)
            else:
                screen.ids[f"slide{i}"].color = rgba(170, 170, 170, 255)

    def next(self):
        screen = self.root.get_screen('Register')
        carousel = screen.ids.carousel
        carousel.load_next(mode="next")

    def on_touch(self, instance):
        pass

    def on_start(self):
        Clock.schedule_once(self.start, 7)

    def start(self, *args):
        self.root.current = "Login"


if __name__ == "__main__":
    TCUAdvisor().run()

# -----------------------------------------------------
# screen = self.root.get_screen('Login')
# bg_image = screen.ids.bg_image
# Animation(x=-dp(300), d=30).start(bg_image)
