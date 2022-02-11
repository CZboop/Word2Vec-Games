import cv2
import random
import numpy as np
import matplotlib
from matplotlib import cm
import threading
from functools import partial
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.button import MDRaisedButton
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.uix.colorpicker import ColorPicker
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel, MDIcon
from datetime import datetime
import gensim
from tensorflow.keras.utils import get_file

# creating child classes of screen
class MainScreen(Screen):
    pass

class MenuScreen(Screen):
    pass

# creating a screen manager
class Manager(ScreenManager):
    pass

# made the window roughly phone sized to check how it will look there
Window.size = (450,750)

# .kv string to set out the layout and contents of the app
builder_str = '''
ScreenManager:
    MenuScreen:
    MainScreen:

<MenuScreen>:
    name: 'Menu'
    FloatLayout:
        MDLabel:
            text: "Word2Vec Maths"
            pos_hint: {'center_x':.5, 'center_y':.7}
            size_hint: 1.0, 0.2
            font_style: 'H3'
            color: (1,1,1,1)
            halign: 'center'

        MDIcon:
            icon: 'abacus'
            pos_hint: {'center_x':.25, 'center_y':.55}
            halign: 'center'

        MDIcon:
            icon: 'book'
            pos_hint: {'center_x':.5, 'center_y':.55}
            halign: 'center'
        MDIcon:
            icon: 'format-list-checkbox'
            pos_hint: {'center_x':.75, 'center_y':.55}
            halign: 'center'

        MDRaisedButton:
            text: 'Begin!'
            size_hint: 0.6, 0.1
            pos_hint: {'center_x': .5, 'center_y': .2}
            font_style: 'H5'
            on_release:
                root.manager.transition.direction='left'
                root.manager.current = 'Main'

<MainScreen>:
    name: "Main"
    FloatLayout:
        Image:
            id: vid
            size_hint: 1, 0.6
            allow_stretch: True
            keep_ratio: True
            pos_hint: {'center_x':0.5, 'top':0.8}

        MDRaisedButton:
            text: app.word
            pos_hint: {"x":0.0, "y":0.0}
            size_hint: 1.0, 0.12
            font_style: 'H6'
            on_release: pass

        MDToolbar:
            id: toolbar
            title: 'Menu'
            pos_hint: {'top': 1}
            elevation: 15
            left_action_items: [["menu", lambda x: nav_drawer.set_state("toggle")]]
        Widget:

    MDNavigationDrawer:
        id: nav_drawer
        FloatLayout:
            size_hint: 1.0, 1.0
            MDLabel:
                text: "Placeholder"
                size_hint: 1.0, 0.1
                pos_hint: {"x":0.3, "y":0.9}
            MDRaisedButton:
                text: "Placeholder"
                size_hint: 1.0, 0.09
                pos_hint: {"x":0.0, "y":0.81}
                on_release: pass
            MDRaisedButton:
                text: "Placeholder"
                size_hint: 1.0, 0.09
                pos_hint: {"x":0.0, "y":0.72}
                on_release: pass
            MDRaisedButton:
                text: "Placeholder"
                size_hint: 1.0, 0.09
                pos_hint: {"x":0.0, "y":0.63}
                on_release: pass
            MDRaisedButton:
                text: "Placeholder"
                size_hint: 1.0, 0.09
                pos_hint: {"x":0.0, "y":0.54}
                on_release: pass
            MDRaisedButton:
                text: "Placeholder"
                size_hint: 1.0, 0.09
                pos_hint: {"x":0.0, "y":0.45}
                on_release: pass
            MDRaisedButton:
                text: "Placeholder"
                size_hint: 1.0, 0.09
                pos_hint: {"x":0.0, "y":0.36}
                on_release: pass
            MDRaisedButton:
                text: "Placeholder"
                size_hint: 1.0, 0.09
                pos_hint: {"x":0.0, "y":0.27}
                on_release: pass
            MDRaisedButton:
                text: "Placeholder"
                size_hint: 1.0, 0.09
                pos_hint: {"x":0.0, "y":0.18}
                on_release: pass
            MDRaisedButton:
                text: "Placeholder"
                size_hint: 1.0, 0.09
                pos_hint: {"x":0.0, "y":0.09}
                on_release: pass
            MDRaisedButton:
                text: "Placeholder"
                size_hint: 1.0, 0.09
                pos_hint: {"x":0.0, "y":0.0}
                on_release: pass

'''
# note the above menu stuff placeholders may or may not use but keeping for the mo, eg if add multiple things in app

class wordMaths(MDApp):
    word = ""

    # building the app with the .kv string above and screen class instances for each screen
    def build(self):
        # setting some colour themes
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"

        # using the builder to parse the .kv string above for use by the app
        Builder.load_string(builder_str)

        # adding screens to the screen manager
        sm = ScreenManager()
        self.welcome_screen = MenuScreen()
        sm.add_widget(self.welcome_screen)
        self.main_screen = MainScreen()
        sm.add_widget(self.main_screen)
        # running load model to test working
        self.load_model()

        #returning the screen manager with all screens
        return sm

    def load_model(self):
        try:
            path = get_file('GoogleNews-vectors-negative300.bin.gz',
                origin='https://s3.amazonaws.com/dl4j-distribution/' +\
                            'GoogleNews-vectors-negative300.bin.gz')
        except:
            print('Error with download')
            raise

        model = gensim.models.KeyedVectors.load_word2vec_format(path, binary=True, limit=30000)
        rand_word = random.choice(model.index_to_key)
        print(rand_word)
        # will prob exclude words that have special chars, some in dataset seem to use hashtags as wildcards etc.
        self.word = rand_word

    def maths_game(self):
        # vaguely will get three words and present in the format word =/- ? = word
        #and can maybe take top x most similar and give some points if not first option
        pass

# running the app
if __name__ == '__main__':
    wordMaths().run()
