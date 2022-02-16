import random
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
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel, MDIcon
import gensim
from tensorflow.keras.utils import get_file
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.utils import get_color_from_hex
from kivy.animation import Animation

# creating a screen manager
class Manager(ScreenManager):
    pass

# creating child classes of screen
# for splash screen on startup
class MenuScreen(Screen):
    pass

# for each game
class MathsScreen(Screen):
    pass

class OddScreen(Screen):
    pass

class ClosestScreen(Screen):
    pass

class MatchScreen(Screen):
    pass

# to show whenever there is a correct/incorrect answer
class CorrectScreen(Screen):
    pass

class IncorrectScreen(Screen):
    pass

# and a screen to show scores for all games
class ScoresScreen(Screen):
    pass

# made the window roughly phone sized to check how it will look there
Window.size = (400,700)

class wordGames(MDApp):

    #some properties for later use
    odd_correct = 0
    odd_total = 0
    maths_correct = 0
    maths_total = 0
    closest_correct = 0
    closest_total = 0
    odd_options = {"...":False, "...": False, "...":False, "...": False}
    selected_count = 0
    selected1 = None
    selected2 = None
    match_correct = 0
    match_total = 0

    # building the app with the .kv string above and screen class instances for each screen
    def build(self):
        #changing window name from default
        self.title = 'Word2Vec Games'
        # setting some colour themes
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"

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
        self.match_screen = MatchScreen()
        sm.add_widget(self.match_screen)

        self.scores_screen = ScoresScreen()
        sm.add_widget(self.scores_screen)

        self.correct_screen = CorrectScreen()
        sm.add_widget(self.correct_screen)
        self.incorrect_screen = IncorrectScreen()
        sm.add_widget(self.incorrect_screen)

        # running load model to test working
        self.load_model()

        # loading kv file with app components
        kv_file = Builder.load_file('app.kv')

        #returning the loaded app with screen manager root
        return kv_file

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
            self.root.transition.direction='left'
            self.root.current = 'Correct'
            Clock.schedule_once(self.back_to_maths, 2)
            self.maths_correct += 1
            self.maths_total += 1
            self.update_all_scores()

        else:
            self.root.transition.direction='right'
            self.root.current = 'Incorrect'
            Clock.schedule_once(self.back_to_maths, 2)
            self.maths_total += 1
            self.update_all_scores()

        #later will prob do text processing which may affect how evaluate
        # also should strip in case user put space or pressed enter etc

    def back_to_maths(self, *args):
        self.root.transition.direction='right'
        self.root.current = 'Maths'
        self.root.get_screen('Maths').ids.maths_ans.text = ""
        self.set_maths_question()

    # this methods is for updating all the labels that display the scores
    def update_all_scores(self):
        self.root.get_screen('Odd').ids.odd_scorebar.title = "Score: " + str(self.odd_correct) + '/' + str(self.odd_total)
        self.root.get_screen('Scores').ids.odd_score.text = 'Odd One Out Score: ' + str(self.odd_correct) + '/' + str(self.odd_total)
        self.root.get_screen('Closest').ids.closest_scorebar.title = "Score: " + str(self.closest_correct) + '/' + str(self.closest_total)
        self.root.get_screen('Scores').ids.closest_score.text = 'Closest Pair Score: ' + str(self.closest_correct) + '/' + str(self.closest_total)
        self.root.get_screen('Maths').ids.maths_scorebar.title = "Score: " + str(self.maths_correct) + '/' + str(self.maths_total)
        self.root.get_screen('Scores').ids.maths_score.text = 'Word Maths Score: ' + str(self.maths_correct) + '/' + str(self.maths_total)
        self.root.get_screen('Scores').ids.total_score.text = 'Total: ' + str(int((self.odd_correct + self.closest_correct + self.maths_correct)/(self.odd_total + self.closest_total + self.maths_total) * 100)) + '%'


    def evaluate_odd(self, selected):
        selected = selected.text

        if self.odd_options[selected] == True:
            self.root.transition.direction='left'
            self.root.current = 'Correct'
            Clock.schedule_once(self.back_to_odd, 2)
            self.odd_correct += 1
            self.odd_total +=1
            self.update_all_scores()

        else:
            self.root.transition.direction='right'
            self.root.current = 'Incorrect'
            Clock.schedule_once(self.back_to_odd, 2)
            self.odd_total += 1
            self.update_all_scores()


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
        try:
            pair1word1 = random.choice(self.model.index_to_key)
            pair1word2 = random.choice([i[0] for i in self.model.most_similar(pair1word1, topn=20)])
            self.pair1 = [pair1word1, pair1word2]
            pair2word1 = random.choice(self.model.index_to_key)
            pair2word2 = random.choice([i[0] for i in self.model.most_similar(pair2word1, topn=50)])
            self.pair2 = [pair2word1, pair2word2]
            pair3word1 = random.choice(self.model.index_to_key)
            pair3word2 = random.choice([i[0] for i in self.model.most_similar(pair3word1, topn=50)])
            self.pair3 = [pair3word1, pair3word2]
            pair4word1 = random.choice(self.model.index_to_key)
            pair4word2 = random.choice([i[0] for i in self.model.most_similar(pair4word1, topn=50)])
            self.pair4 = [pair4word1, pair4word2]

            self.closest_pair = sorted([self.pair1, self.pair2, self.pair3, self.pair4], key= lambda x: self.model.similarity(x[0], x[1]))[-1]

            print([(i, self.model.similarity(i[0], i[1])) for i in self.closest_pair])

            self.root.get_screen('Closest').ids.pair_one.text = ", ".join(self.pair1)
            self.root.get_screen('Closest').ids.pair_two.text = ", ".join(self.pair2)
            self.root.get_screen('Closest').ids.pair_three.text = ", ".join(self.pair3)
            self.root.get_screen('Closest').ids.pair_four.text = ", ".join(self.pair4)

        # was getting ocassional gensim error with similarity comparison, this seems to fix although would be good to revisit
        except:
            self.set_closest_pair()


    def evaluate_closest(self, selected):
        if selected.text.split(", ") == self.closest_pair:
            self.root.transition.direction='left'
            self.root.current = 'Correct'
            Clock.schedule_once(self.back_to_closest, 2)
            self.closest_correct += 1
            self.closest_total += 1
            self.update_all_scores()

        else:
            self.root.transition.direction='right'
            self.root.current = 'Incorrect'
            Clock.schedule_once(self.back_to_closest, 2)
            self.closest_total += 1
            self.update_all_scores()

    def back_to_closest(self, *args):
        self.root.transition.direction='right'
        self.root.current = 'Closest'
        self.set_closest_pair()

    def set_pairs_match(self):
        pair1starter = random.choice(self.model.index_to_key)
        self.match_pair1 = [pair1starter, random.choice([i[0] for i in self.model.most_similar(pair1starter)])]
        pair2starter = random.choice(self.model.index_to_key)
        self.match_pair2 = [pair2starter, random.choice([i[0] for i in self.model.most_similar(pair2starter)])]
        pair3starter = random.choice(self.model.index_to_key)
        self.match_pair3 = [pair3starter, random.choice([i[0] for i in self.model.most_similar(pair3starter)])]
        pair4starter = random.choice(self.model.index_to_key)
        self.match_pair4 = [pair4starter, random.choice([i[0] for i in self.model.most_similar(pair4starter)])]

        shuffled_pairs = random.sample([self.match_pair1[0],self.match_pair2[0],self.match_pair3[0],self.match_pair4[0]], 4) + random.sample([self.match_pair1[1],self.match_pair2[1],self.match_pair3[1],self.match_pair4[1]], 4)
        print(self.match_pair1, self.match_pair2, self.match_pair3, self.match_pair4)

        self.root.get_screen('Match').ids.match_1.text = shuffled_pairs[0]
        self.root.get_screen('Match').ids.match_2.text = shuffled_pairs[1]
        self.root.get_screen('Match').ids.match_3.text = shuffled_pairs[2]
        self.root.get_screen('Match').ids.match_4.text = shuffled_pairs[3]
        self.root.get_screen('Match').ids.match_5.text = shuffled_pairs[4]
        self.root.get_screen('Match').ids.match_6.text = shuffled_pairs[5]
        self.root.get_screen('Match').ids.match_7.text = shuffled_pairs[6]
        self.root.get_screen('Match').ids.match_8.text = shuffled_pairs[7]

    def on_select(self, instance):
        self.selected_clr = [0.1,0.1,0.8,1]
        instance.md_bg_color = self.selected_clr
        self.selected_count += 1

        if self.selected_count==2:
            eval = self.evaluate_pair()
            self.handle_pair_submit(eval)

    def evaluate_pair(self):
        for child in self.root.get_screen('Match').children:
            for subchild in child.children:
                try:
                    print(subchild.md_bg_color)
                    if subchild.md_bg_color == self.selected_clr:
                        if self.selected1 == None:
                            self.selected1 = subchild.text
                        else:
                            self.selected2 = subchild.text
                except:
                    pass

        for i in [self.match_pair1, self.match_pair2, self.match_pair3, self.match_pair4]:
            if self.selected1 in i and self.selected2 in i:
                return True
        return False

    def handle_pair_submit(self, correct):
        # resetting and disabling
        self.selected1 = None
        self.selected2 = None
        self.selected_count = 0

        default_clr = [0.12941176470588237, 0.5882352941176471, 0.9529411764705882, 1.0]

        for child in self.root.get_screen('Match').children:
            for subchild in child.children:
                try:
                    if subchild.md_bg_color == self.selected_clr:
                        if correct == True:
                            subchild.md_bg_color_disabled = [0,1,0,1]
                            subchild.disabled = True
                        else:
                            subchild.md_bg_color = default_clr
                except:
                    pass
        if correct:
            self.match_correct += 1
        self.match_total += 1

        # print(self.match_correct, self.match_total)

# running the app
if __name__ == '__main__':
    wordGames().run()
