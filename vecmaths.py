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
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
import time

# creating child classes of screen
class MathsScreen(Screen):
    pass

class MenuScreen(Screen):
    pass

class OddScreen(Screen):
    pass

# creating a screen manager
class Manager(ScreenManager):
    pass

# creating screens for correct and incorrect answers
class CorrectScreen(Screen):
    pass

class IncorrectScreen(Screen):
    pass

# screen for selecting closest pair of words
class ClosestScreen(Screen):
    pass

# made the window roughly phone sized to check how it will look there
Window.size = (400,700)

# .kv string to set out the layout and contents of the app
builder_str = '''
ScreenManager:
    MenuScreen:
    MathsScreen:
    OddScreen:
    CorrectScreen:
    IncorrectScreen:
    ClosestScreen:

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

        MDLabel:
            text: "Word Games with Word2Vec!"
            pos_hint: {'center_x':.5, 'center_y':.4}
            size_hint: 1.0, 0.2
            font_style: 'H5'
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
                app.set_odd_options()
                root.manager.transition.direction='left'
                root.manager.current = 'Odd'

<MathsScreen>:
    name: "Maths"
    FloatLayout:
        MDLabel:
            id: maths_question
            text: "Test"
            pos_hint: {'center_x': .5, 'top': 0.85}
            size_hint: 1.0, 0.2
            font_style: 'H5'
            color: (1,1,1,1)
            halign: 'center'


        TextInput:
            id: maths_ans
            size_hint: 0.8, 0.05
            pos_hint: {'center_x':0.5, 'top':0.62}

        MDRaisedButton:
            text: 'Submit'
            pos_hint: {"center_x":0.5, "y":0.3}
            size_hint: 0.8, 0.1
            font_style: 'H6'
            on_press: app.evaluate_maths_q()

        MDToolbar:
            id: toolbar
            title: 'Menu'
            pos_hint: {'top': 1}
            elevation: 15
            left_action_items: [["menu", lambda x: nav_drawer.set_state("toggle")]]

        MDToolbar:
            id: maths_scorebar
            title: 'Score: ' + str(app.maths_score)
            elevation: 15
            pos_hint: {'bottom': 1}

    MDNavigationDrawer:
        id: nav_drawer
        FloatLayout:
            size_hint: 1.0, 1.0
            MDLabel:
                text: "Game Selection"
                size_hint: 1.0, 0.1
                pos_hint: {"x":0.3, "y":0.9}
            MDRaisedButton:
                text: "Odd One Out"
                size_hint: 1.0, 0.09
                pos_hint: {"x":0.0, "y":0.81}
                on_release:
                    app.set_odd_options()
                    root.manager.transition.direction='left'
                    root.manager.current = 'Odd'

            MDRaisedButton:
                text: "Word Maths"
                size_hint: 1.0, 0.09
                pos_hint: {"x":0.0, "y":0.72}
                on_release:
                    app.set_maths_question()
                    root.manager.transition.direction='left'
                    root.manager.current = 'Maths'

            MDRaisedButton:
                text: "Closest Pair"
                size_hint: 1.0, 0.09
                pos_hint: {"x":0.0, "y":0.63}
                on_release:
                    app.set_closest_pair()
                    root.manager.transition.direction='left'
                    root.manager.current = 'Closest'

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

<CorrectScreen>:
    name: 'Correct'
    id: correct
    FloatLayout:
        MDLabel:
            text: 'CORRECT!'
            pos_hint: {'center_x':.5, 'center_y':.5}
            font_style: 'H2'
            color: (1,1,1,1)
            halign: 'center'

<IncorrectScreen>:
    name: 'Incorrect'
    id: incorrect
    FloatLayout:
        MDLabel:
            text: 'INCORRECT :('
            pos_hint: {'center_x':.5, 'center_y':.5}
            font_style: 'H2'
            color: (1,1,1,1)
            halign: 'center'

<OddScreen>:
    id: odd
    name: "Odd"
    FloatLayout:
        MDLabel:
            text: "Which word is the odd one out?"
            pos_hint: {'center_x':.5, 'y':.73}
            size_hint: 1.0, 0.2
            font_style: 'H5'
            color: (1,1,1,1)
            halign: 'center'

        MDRaisedButton:
            id: four
            text: 'Word 4'
            pos_hint: {"center_x":0.5, "y":0.2}
            size_hint: 0.8, 0.1
            font_style: 'H6'
            on_press: app.evaluate_odd(self)

        MDRaisedButton:
            id: three
            text: 'Word 3'
            pos_hint: {"center_x":0.5, "y":0.35}
            size_hint: 0.8, 0.1
            font_style: 'H6'
            on_press: app.evaluate_odd(self)

        MDRaisedButton:
            id: two
            text: 'Word 2'
            pos_hint: {"center_x":0.5, "y":0.5}
            size_hint: 0.8, 0.1
            font_style: 'H6'
            on_press: app.evaluate_odd(self)

        MDRaisedButton:
            id: one
            text: str(app.odd_options)
            pos_hint: {"center_x":0.5, "y":0.65}
            size_hint: 0.8, 0.1
            font_style: 'H6'
            on_press: app.evaluate_odd(self)

        MDToolbar:
            id: toolbar
            title: 'Menu'
            pos_hint: {'top': 1}
            elevation: 15
            left_action_items: [["menu", lambda x: nav_drawer.set_state("toggle")]]

        MDToolbar:
            id: odd_scorebar
            title: 'Score: ' + str(app.odd_correct)
            elevation: 15
            pos_hint: {'bottom': 1}

    MDNavigationDrawer:
        id: nav_drawer
        FloatLayout:
            size_hint: 1.0, 1.0
            MDLabel:
                text: "Game Selection"
                size_hint: 1.0, 0.1
                pos_hint: {"x":0.3, "y":0.9}
            MDRaisedButton:
                text: "Odd One Out"
                size_hint: 1.0, 0.09
                pos_hint: {"x":0.0, "y":0.81}
                on_release:
                    root.manager.transition.direction='left'
                    root.manager.current = 'Odd'
            MDRaisedButton:
                text: "Word Maths"
                size_hint: 1.0, 0.09
                pos_hint: {"x":0.0, "y":0.72}
                on_release:
                    app.set_maths_question()
                    root.manager.transition.direction='left'
                    root.manager.current = 'Maths'
            MDRaisedButton:
                text: "Closest Pair"
                size_hint: 1.0, 0.09
                pos_hint: {"x":0.0, "y":0.63}
                on_release:
                    app.set_closest_pair()
                    root.manager.transition.direction='left'
                    root.manager.current = 'Closest'
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

<ClosestScreen>:
    id: closest
    name: "Closest"
    FloatLayout:
        MDLabel:
            text: "Which pair is the most related?"
            pos_hint: {'center_x':.5, 'y':.73}
            size_hint: 1.0, 0.2
            font_style: 'H5'
            color: (1,1,1,1)
            halign: 'center'

        MDRaisedButton:
            id: pair_four
            text: '...'
            pos_hint: {"center_x":0.5, "y":0.2}
            size_hint: 0.8, 0.1
            font_style: 'H6'
            on_press: app.evaluate_closest(self)

        MDRaisedButton:
            id: pair_three
            text: '...'
            pos_hint: {"center_x":0.5, "y":0.35}
            size_hint: 0.8, 0.1
            font_style: 'H6'
            on_press: app.evaluate_closest(self)

        MDRaisedButton:
            id: pair_two
            text: '...'
            pos_hint: {"center_x":0.5, "y":0.5}
            size_hint: 0.8, 0.1
            font_style: 'H6'
            on_press: app.evaluate_closest(self)

        MDRaisedButton:
            id: pair_one
            text: '...'
            pos_hint: {"center_x":0.5, "y":0.65}
            size_hint: 0.8, 0.1
            font_style: 'H6'
            on_press: app.evaluate_closest(self)

        MDToolbar:
            id: toolbar
            title: 'Menu'
            pos_hint: {'top': 1}
            elevation: 15
            left_action_items: [["menu", lambda x: nav_drawer.set_state("toggle")]]

        MDToolbar:
            id: odd_scorebar
            title: 'Score: ' + str(app.closest_correct)
            elevation: 15
            pos_hint: {'bottom': 1}

    MDNavigationDrawer:
        id: nav_drawer
        FloatLayout:
            size_hint: 1.0, 1.0
            MDLabel:
                text: "Game Selection"
                size_hint: 1.0, 0.1
                pos_hint: {"x":0.3, "y":0.9}
            MDRaisedButton:
                text: "Odd One Out"
                size_hint: 1.0, 0.09
                pos_hint: {"x":0.0, "y":0.81}
                on_release:
                    root.manager.transition.direction='left'
                    root.manager.current = 'Odd'
            MDRaisedButton:
                text: "Word Maths"
                size_hint: 1.0, 0.09
                pos_hint: {"x":0.0, "y":0.72}
                on_release:
                    app.set_maths_question()
                    root.manager.transition.direction='left'
                    root.manager.current = 'Maths'
            MDRaisedButton:
                text: "Closest Pair"
                size_hint: 1.0, 0.09
                pos_hint: {"x":0.0, "y":0.63}
                on_release:
                    app.set_closest_pair()
                    root.manager.transition.direction='left'
                    root.manager.current = 'Closest'
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

class wordMaths(MDApp):

    #some properties for later use
    odd_correct = 0
    odd_wrong = 0
    maths_score = 0
    closest_correct = 0

    # building the app with the .kv string above and screen class instances for each screen
    def build(self):
        self.odd_options = {"...":False, "...": False, "...":False, "...": False}
        #changing window name from default
        self.title = 'Word2Vec Maths'
        # setting some colour themes
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"

        # using the builder to parse the .kv string above for use by the app
        Builder.load_string(builder_str)

        # adding screens to the screen manager
        sm = ScreenManager()
        self.welcome_screen = MenuScreen()
        sm.add_widget(self.welcome_screen)
        self.maths_screen = MathsScreen()
        sm.add_widget(self.maths_screen)
        self.odd_screen = OddScreen()
        sm.add_widget(self.odd_screen)
        self.closest_screen = ClosestScreen()
        sm.add_widget(self.closest_screen)

        self.correct_screen = CorrectScreen()
        sm.add_widget(self.correct_screen)
        self.incorrect_screen = IncorrectScreen()
        sm.add_widget(self.incorrect_screen)

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
            print('Could not download dataset')
            raise

        self.model = gensim.models.KeyedVectors.load_word2vec_format(path, binary=True, limit=30000)

    def set_maths_question(self):
        # will prob exclude words that have special chars, some in dataset seem to use hashtags as wildcards etc. uses underscores as spaces

        word1 = random.choice(self.model.index_to_key)
        word2 = random.choice(self.model.index_to_key)
        word3 = random.choice(self.model.index_to_key)
        ans = self.model.most_similar(positive=[word1, word2])
        self.maths_ans = ans # this is the list of tuples and later will get values and can check if top match etc
        print(self.maths_ans[0][0], self.maths_ans[5][0])
        # here there are a lot of results that are very similar to either of the starting words
        # processing dataset/creating own could eliminate plurals, capitalisation etc.
        # could try adjusting the equation or having a minimum linear algebra distance between each and the answer?

        self.root.get_screen('Maths').ids.maths_question.text =  '{} + {} = ?'.format(word1, word2)

    def evaluate_maths_q(self):
        user_ans = self.root.get_screen('Maths').ids.maths_ans.text.lower()

        if user_ans in [i[0].lower() for i in self.maths_ans]:
            print('correct')
            self.root.transition.direction='left'
            self.root.current = 'Correct'
            Clock.schedule_once(self.back_to_maths, 2)
            self.maths_score += 1
            self.root.get_screen('Maths').ids.maths_scorebar.title = "Score: " + str(self.maths_score)
        else:
            print('incorrect')
            self.root.transition.direction='left'
            self.root.current = 'Incorrect'
            Clock.schedule_once(self.back_to_maths, 2)

        #later will prob do text processing which may affect how evaluate
        # also should strip in case user put space or pressed enter etc

    def back_to_maths(self, *args):
        self.root.transition.direction='right'
        self.root.current = 'Maths'
        self.root.get_screen('Maths').ids.maths_ans.text = ""
        self.set_maths_question()


    def evaluate_odd(self, selected):
        selected = selected.text

        if self.odd_options[selected] == True:
            self.root.transition.direction='left'
            self.root.current = 'Correct'
            Clock.schedule_once(self.back_to_odd, 2)
            self.odd_correct += 1
            self.root.get_screen('Odd').ids.odd_scorebar.title = "Score: " + str(self.odd_correct)

        else:
            self.root.transition.direction='right'
            self.root.current = 'Incorrect'
            Clock.schedule_once(self.back_to_odd, 2)
            self.odd_wrong += 1

    def back_to_odd(self, *args):
        self.root.transition.direction='right'
        self.root.current = 'Odd'
        self.set_odd_options()

    def set_odd_options(self):
        self.odd_options = {}
        base_word = random.choice(self.model.index_to_key)
        related = self.model.most_similar(base_word)[:2]
        unrelated = random.choice(self.model.index_to_key)
        # and have a check to see that the unrelated is not also in the most similar longer list
        self.odd_options[base_word] = False
        self.odd_options[unrelated] = True

        for i in related:
            self.odd_options[i[0]] = False

        keys =  list(self.odd_options.keys())
        random.shuffle(keys)
        shuffled_options = [(key, self.odd_options[key]) for key in keys]
        self.odd_options = {}
        for i,j in shuffled_options:
            self.odd_options[i] = j

        self.set_button_text()

    def set_button_text(self):
        app = MDApp.get_running_app()
        self.root.get_screen('Odd').ids.one.text = list(self.odd_options.keys())[0]
        self.root.get_screen('Odd').ids.two.text = list(self.odd_options.keys())[1]
        self.root.get_screen('Odd').ids.three.text = list(self.odd_options.keys())[2]
        self.root.get_screen('Odd').ids.four.text = list(self.odd_options.keys())[3]


    def set_closest_pair(self):
        pair1word1 = random.choice(self.model.index_to_key)
        pair1word2 = random.choice([i[0] for i in self.model.most_similar(pair1word1, topn=20)])
        self.pair1 = [pair1word1, pair1word2]
        pair2word1 = random.choice(self.model.index_to_key)
        pair2word2 = random.choice([i[0] for i in self.model.most_similar(pair2word1, topn=20)])
        self.pair2 = [pair2word1, pair2word2]
        pair3word1 = random.choice(self.model.index_to_key)
        pair3word2 = random.choice([i[0] for i in self.model.most_similar(pair3word1, topn=50)])
        self.pair3 = [pair3word1, pair3word2]
        pair4word1 = random.choice(self.model.index_to_key)
        pair4word2 = random.choice([i[0] for i in self.model.most_similar(pair4word1, topn=50)])
        self.pair4 = [pair4word1, pair4word2]

        closest_pair = sorted([self.pair1, self.pair2, self.pair3, self.pair4], key= lambda x: self.model.similarity(x[0], x[1]))[-1]

        # print([(i, self.model.similarity(i[0], i[1])) for i in closest_pair])

        self.root.get_screen('Closest').ids.pair_one.text = ", ".join(self.pair1)
        self.root.get_screen('Closest').ids.pair_two.text = ", ".join(self.pair2)
        self.root.get_screen('Closest').ids.pair_three.text = ", ".join(self.pair3)
        self.root.get_screen('Closest').ids.pair_four.text = ", ".join(self.pair4)


    def evaluate_closest(self):
        pass

# running the app
if __name__ == '__main__':
    wordMaths().run()
