from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
random_choice = {}
data = pandas.read_csv("french_words.csv")
new_data = data.to_dict(orient="records")
to_learn = {}
try:
    data = pandas.read_csv("words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

print(to_learn)
windows = Tk()
windows.config(bg=BACKGROUND_COLOR, padx=50, pady=50)


def flip_card():
    global random_choice
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=random_choice["English"], fill="white")
    canvas.itemconfig(card_bg, image=card_back)


def next_card():
    global random_choice, flip_timer
    windows.after_cancel(flip_timer)
    random_choice = random.choice(new_data)
    random_fr_word = random_choice["French"]
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=random_fr_word, fill="black")
    canvas.itemconfig(card_bg, image=card_front)
    flip_timer = windows.after(3000, func=flip_card)


def is_known():
    to_learn.remove(random_choice)
    data = pandas.DataFrame(to_learn)
    data.to_csv("words_to_learn.csv", index=False)
    next_card()


flip_timer = windows.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front = PhotoImage(file="card_front.png")
card_back = PhotoImage(file="card_back.png")
card_bg = canvas.create_image(400, 263, image=card_front)
card_title = canvas.create_text(400, 152, text="", font=("Arial", 30, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 50, "bold"))
canvas.grid(row=1, column=1)

wrong_image = PhotoImage(file="wrong.png")
wrong = Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong.grid(column=0, row=3)

right_image = PhotoImage(file="right.png", )
right = Button(image=right_image, highlightthickness=0, command=is_known)
right.grid(column=2, row=3)
next_card()

windows.mainloop()
