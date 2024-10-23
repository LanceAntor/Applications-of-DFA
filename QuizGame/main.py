import tkinter as tk
from tkinter import messagebox, ttk
from ttkbootstrap import Style
from quiz_questions import quiz_data  
import random

class QuizGameFSM:
    def __init__(self, root):
        self.root = root
        self.current_state = None  # Track the current state of the game
        self.category = None
        self.current_question = 0
        self.score = 0
        self.lives = 3  # Start with 3 lives
        self.questions = []
        
        # Setup styles
        self.style = Style(theme="flatly")
        self.style.configure("Quiz.TButton", font=("Arial", 12))

        # Start with the start screen state
        self.transition_to("StartScreen")

    def transition_to(self, state):
        """Transition to a new state."""
        self.current_state = state
        self.clear_screen()

        if state == "StartScreen":
            self.show_start_screen()
        elif state == "QuestionDisplay":
            self.show_question_screen()
        elif state == "EndGame":
            self.end_game()

    def clear_screen(self):
        """Remove all widgets from the current screen."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_start_screen(self):
        """Show the category selection screen."""
        self.root.title("Quiz Game")
        self.root.geometry("600x500")

        title_label = ttk.Label(
            self.root,
            text="Quiz Game",
            font=("Arial", 24)
        )
        title_label.pack(pady=40)

        category_label = ttk.Label(
            self.root,
            text="Choose a category:",
            font=("Arial", 16)
        )
        category_label.pack(pady=20)

        categories = list(quiz_data.keys())
        for category in categories:
            button = ttk.Button(
                self.root,
                text=category,
                command=lambda c=category: self.start_quiz(c),
                style="Quiz.TButton",
                width=20
            )
            button.pack(pady=10)

    def start_quiz(self, category):
        """Start the quiz for the selected category."""
        self.category = category
        self.questions = quiz_data[self.category]
        random.shuffle(self.questions)
        self.current_question = 0
        self.score = 0
        self.lives = 3
        self.transition_to("QuestionDisplay")

    def show_question_screen(self):
        """Display the current question and answer options."""
        if self.current_question >= len(self.questions):
            self.transition_to("EndGame")
            return

        question = self.questions[self.current_question]

        self.q_label = ttk.Label(
            self.root,
            anchor="center",
            wraplength=500,
            padding=10,
            font=("Arial", 18)
        )
        self.q_label.pack(pady=10)
        self.q_label.config(text=question["question"])
        
        self.choice_btns = []
        for i in range(4):
            button = ttk.Button(
                self.root,
                text=question["choices"][i],
                command=lambda i=i: self.check_answer(i),
                style="Quiz.TButton",
                width=10
            )
            button.pack(pady=10)
            self.choice_btns.append(button)

        self.feedback_label = ttk.Label(
            self.root,
            anchor="center",
            padding=10,
            font=("Arial", 16),
            foreground="red"
        )
        self.feedback_label.pack(pady=5)

        self.correct_answer_label = ttk.Label(
            self.root,
            anchor="center",
            padding=10,
            font=("Arial", 14),
            foreground="green"
        )
        self.correct_answer_label.pack(pady=1)

        self.lives_label = ttk.Label(
            self.root,
            text=f"Lives: {'❤️' * self.lives}",
            font=("Arial", 14),
            foreground="red"
        )
        self.lives_label.pack(pady=5)

        self.next_btn = ttk.Button(
            self.root,
            text="Next",
            command=self.next_question,
            state="disabled",
            style="Quiz.TButton"
        )
        self.next_btn.pack(pady=10)

    def check_answer(self, choice):
        """Check the user's selected answer and show feedback."""
        question = self.questions[self.current_question]
        selected_choice = self.choice_btns[choice].cget("text")

        if selected_choice == question["answer"]:
            self.score += 1
            self.feedback_label.configure(text="Correct!", foreground="green")
        else:
            self.lives -= 1
            self.lives_label.config(text=f"Lives: {'❤️' * self.lives}") 
            self.feedback_label.configure(text="Incorrect!", foreground="red")
            self.correct_answer_label.configure(text=f"The correct answer is: {question['answer']}", foreground="green")

        # Disable all buttons after an answer is selected
        for button in self.choice_btns:
            button.configure(state="disabled")

        # Enable the "Next" button to allow moving to the next question
        self.next_btn.configure(state="normal")

        if self.lives == 0:
            self.transition_to("EndGame")

    def next_question(self):
        """Proceed to the next question or end the game."""
        self.current_question += 1
        if self.lives > 0 and self.current_question < len(self.questions):
            self.transition_to("QuestionDisplay")
        else:
            self.transition_to("EndGame")

    def end_game(self):
        """End the game and display the final score."""
        messagebox.showinfo("Game Over", f"Your score is: {self.score}/{len(self.questions)}")
        self.transition_to("StartScreen")


if __name__ == "__main__":
    root = tk.Tk()
    game_fsm = QuizGameFSM(root)
    root.mainloop()
