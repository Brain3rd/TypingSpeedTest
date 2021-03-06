from tkinter import *
from tkinter import messagebox
import random
import math


BTN_COLOR = "#1e2022"
CANVAS_COLOR = "#dddddd"
BG_COLOR = '#52616b'
FONT_COLOR = '#c9d6df'
GREEN = '#7ea04d'
RED = '#900d0d'


class App:

    def __init__(self, typos):
        # Variables to store chancing information
        self.timer = None
        self.words = typos
        self.words_to_type = self.words.word_list
        self.next_word = None
        self.next_word_list = []
        self.correct_letters = []
        self.letter_typed = []
        self.letters_typed = []
        self.current_letter_list = []
        self.current_type = None
        self.errors = 0
        self.error_words = 0
        self.entry = None

        # Set the starting word
        self.next_word = random.choice(self.words_to_type)
        self.next_word_list.append(self.next_word)

        # Store letters from the word
        split_list = list(self.next_word)
        for letter in split_list:
            self.correct_letters.append(letter)
            self.current_letter_list.append(letter)

        # UI SETUP #
        # Window
        self.window = Tk()
        self.window.title("TTypo 1.0")
        self.window.resizable(width=False, height=False)
        self.window.configure(background=BTN_COLOR)
        self.window.geometry("+700+100")

        # Canvas
        self.canvas = Canvas(width=600, height=300, bg=CANVAS_COLOR)
        self.canvas_text = self.canvas.create_text(
            300, 300,
            text='Click the start button and start writing.\nHit the space bar to reveal next word.',
            width=550, font=('calibre', 20, 'bold'), anchor=S
        )
        self.canvas.grid(row=0, column=0, columnspan=3, sticky="we", pady=(20, 20), padx=(20, 20), ipady=2)

        # Row 1
        self.label_wrong = Label(font=('calibre', 18, 'bold'), bg=BTN_COLOR, fg=RED)
        self.label_wrong.grid(column=1, row=1, sticky="we", pady=(3, 3), padx=(10, 10), ipady=2)
        self.label_errors = Label(text="0 Type Errors", font=('calibre', 12, 'bold'), bg=BTN_COLOR, fg=RED)
        self.label_errors.grid(column=2, row=1, sticky="we", pady=(3, 3), padx=(10, 10), ipady=2)

        # Row 2
        self.label_pre = Label(font=('calibre', 15, 'bold'), bg=BTN_COLOR, fg=FONT_COLOR)
        self.label_pre.config(text='Previous word:')
        self.label_pre.grid(column=0, row=2, sticky="we", pady=(3, 3), padx=(10, 10), ipady=2)
        # This label shows if previously word was correct or not
        self.label_color = Label(font=('calibre', 25, 'bold'), bg=BTN_COLOR, fg=FONT_COLOR)
        self.label_color.config(text='')
        self.label_color.grid(column=1, row=2)
        self.label_errors_2 = Label(text="0 Words Wrong", font=('calibre', 12, 'bold'), bg=BTN_COLOR, fg=RED)
        self.label_errors_2.grid(column=2, row=2, sticky="we", pady=(3, 3), padx=(10, 10), ipady=2)

        # Row 3
        self.label_cur = Label(font=('calibre', 15, 'bold'), bg=BTN_COLOR, fg=FONT_COLOR)
        self.label_cur.config(text='Current word:')
        self.label_cur.grid(column=0, row=3, sticky="we", pady=(3, 3), padx=(10, 10), ipady=2)

        # This label shows next word
        self.label = Label(font=('calibre', 25, 'bold'), bg=BTN_COLOR, fg=FONT_COLOR)
        self.label.config(text=self.next_word)
        self.label.grid(column=1, row=3, sticky="we", pady=(3, 3), padx=(10, 10), ipady=2)
        self.label_timer = Label(text="00:00", font=('calibre', 20, 'bold'), bg=BTN_COLOR, fg=FONT_COLOR)
        self.label_timer.grid(column=2, row=3, sticky="we", pady=(3, 3), padx=(10, 10), ipady=2)

        # Row 4
        self.entry = Entry(justify='center', font=('arial', 25, 'bold'))
        self.entry.bind('<Key>', self.key_pressed)

        # Button
        button = Button(text='Start', font=('arial', 12, 'bold'), command=self.start_timer, bg=BG_COLOR, fg=FONT_COLOR)
        button.grid(column=2, row=4, sticky="we", pady=(3, 3), padx=(10, 10), ipady=2)

        # ABOUT POPUP #
        def about_message():
            messagebox.showinfo(
                "TTypo v1.0", "This app tests your typing speed.\n\n"
                              "Version 1.0 - App check your typos")

        button_about = Button(
            text="About", command=about_message, bg=BG_COLOR, fg=FONT_COLOR, font=('arial', 12, 'bold'))
        button_about.grid(row=4, column=0, sticky="we", ipady=2, pady=(3, 3), padx=(10, 10))

        self.window.mainloop()

    def reset(self):
        self.entry.unbind('<Key>')
        self.entry.grid_remove()
        self.errors = 0
        self.error_words = 0
        self.correct_letters = []
        self.letters_typed = []
        self.next_word_list = [self.next_word]
        # self.current_letter_list = []
        self.label_errors.config(text='0 Type Errors')
        self.label_errors_2.config(text='0 Words Wrong')

    # Countdown timer
    def count_down(self, count):
        # Places input box in screen
        self.entry.grid(column=1, row=4, sticky="we", pady=(3, 3), padx=(10, 10), ipady=2)
        self.entry.bind('<Key>', self.key_pressed)
        # Start counting time
        count_min = math.floor(count / 60)
        count_sec = count % 60
        if count_sec < 10:
            count_sec = f"0{count_sec}"
        # Show time in screen
        self.label_timer.config(text=f"{count_min}:{count_sec}")
        if count > 0:
            self.timer = self.window.after(1000, self.count_down, count - 1)
        # When time is 0 game over
        if count == 0:
            if len(self.correct_letters) > len(self.letters_typed):
                self.letters_typed = self.correct_letters
            self.canvas.itemconfig(
                self.canvas_text, text=f"Time is up.\nYou typing speed was {len(self.next_word_list)} words / min\n"
                                       f"You typed {len(self.letters_typed)} letters following results:\n"
                                       f"{len(self.correct_letters) - self.errors} letters correct.\n"
                                       f"{self.errors} letters wrong\n"
                                       f"{len(self.next_word_list) - self.error_words} words right\n"
                                       f"{self.error_words} words wrong\n")
            self.reset()

    def start_timer(self):
        self.count_down(60)

    def correct_typing(self):
        # Shows
        self.label_color.config(text=self.next_word)

        # Delete clear entry form and current letter lists
        self.entry.delete(0, 'end')
        self.current_letter_list.clear()
        self.letter_typed.clear()

        # Choose next word
        self.next_word = random.choice(self.words_to_type)

        # Put words into canvas
        self.canvas.itemconfig(self.canvas_text, text=self.next_word_list[0:-1])

        # Store next word in list and shows it in label
        self.next_word_list.append(self.next_word)
        self.label.config(text=self.next_word)

        # Store next letters
        letters_joined = ''.join(self.next_word)
        split_list = list(letters_joined)
        for letter in split_list:
            self.correct_letters.append(letter)
            self.current_letter_list.append(letter)

    # This function monitor if keyboard get pressed
    def key_pressed(self, event):

        # Current key pressed
        self.current_type = "" + event.char

        # If user press 'back' key previous letter gets deleted from lists
        if self.current_type == '\x08':
            try:
                self.letter_typed.pop()
                self.letters_typed.pop()
            except IndexError:
                pass
        else:
            # Stores pressed key in letter lists
            if self.current_type != ' ':
                if self.current_type not in self.current_letter_list:
                    self.label_wrong.config(text=f"Letter {self.current_type} is not in {self.next_word}")
                else:
                    self.label_wrong.config(text='')
                self.letter_typed.append(self.current_type)
                self.letters_typed.append(self.current_type)
            if self.current_type == ' ':
                self.label_color.config(fg=GREEN)
                # Monitor if previously typed word was correct, modifies list and give feedback to user
                while len(self.letter_typed) > len(self.current_letter_list):
                    self.letter_typed.pop()
                while len(self.letter_typed) < len(self.current_letter_list):
                    self.letter_typed.append('555')
                for letter in range(len(self.current_letter_list)):
                    if self.letter_typed[letter] != self.current_letter_list[letter]:
                        if self.letter_typed[letter] == '555':
                            pass
                        else:
                            self.errors += 1
                            self.label_wrong.config(text=f"You typed {self.letter_typed[letter]} "
                                                         f"instead of {self.current_letter_list[letter]}")
                            self.label_errors.config(text=f"{self.errors} Type Errors")
                            self.label_color.config(fg=RED)
                if ''.join(self.letter_typed) != self.next_word:
                    self.error_words += 1
                    self.label_errors_2.config(text=f"{self.error_words} Words Wrong")

                self.correct_typing()


class Words:

    with open('data/words.txt') as file:
        words = file.readlines()
        word_list = [word.strip() for word in words]


words = Words()
if __name__ == '__main__':
    App(words)
