from tkinter import *
from tkinter import ttk

# --Fenster Einstellungen--
root = Tk()
root.title("Bundestagsrede Abfrage")
root.geometry("800x600")
root.resizable(False, False)

# --Funktionen--
def on_enter(e):
    e.widget['background'] = 'lightblue'

def on_leave(e):
    e.widget['background'] = 'SystemButtonFace'

def print_input(event):
    print(entry.get())

def add_placeholder(event, text):
    if entry.get() == '':
        entry.insert(0, text)
        entry.config(foreground='grey')

def remove_placeholder(event, text):
    if entry.get() == text:
        entry.delete(0, END)
        entry.config(foreground='black')

# --Quit Button--
frm_quit_btn = ttk.Frame(root, padding=10)
frm_quit_btn.pack(side=BOTTOM, anchor='w')

quit_button = Button(frm_quit_btn, text="Quit", command=root.destroy)
quit_button.pack(side=LEFT)

quit_button.bind("<Enter>", on_enter)
quit_button.bind("<Leave>", on_leave)

# --Frage stellen Button--
placeholder = 'Stelle eine Frage...'

frm_question = ttk.Frame(root)
frm_question.pack(anchor=CENTER, side=BOTTOM)

# --Variablen für Eingabefeld Größe--
entry_width = 400
entry_height = 50
canvas_width = entry_width + 10
canvas_height = entry_height + 10

# --Canvas für abgerundete Ecken--
canvas = Canvas(frm_question, width=canvas_width, height=canvas_height, bg='white', highlightthickness=0)
canvas.pack()

# --Abgerundetes Rechteck zeichnen--
radius = 15
canvas.create_arc((0, 0, radius*2, radius*2), start=90, extent=90, fill='lightgrey', outline='lightgrey')
canvas.create_arc((canvas_width-radius*2, 0, canvas_width, radius*2), start=0, extent=90, fill='lightgrey', outline='lightgrey')
canvas.create_arc((0, canvas_height-radius*2, radius*2, canvas_height), start=180, extent=90, fill='lightgrey', outline='lightgrey')
canvas.create_arc((canvas_width-radius*2, canvas_height-radius*2, canvas_width, canvas_height), start=270, extent=90, fill='lightgrey', outline='lightgrey')
canvas.create_rectangle((radius, 0, canvas_width-radius, canvas_height), fill='lightgrey', outline='lightgrey')
canvas.create_rectangle((0, radius, canvas_width, canvas_height-radius), fill='lightgrey', outline='lightgrey')

# --Entry Widget auf Canvas platzieren--
entry = Entry(frm_question, foreground='grey', background='lightgrey', highlightthickness=0, borderwidth=0)
entry.insert(0, placeholder)

canvas.create_window(canvas_width//2, canvas_height//2, window=entry, width=entry_width, height=entry_height)

# --Bindings für Frage stellen Button--
entry.bind("<FocusOut>", lambda event: add_placeholder(event, placeholder))
entry.bind("<FocusIn>", lambda event: remove_placeholder(event, placeholder))
entry.bind("<Return>", print_input)

root.mainloop()