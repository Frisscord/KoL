from tkinter import *
from tkinter import ttk
import threading

class UI:
    def __init__(self):
        root = Tk()
        root.title("Bundestagsrede Abfrage")
        root.geometry("800x600")
        root.resizable(False, False)
        root.configure(bg='white')

        request_in_progress = BooleanVar(value=False)

        frm_quit_btn = Frame(root, bg='lightblue')
        frm_quit_btn.pack(side=BOTTOM, anchor='w', padx=10, pady=10)

        quit_button = Button(frm_quit_btn, text="Quit", command=root.destroy)
        quit_button.pack(side=LEFT)

        quit_button.configure(bg='white')

        placeholder = 'Stelle eine Frage...'

        frm_question = ttk.Frame(root)
        frm_question.pack(anchor=CENTER, side=BOTTOM)

        entry_width_input = 400
        entry_height_input = 50
        canvas_width_input = entry_width_input + 10
        canvas_height_input = entry_height_input + 10

        canvas_input = Canvas(frm_question, width=canvas_width_input, height=canvas_height_input, bg='white',
                              highlightthickness=0)
        canvas_input.pack()

        radius = 15
        canvas_input.create_arc((0, 0, radius * 2, radius * 2), start=90, extent=90, fill='lightgrey',
                                outline='lightgrey')
        canvas_input.create_arc((canvas_width_input - radius * 2, 0, canvas_width_input, radius * 2), start=0,
                                extent=90,
                                fill='lightgrey', outline='lightgrey')
        canvas_input.create_arc((0, canvas_height_input - radius * 2, radius * 2, canvas_height_input), start=180,
                                extent=90,
                                fill='lightgrey', outline='lightgrey')
        canvas_input.create_arc(
            (
            canvas_width_input - radius * 2, canvas_height_input - radius * 2, canvas_width_input, canvas_height_input),
            start=270, extent=90, fill='lightgrey', outline='lightgrey')
        canvas_input.create_rectangle((radius, 0, canvas_width_input - radius, canvas_height_input), fill='lightgrey',
                                      outline='lightgrey')
        canvas_input.create_rectangle((0, radius, canvas_width_input, canvas_height_input - radius), fill='lightgrey',
                                      outline='lightgrey')

        entry_input = Entry(frm_question, foreground='black', background='lightgrey', highlightthickness=0,
                            borderwidth=0)
        entry_input.insert(0, placeholder)

        canvas_input.create_window(canvas_width_input // 2, canvas_height_input // 2, window=entry_input,
                                   width=entry_width_input, height=entry_height_input)

        frm_output = ttk.Frame(root)
        frm_output.pack(anchor=CENTER, side='top', pady=(20, 20), padx=10)

        output_text = Text(frm_output, wrap='word', bg='lightgrey', fg='black', width=500, height=500,
                           font=('Arial', 12))
        output_text.config(state='disabled')
        output_text.pack()

        root.mainloop()