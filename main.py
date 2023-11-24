import flet as ft
from flet_core import MainAxisAlignment, CrossAxisAlignment, Column, Row, ElevatedButton
import time
import threading

class ToggleThemeButton(ft.IconButton):
    def __init__(self, on_click_callback, **kwargs) -> None:
        super().__init__(icon=ft.icons.WB_SUNNY_OUTLINED, on_click=on_click_callback, **kwargs)

def toggle_theme(page):
    if page.theme_mode == "light":
        page.theme_mode = "dark"
        page.bgcolor = "#2C3E50"  # Set the dark mode background color
    else:
        page.theme_mode = "light"
        page.bgcolor = "#d5cdc4"  # Set the light mode background color

    page.update()


def QuizGame(page: ft.Page):
    chat = ft.Column()
    appbar = ft.AppBar(
        leading_width=100,
        actions=[ToggleThemeButton(on_click_callback=lambda e: toggle_theme(page)),],
        title=ft.Text("Quiz Game", weight=ft.FontWeight.W_700, text_align='Center'),
        bgcolor=ft.colors.SURFACE_VARIANT,
        center_title=True,
    )

    btn_a = ElevatedButton("(A)", on_click=lambda e: handle_button_click('a'), expand=True)
    btn_b = ElevatedButton("(B)", on_click=lambda e: handle_button_click('b'), expand=True)
    btn_c = ElevatedButton("(C)", on_click=lambda e: handle_button_click('c'), expand=True)
    btn_d = ElevatedButton("(D)", on_click=lambda e: handle_button_click('d'), expand=True)

    page.window_width = 800
    page.window_height = 700
    page.appbar = appbar

    chat = ft.ListView(
        expand=True,
        spacing=15,
        auto_scroll=True,
        padding=15,
    )

    page.add(
        ft.Container(
            content=chat,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=5,
            padding=10,
            expand=True,
        ),
        ft.Row(
            controls=[
                btn_a,
                btn_b,
                btn_c,
                btn_d,
            ],
        ),
    )

    score = 0
    correct_answers = 0  # To keep track of correct answers
    questions = [
        {
            "question": "What does PSU stand for?",
            "options": ["power supply unit", "power source unit", "processing supply unit", "powerranger supply unit"],
            "correct_answer": "a"
        },
        {
            "question": "What does HTML stand for?",
            "options": ["Hyper Text Markup Language", "Hyperlinks and Text Markup Language", "Home Tool Markup Language", "Hyper Tool Multi Language"],
            "correct_answer": "a"
        },
        {
            "question": "What is the capital of France?",
            "options": ["Madrid", "Berlin", "Paris", "London"],
            "correct_answer": "c"
        },
        # Add more questions here...
        {
            "question": "What is the largest planet in our solar system?",
            "options": ["Earth", "Jupiter", "Saturn", "Mars"],
            "correct_answer": "b"
        },
        {
            "question": "Which famous scientist is known for the theory of relativity?",
            "options": ["Isaac Newton", "Albert Einstein", "Stephen Hawking", "Galileo Galilei"],
            "correct_answer": "b"
        },
        {
            "question": "Which planet is known as the 'Red Planet'?",
            "options": ["Mars", "Jupiter", "Saturn", "Venus"],
            "correct_answer": "a"
        },
        {
            "question": "What is the purpose of Git?",
            "options": ["Text editing", "Version control", "Database management", "Server hosting"],
            "correct_answer": "b"
        },
        {
            "question": "What language is Flutter developed in?",
            "options": ["Java", "Dart", "Kotlin", "Swift"],
            "correct_answer": "b"
        },
        {
            "question": "What is the most widely used programming language in 2021?",
            "options": ["Python", "JavaScript", "Java", "C++"],
            "correct_answer": "a"
        },
        {
            "question": "What does IDE stand for in the context of programming?",
            "options": ["Integrated Development Environment", "Interactive Data Exchange",
                        "Integrated Design Environment", "Integrated Documentation Environment"],
            "correct_answer": "a"
        },
        {
            "question": "Which programming language is known for its association with machine learning and data science?",
            "options": ["JavaScript", "R", "Swift", "Ruby"],
            "correct_answer": "b"
        },
        {
            "question": "What is the main difference between Python 2.x and Python 3.x?",
            "options": ["Syntax", "Indentation", "Availability of libraries", "Speed"],
            "correct_answer": "a"
        },
        {
            "question": "What is the purpose of the 'elif' keyword in Python?",
            "options": ["Used to indicate an 'else if' condition", "Used to handle exceptions",
                        "Used in loop iterations", "None of the above"],
            "correct_answer": "a"
        },
        {
            "question": "What is the primary function of CSS in web development?",
            "options": ["Structuring content", "Providing interactivity", "Styling presentation",
                        "Handling server-side operations"],
            "correct_answer": "c"
        },
    ]

    max_questions = 14  # Set the maximum number of questions
    questions_answered = -1  # Track the number of questions answered
    time_per_question = 10  # Time limit per question in seconds

    def display_next_question():
        nonlocal questions_answered
        questions_answered += 1

        if questions_answered < max_questions:
            question_no = questions_answered + 1
            chat.controls.append(ft.Text(f'\n{question_no}. {questions[questions_answered]["question"]}'))

            options_text = ""
            for i, option in enumerate(questions[questions_answered]['options'], start=97):
                options_text += f"{chr(i).upper()}). {option}\n"

            chat.controls.append(ft.Text(options_text, size=15))
            page.update()

    def handle_question_timer():
        nonlocal questions_answered
        while questions_answered < max_questions:
            start_time = time.time()
            elapsed_time = 0

            while elapsed_time < time_per_question:
                elapsed_time = time.time() - start_time
                remaining_time = max(0, time_per_question - int(elapsed_time))
                chat.controls.append(ft.Text(f'Time remaining: {remaining_time} seconds'))
                page.update()
                time.sleep(1)

            # Clear timer display after time per question is elapsed
            chat.controls.clear()
            page.update()

            # Move to the next question
            display_next_question()

    threading.Thread(target=handle_question_timer).start()

    for index, question_data in enumerate(questions, start=1):
        if questions_answered == max_questions:  # Check if maximum questions reached
            break

        question_no = index
        chat.controls.append(ft.Text(f'\n{question_no}. {question_data["question"]}'))

        options_text = ""
        for i, option in enumerate(question_data['options'], start=97):
            options_text += f"{chr(i).upper()}). {option}\n"

        chat.controls.append(ft.Text(options_text, size=15))
        page.update()

        def handle_button_click(answer):
            nonlocal score, correct_answers, questions_answered
            if questions_answered == max_questions - 1:  # Check if maximum questions reached
                return

            question_data = questions[questions_answered + 1]  # Retrieve the current question data

            questions_answered += 1  # Increment the questions answered count

            if answer == question_data['correct_answer']:
                score += 1
                correct_answers += 1  # Increment correct answers count
                chat.controls.append(ft.Text('Correct! You got 1 point'))
            else:
                chat.controls.append(ft.Text('Incorrect!'))
                chat.controls.append(ft.Text(f'Correct answer is --> {question_data["correct_answer"]}'))

            if questions_answered == max_questions - 1:  # Check if this was the last question
                display_total_correct_answers()  # Display total correct answers
            else:
                page.update()

        def display_total_correct_answers():
            chat.controls.append(
                ft.Text(f'Total Correct Answers: {correct_answers}/{min(max_questions, len(questions))}'))
            page.update()

        # Display the first question initially
        display_next_question()

        options_text = ""
        for i, option in enumerate(questions[0]['options'], start=97):
            options_text += f"{chr(i).upper()}). {option}\n"

        chat.controls.append(ft.Text(options_text, size=15))
        page.update()

        page.update()

    def display_total_correct_answers():
        chat.controls.append(ft.Text(f'Total Correct Answers: {correct_answers}/{min(max_questions, len(questions))}'))
        page.update()



if __name__ == "__main__":
    ft.app(target=QuizGame)
