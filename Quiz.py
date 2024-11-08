import tkinter as tk
import json
import random


# Загружаем вопросы из JSON-файла
# Тут тоже не забудь поменять
def load_questions(questionsITP):
    with open(questionsITP, encoding='utf-8') as file:
        return json.load(file)


# Инициализация главного окна и переменных
root = tk.Tk()
root.title("Quiz Application")
root.geometry("600x600")

# Глобальные переменные
questions = load_questions('questionsITP.json')  # Нужно поменять JSON на нужный
current_question = 0
score = 0
incorrect_questions = []  # Список для хранения неправильных вопросов

# Виджеты
question_label = tk.Label(root, text="", font=("Aptos", 16), wraplength=400)
question_label.pack(pady=20)
radio_buttons = []
selected_option = tk.StringVar()  # Глобальная переменная для выбранного варианта
status_label = tk.Label(root, text="", font=("Arial", 12))  # Лейбл для отображения оставшихся вопросов
status_label.pack(pady=10)


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

    # Обновляем статус оставшихся вопросов
    remaining_questions = len(questions) - current_question
    status_label.config(text=f"{remaining_questions} questions left")


# Функция для проверки ответа
def check_answer():
    global current_question, score, incorrect_questions
    selected_value = selected_option.get()
    if selected_value == questions[current_question]["answer"]:
        score += 1
    else:
        incorrect_questions.append(current_question)  # Добавляем номер вопроса с ошибкой
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
    global questions, current_question, score, incorrect_questions
    random.shuffle(questions)  # Перемешиваем список вопросов
    current_question = 0  # Сбрасываем текущий вопрос на начало
    score = 0  # Обнуляем счёт
    incorrect_questions.clear()  # Очищаем список неправильных вопросов
    load_question()  # Загружаем первый вопрос


# Функция для отображения результата
def show_result():
    question_label.config(text=f"Ваш результат: {score} из {len(questions)}")
    result_text = "Ошибки:\n"
    for idx in incorrect_questions:
        result_text += f"Вопрос {idx + 1}: {questions[idx]['question']}\n"
    question_label.config(text=result_text)
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
