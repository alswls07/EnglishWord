from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.clock import Clock
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

        back_btn=Button(text='뒤로가기', font_name=fontName, font_size=20, size_hint_y=None, height=40)
        back_btn.bind(on_press=lambda x: self.back())
        layout.add_widget(back_btn)

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
        self.change_screen('word', 0)

    def back(self):
        self.change_screen('main', 1)

    def change_screen(self, screen_name, num):
        if num==0:
            self.manager.transition.direction='left'
        else:
            self.manager.transition.direction='right'
        self.manager.current=screen_name

class WordScreen(Screen):
    app = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(WordScreen, self).__init__(**kwargs)

        self.layout = GridLayout(cols=2, spacing=10, padding=10)
        self.wordLabel = Label(text="Label", font_name=fontName, font_size=40)
        self.layout.add_widget(self.wordLabel)
        self.timeLabel=Label(text='Time', font_name=fontName, font_size=40)
        self.layout.add_widget(self.timeLabel)

        self.btn1 = Button(text="1", font_name=fontName, font_size=30)
        self.btn2 = Button(text="2", font_name=fontName, font_size=30)
        self.btn3 = Button(text="3", font_name=fontName, font_size=30)
        self.btn4 = Button(text="4", font_name=fontName, font_size=30)

        self.btn1.bind(on_press=lambda x: self.check_answer(self.btn1.text))
        self.btn2.bind(on_press=lambda x: self.check_answer(self.btn2.text))
        self.btn3.bind(on_press=lambda x: self.check_answer(self.btn3.text))
        self.btn4.bind(on_press=lambda x: self.check_answer(self.btn4.text))

        self.layout.add_widget(self.btn1)
        self.layout.add_widget(self.btn2)
        self.layout.add_widget(self.btn3)
        self.layout.add_widget(self.btn4)

        self.add_widget(self.layout)
        self.on_enter()

    def on_enter(self):
        global code
        self.file_path = os.path.join(os.path.dirname(__file__), 'WordFile', str(code) + '.txt')
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
        if len(self.word_list)==len(self.already_use):
            self.wordLabel.text = "모든 단어를 학습했습니다."
            self.btn1.text = ""
            self.btn2.text = ""
            self.btn3.text = ""
            self.btn4.text = ""
            Clock.schedule_once(lambda dt: self.change_screen('main'), 2)
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
        selected_button = None
        if selected_answer == self.correct_answer:
            if self.btn1.text == self.correct_answer:
                selected_button = self.btn1
            elif self.btn2.text == self.correct_answer:
                selected_button = self.btn2
            elif self.btn3.text == self.correct_answer:
                selected_button = self.btn3
            elif self.btn4.text == self.correct_answer:
                selected_button = self.btn4
       
        correct_button=None
        if self.correct_answer==self.btn1.text:
            correct_button=self.btn1
        elif self.correct_answer==self.btn2.text:
            correct_button=self.btn2
        elif self.correct_answer==self.btn3.text:
            correct_button=self.btn3
        elif self.correct_answer==self.btn4.text:
            correct_button=self.btn4

        if selected_button is not None:
            self.show_word()
        else:
            if self.btn1.text == selected_answer:
                incorrect_button = self.btn1
            elif self.btn2.text == selected_answer:
                incorrect_button = self.btn2
            elif self.btn3.text == selected_answer:
                incorrect_button = self.btn3
            elif self.btn4.text == selected_answer:
                incorrect_button = self.btn4

            self.disable_buttons()

            correct_button.background_color = (0, 1, 0, 1)
            incorrect_button.background_color = (1, 0, 0, 1)
            Clock.schedule_once(lambda dt: self.init_color(correct_button, incorrect_button), 1)
            Clock.schedule_once(lambda dt: self.enable_buttons(), 1)
            Clock.schedule_once(lambda dt: self.show_word(), 1)
       
    def init_color(self, correct_button, incorrect_button):
        correct_button.background_color = (1, 1, 1, 1)
        incorrect_button.background_color = (1, 1, 1, 1)

    def disable_buttons(self):
        self.btn1.disabled = True
        self.btn2.disabled = True
        self.btn3.disabled = True
        self.btn4.disabled = True
   
    def enable_buttons(self):
        self.btn1.disabled = False
        self.btn2.disabled = False
        self.btn3.disabled = False
        self.btn4.disabled = False

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