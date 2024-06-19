from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
import random
import os

code = 0
fontName = '온글잎 강동희.ttf'

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        BookName = ['고등 VOCA 콕', 'Book2', 'Book3']

        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        for i in range(1, 4):
            btn = Button(text=f'{BookName[i-1]}', font_name=fontName, font_size=20, size_hint_y=None, height=40)
            btn.bind(on_press=lambda x, num=i: self.on_button_press(num))
            layout.add_widget(btn)

        scroll_view = ScrollView()
        scroll_view.add_widget(layout)
    
        self.add_widget(scroll_view)

    def on_button_press(self, number):
        global code
        code = number * 100
        self.change_screen('branch')

    def change_screen(self, screen_name):
        self.manager.transition.direction = 'left'
        self.manager.current = screen_name

class BranchScreen(Screen):
    def __init__(self, **kwargs):
        super(BranchScreen, self).__init__(**kwargs)

        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        for i in range(1, 51):
            btn = Button(text=f'Unit {i}', font_name=fontName, font_size=20, size_hint_y=None, height=40)
            btn.bind(on_press=lambda x, num=i: self.on_button_press(num))
            layout.add_widget(btn)

        scroll_view = ScrollView()
        scroll_view.add_widget(layout)
    
        self.add_widget(scroll_view)

    def on_button_press(self, number):
        global code
        code += number
        print(code)
        self.change_screen('word')

    def change_screen(self, screen_name):
        self.manager.transition.direction = 'left'
        self.manager.current = screen_name

class WordScreen(Screen):
    app = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(WordScreen, self).__init__(**kwargs)

        self.layout = GridLayout(cols=2, spacing=10, padding=10)
        self.wordLabel = Label(text="Label", font_name=fontName, font_size=20)
        self.layout.add_widget(self.wordLabel)
        self.layout.add_widget(Label())

        self.btn1 = Button(text="1", font_name=fontName, font_size=20)
        self.btn2 = Button(text="2", font_name=fontName, font_size=20)
        self.btn3 = Button(text="3", font_name=fontName, font_size=20)
        self.btn4 = Button(text="4", font_name=fontName, font_size=20)

        self.btn1.bind(on_press=lambda x: self.check_answer(self.btn1.text))
        self.btn2.bind(on_press=lambda x: self.check_answer(self.btn2.text))
        self.btn3.bind(on_press=lambda x: self.check_answer(self.btn3.text))
        self.btn4.bind(on_press=lambda x: self.check_answer(self.btn4.text))

        self.layout.add_widget(self.btn1)
        self.layout.add_widget(self.btn2)
        self.layout.add_widget(self.btn3)
        self.layout.add_widget(self.btn4)

        self.add_widget(self.layout)
        self.load_words()

    def load_words(self):
        global code
        print(code)
        self.file_path = os.path.join(os.path.dirname(__file__), str(code) + '.txt')
        self.english_list = {}
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                for string in file:
                    s = string.split()
                    key = s.pop(0)
                    value = ' '.join(str(x) for x in s)
                    self.english_list[key] = value
            self.already_use = []
            self.word_list = list(self.english_list.keys())
            self.show_word()
        except FileNotFoundError:
            self.wordLabel.text = '파일을 찾을 수 없습니다.'

    def show_word(self):
        if len(set(self.word_list) - set(self.already_use)) == 0:
            self.wordLabel.text = "모든 단어를 학습했습니다."
            self.btn1.text = ""
            self.btn2.text = ""
            self.btn3.text = ""
            self.btn4.text = ""
            return

        word = random.choice(list(set(self.word_list) - set(self.already_use)))
        self.correct_answer = self.english_list[word]
        possible_answers = random.sample(list(self.english_list.values()), 4)
        self.already_use.append(word)

        if self.correct_answer in possible_answers:
            possible_answers.remove(self.correct_answer)
        else:
            possible_answers = possible_answers[:-1]
        possible_answers.append(self.correct_answer)
        random.shuffle(possible_answers)

        self.wordLabel.text = word
        self.btn1.text = possible_answers[0]
        self.btn2.text = possible_answers[1]
        self.btn3.text = possible_answers[2]
        self.btn4.text = possible_answers[3]

    def check_answer(self, selected_answer):
        if selected_answer == self.correct_answer:
            self.show_word()
        
    def change_screen(self, screen_name):
        self.manager.transition.direction = 'left'
        self.manager.current = screen_name

class EnglishApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(BranchScreen(name='branch'))
        sm.add_widget(WordScreen(name='word', app=self))
        return sm

if __name__ == '__main__':
    EnglishApp().run()