import tkinter as tk
import json
import random

# Загружаем вопросы из JSON-файла
def load_questions(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Инициализация главного окна и переменных
root = tk.Tk()
root.title("Quiz Application")
root.geometry("500x400")

# Глобальные переменные
questions = load_questions('questions.json')  # ваш JSON файл с вопросами
current_question = 0
score = 0

# Виджеты
question_label = tk.Label(root, text="", font=("Arial", 16), wraplength=400)
question_label.pack(pady=20)
radio_buttons = []
selected_option = tk.StringVar()  # Глобальная переменная для выбранного варианта

# Функция для загрузки вопроса
def load_question():
    global current_question, radio_buttons, selected_option
    question_data = questions[current_question]
    question_label.config(text=question_data["question"])
    selected_option.set(None)
    for rb in radio_buttons:
        rb.destroy()
    radio_buttons.clear()
    for option in question_data["options"]:
        rb = tk.Radiobutton(root, text=option, variable=selected_option, value=option, font=("Arial", 12), anchor="w")
        rb.pack(anchor="w", padx=20)
        radio_buttons.append(rb)

# Функция для проверки ответа
def check_answer():
    global current_question, score
    selected_value = selected_option.get()
    if selected_value == questions[current_question]["answer"]:
        score += 1
    current_question += 1
    if current_question < len(questions):
        load_question()
    else:
        show_result()

# Функция для досрочного завершения
def finish_quiz():
    show_result()

# Функция для перемешивания вопросов
def shuffle_questions():
    global questions, current_question, score
    random.shuffle(questions)  # Перемешиваем список вопросов
    current_question = 0  # Сбрасываем текущий вопрос на начало
    score = 0  # Обнуляем счёт
    load_question()  # Загружаем первый вопрос

# Функция для отображения результата
def show_result():
    question_label.config(text=f"Ваш результат: {score} из {current_question}")
    for rb in radio_buttons:
        rb.destroy()
    submit_button.config(state="disabled")
    finish_button.config(state="disabled")
    shuffle_button.config(state="disabled")

# Фрейм для кнопок "Submit" и "Finish"
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Кнопка для подтверждения выбора
submit_button = tk.Button(button_frame, text="Submit", command=check_answer, font=("Arial", 14))
submit_button.pack(side=tk.LEFT, padx=10)

# Кнопка для досрочного завершения
finish_button = tk.Button(button_frame, text="Finish", command=finish_quiz, font=("Arial", 14))
finish_button.pack(side=tk.LEFT, padx=10)

# Кнопка для перемешивания вопросов
shuffle_button = tk.Button(root, text="Shuffle Questions", command=shuffle_questions, font=("Arial", 14))
shuffle_button.pack(pady=20)  # Размещаем под ответами

# Загрузка первого вопроса
load_question()

# Запуск основного цикла
root.mainloop()
