import tkinter as tk
import random
import ctypes
import time
from difflib import SequenceMatcher


#change theme
bg1 = "gray20"
fg1 = "white"
counter = 0
def change_theme():
    global counter
    global fg1
    counter += 1
    backgrounds = ["black", "red", "green","#7b24f4",
                   "blue","orange", "pink","pale green",
                    "aqua", "gray", "gray20"]
    if counter == len(backgrounds):
        counter = 0
    bg1 = backgrounds[counter]
    canvas.configure(bg = bg1)
    prompt_label.configure(bg = bg1, fg = fg1)
    instructions.configure(bg = bg1, fg = fg1)
    wpm_acc.configure(bg=bg1, fg=fg1)

#start and end time
start_time = 0
def timer_start():
    text_entry.delete(0, "end")
    global start_time
    start_time = time.time()

time_elapsed = 0
def timer_end(enterpress):
    global time_elapsed
    end_time = time.time()
    time_elapsed = start_time - end_time
    time_elapsed *= -1
    global input
    input = text_entry.get()
    check_accuracy(input, prompt, time_elapsed)


#window
window = tk.Tk()
window.geometry("1000x500")
window.title("Typing Test")
#improve quality
ctypes.windll.shcore.SetProcessDpiAwareness(1)


#prompts
with open("sentences.txt") as sentences:
    prompts = sentences.readlines()
prompt = ""
def change_prompt(escpress):
    global prompt
    prompt = random.choice(prompts)
    prompt = prompt.replace("\n", "")
    prompt_label.configure(text = prompt)
    timer_start()
    return prompt


#gui
canvas = tk.Canvas(window, bg=bg1)
canvas.place(x=-1, y=-1, width=1000, height=500)
instructions = tk.Label(window, text = "Press ESC to (re)start!\nPress ENTER to stop!",
                        bg = bg1, fg = fg1, font = ("TkMenuFont", 18))
instructions.pack(padx = 10, pady = 20)
prompt_label = tk.Label(window, text = prompt,bg = bg1, fg = fg1, font = ("TkMenuFont", 18))
prompt_label.pack(padx = 10, pady = 20)
text_entry = tk.Entry(window, width = 50, font = ("TkMenuFont", 18))
text_entry.pack(padx = 10, pady = 10)
change_theme = tk.Button(window, text = "Change Theme!",
                         font = ("TkMenuFont", 16), command = change_theme)
change_theme.pack(padx = 10, pady = 10)
wpm_acc = tk.Label(window, text = "",bg = bg1, fg = fg1, font = ("TkMenuFont", 18))
wpm_acc.pack(padx = 10, pady = 20)
window.bind("<Escape>", change_prompt)
window.bind("<Return>", timer_end)


#check accuracy
def check_accuracy(input, prompt, time_elapsed):
    match = SequenceMatcher(None,input, prompt).ratio()
    match *= 100
    match = (str(round(match, 2)))
    words = prompt.split()
    num_of_words = len(words)
    wps = num_of_words / time_elapsed
    wpm = wps * 60
    wps_round = (str(round(wps, 2)))
    wpm_round = (str(round(wpm, 2)))
    wpm_acc.configure(text = f"WPS: {wps_round}\nWPM: {wpm_round}\nAccuracy: {match} %")


#run
window.mainloop()

