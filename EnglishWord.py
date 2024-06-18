from  tkinter import *
import random

window = Tk()
window.title("영어 단어 암기하기")

file_path = r'C:\Users\sky70\OneDrive\바탕 화면\김민진\코딩\EnglishWord\EnglishWordList.txt'

# 파일에서 단어와 뜻을 읽어 딕셔너리에 저장
def LearnWord(window, file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        english_list = {}
        for string in file:
            s = string.split()
            key = s.pop(0)
            value = ' '.join(str(x) for x in s)
            english_list[key] = value
    already_use=[]
    word_list=list(english_list.keys())

    label = Label(window, text="", height=2)
    label.grid(row=0, column=0, columnspan=2)

    btn1 = Button(window, text="", width=25, height=2)
    btn1.grid(row=1, column=0)
    btn2 = Button(window, text="", width=25, height=2)
    btn2.grid(row=1, column=1)
    btn3 = Button(window, text="", width=25, height=2)
    btn3.grid(row=2, column=0)
    btn4 = Button(window, text="", width=25, height=2)
    btn4.grid(row=2, column=1)

    def update_labels():
        word = random.choice(list(set(word_list)-set(already_use)))
        correct_answer = english_list[word]
        possible_answers = random.sample(list(english_list.values()), 4)
        already_use.append(word)

        if correct_answer in possible_answers:
            possible_answers.remove(correct_answer)
        else:
            possible_answers = possible_answers[:-1]
        possible_answers.append(correct_answer)
        random.shuffle(possible_answers)

        label.config(text=word)
        btn1.config(text=possible_answers[0])
        btn2.config(text=possible_answers[1])
        btn3.config(text=possible_answers[2])
        btn4.config(text=possible_answers[3])

    def check_answer(selected_answer):
        correct_answer = english_list[label.cget("text")]
        if selected_answer == correct_answer:
            update_labels()

# 버튼에 이벤트 핸들러 연결
    btn1.config(command=lambda: check_answer(btn1.cget("text")))
    btn2.config(command=lambda: check_answer(btn2.cget("text")))
    btn3.config(command=lambda: check_answer(btn3.cget("text")))
    btn4.config(command=lambda: check_answer(btn4.cget("text")))
    return update_labels

update_label = LearnWord(window, file_path)
update_label()

window.mainloop()