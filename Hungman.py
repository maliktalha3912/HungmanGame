import tkinter as tk
import random

WORDS = ['python', 'hangman', 'challenge', 'programming', 'developer', 'interface', 'keyboard']
MAX_GUESSES = 6

class HangmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        self.root.geometry("600x600")
        self.root.config(bg="lightblue")

        self.word = random.choice(WORDS)
        self.guessed_letters = set()
        self.incorrect_guesses = 0

        self.create_widgets()
        self.draw_word()
        self.draw_hangman()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=300, height=300, bg='white')
        self.canvas.pack(pady=10)

        self.word_label = tk.Label(self.root, text='', font=('Helvetica', 24), bg='lightblue')
        self.word_label.pack(pady=5)

        self.guessed_label = tk.Label(self.root, text='Guessed Letters: ', font=('Helvetica', 14), bg='lightblue')
        self.guessed_label.pack(pady=5)

        self.buttons_frame = tk.Frame(self.root, bg='lightblue')
        self.buttons_frame.pack()

        self.buttons = {}
        for i, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            btn = tk.Button(self.buttons_frame, text=letter, width=4, height=2,
                            command=lambda l=letter: self.guess_letter(l))
            btn.grid(row=i // 9, column=i % 9, padx=2, pady=2)
            self.buttons[letter] = btn

        self.result_label = tk.Label(self.root, text='', font=('Helvetica', 16), bg='lightblue')
        self.result_label.pack(pady=10)

        # Always-visible Retry button
        self.retry_button = tk.Button(self.root, text="🔁 Retry Game", font=('Arial', 14), command=self.restart_game, bg='#f0f0f0')
        self.retry_button.pack(pady=10)

    def draw_word(self):
        display = [letter.upper() if letter in self.guessed_letters else '_' for letter in self.word]
        self.word_label.config(text=' '.join(display))
        self.guessed_label.config(text="Guessed Letters: " + ' '.join(sorted(self.guessed_letters)).upper())

    def draw_hangman(self):
        self.canvas.delete("all")
        # Base
        self.canvas.create_line(20, 280, 280, 280)
        self.canvas.create_line(60, 280, 60, 50)
        self.canvas.create_line(60, 50, 180, 50)
        self.canvas.create_line(180, 50, 180, 80)

        if self.incorrect_guesses > 0:
            self.canvas.create_oval(160, 80, 200, 120)  # Head
        if self.incorrect_guesses > 1:
            self.canvas.create_line(180, 120, 180, 190)  # Body
        if self.incorrect_guesses > 2:
            self.canvas.create_line(180, 140, 150, 160)  # Left Arm
        if self.incorrect_guesses > 3:
            self.canvas.create_line(180, 140, 210, 160)  # Right Arm
        if self.incorrect_guesses > 4:
            self.canvas.create_line(180, 190, 150, 230)  # Left Leg
        if self.incorrect_guesses > 5:
            self.canvas.create_line(180, 190, 210, 230)  # Right Leg

    def guess_letter(self, letter):
        letter = letter.lower()
        self.buttons[letter.upper()].config(state='disabled')

        self.guessed_letters.add(letter)
        if letter not in self.word:
            self.incorrect_guesses += 1

        self.draw_word()
        self.draw_hangman()
        self.check_game_over()

    def check_game_over(self):
        if all(letter in self.guessed_letters for letter in self.word):
            self.end_game(won=True)
        elif self.incorrect_guesses >= MAX_GUESSES:
            self.end_game(won=False)

    def end_game(self, won):
        for btn in self.buttons.values():
            btn.config(state='disabled')

        if won:
            self.root.config(bg='#d4fcd4')  # Celebration green
            self.canvas.config(bg='#d4fcd4')
            self.word_label.config(bg='#d4fcd4')
            self.guessed_label.config(bg='#d4fcd4')
            self.buttons_frame.config(bg='#d4fcd4')

            self.result_label.config(
                text="🎉 Congratulations! You Guessed the Word! 🎉",
                fg='green',
                bg='#d4fcd4',
                font=('Helvetica', 18, 'bold')
            )
        else:
            self.result_label.config(
                text=f"😢 You Lost! The word was: {self.word.upper()}",
                fg='red',
                bg='lightblue',
                font=('Helvetica', 16)
            )

    def restart_game(self):
        self.word = random.choice(WORDS)
        self.guessed_letters.clear()
        self.incorrect_guesses = 0

        # Reset all visuals
        self.root.config(bg='lightblue')
        self.canvas.config(bg='white')
        self.word_label.config(bg='lightblue')
        self.guessed_label.config(bg='lightblue')
        self.buttons_frame.config(bg='lightblue')
        self.result_label.config(text='', bg='lightblue')

        for btn in self.buttons.values():
            btn.config(state='normal')

        self.draw_word()
        self.draw_hangman()

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    app = HangmanGUI(root)
    root.mainloop()
