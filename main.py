#--imports--
from tkinter import *
from tkinter import ttk
from pgpt_python.client import PrivateGPTApi
import PyPDF2
import os
import re

client = PrivateGPTApi(base_url="http://localhost:8001")

def check_client_health():
    if client.health.health().status == 'ok':
        print("pGPT Ist startbereit! Du kannst jetzt Anfragen stellen.")
    else:
        print("pGPT ist nicht startbereit, bitte überprüfe den Server! Das Programm wurde beendet.")
        os._exit(0)


print(client.health.health().status)

check_client_health()

#-----------------------------------------------------------------------------------------------------------------------

#--pdf to txt | Kürzung des Textes--

#--Variablen--

pdf = 'pdf/20182.pdf'
muster = r'\(A\)|\(B\)|\(C\)|\(D\)|Gesamtherstellung:.*?\-8333|\(.*?\)'
output_dir = 'txt/'


def remove_after_period(s):
    s = s.split('.')[0]
    s = s.split('/')[1]
    return s


result = remove_after_period(pdf)


def get_txt(input_pdf, output_dir):
    with open(input_pdf, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page in reader.pages:
            text += page.extract_text() + '\n'
            ergebnis = re.sub(muster, '', text, flags=re.DOTALL)

    # Text in eine .txt-Datei schreiben
    output_txt = os.path.join(output_dir, f'{result}.txt')
    with open(output_txt, 'w', encoding='utf-8') as txt_file:
        txt_file.write(ergebnis)

get_txt(f'pdf/{result}.pdf', output_dir)

print(f"Text wurde in '{os.path.join(output_dir, f'{result}.txt')}' geschrieben.")

#-----------------------------------------------------------------------------------------------------------------------

# --Fenster Einstellungen--
root = Tk()
root.title("Bundestagsrede Abfrage")
root.geometry("800x600")
root.resizable(False, False)
root.configure(bg='white')

#-----------------------------------------------------------------------------------------------------------------------

# --Tk | Funktionen--
def on_enter(e):
    e.widget['background'] = 'lightblue'

def on_leave(e):
    e.widget['background'] = 'SystemButtonFace'

def print_input(event):
    print(entry_input.get())
    entry_input.delete(0, END)

def add_placeholder(event, text):
    if entry_input.get() == '':
        entry_input.insert(0, text)
        entry_input.config(foreground='grey')

def remove_placeholder(event, text):
    if entry_input.get() == text:
        entry_input.delete(0, END)
        entry_input.config(foreground='black')

#-----------------------------------------------------------------------------------------------------------------------

# --Quit Button Frame--
frm_quit_btn = Frame(root, bg='lightblue')
frm_quit_btn.pack(side=BOTTOM, anchor='w', padx=10, pady=10)

quit_button = Button(frm_quit_btn, text="Quit", command=root.destroy)
quit_button.pack(side=LEFT)

quit_button.configure(bg='white')

quit_button.bind("<Enter>", on_enter)
quit_button.bind("<Leave>", on_leave)

#-----------------------------------------------------------------------------------------------------------------------

# --Frage stellen Button--
placeholder = 'Stelle eine Frage...'

frm_question = ttk.Frame(root)
frm_question.pack(anchor=CENTER, side=BOTTOM)



# --Variablen für Eingabefeld Größe--
entry_width_input = 400
entry_height_input = 50
canvas_width_input = entry_width_input + 10
canvas_height_input = entry_height_input + 10

# --Canvas für abgerundete Ecken--
canvas_input = Canvas(frm_question, width=canvas_width_input, height=canvas_height_input, bg='white', highlightthickness=0)
canvas_input.pack()

# --Abgerundetes Rechteck zeichnen--
radius = 15
canvas_input.create_arc((0, 0, radius*2, radius*2), start=90, extent=90, fill='lightgrey', outline='lightgrey')
canvas_input.create_arc((canvas_width_input-radius*2, 0, canvas_width_input, radius*2), start=0, extent=90, fill='lightgrey', outline='lightgrey')
canvas_input.create_arc((0, canvas_height_input-radius*2, radius*2, canvas_height_input), start=180, extent=90, fill='lightgrey', outline='lightgrey')
canvas_input.create_arc((canvas_width_input-radius*2, canvas_height_input-radius*2, canvas_width_input, canvas_height_input), start=270, extent=90, fill='lightgrey', outline='lightgrey')
canvas_input.create_rectangle((radius, 0, canvas_width_input-radius, canvas_height_input), fill='lightgrey', outline='lightgrey')
canvas_input.create_rectangle((0, radius, canvas_width_input, canvas_height_input-radius), fill='lightgrey', outline='lightgrey')

# --Entry Widget auf Canvas platzieren--
entry_input = Entry(frm_question, foreground='black', background='lightgrey', highlightthickness=0, borderwidth=0)
entry_input.insert(0, placeholder)

canvas_input.create_window(canvas_width_input//2, canvas_height_input//2, window=entry_input, width=entry_width_input, height=entry_height_input)

# --Bindings für Frage stellen Button--
entry_input.bind("<FocusOut>", lambda event: add_placeholder(event, placeholder))
entry_input.bind("<FocusIn>", lambda event: remove_placeholder(event, placeholder))
entry_input.bind("<Return>", print_input)

#-----------------------------------------------------------------------------------------------------------------------

# --Output Fenster--
frm_output = ttk.Frame(root)
frm_output.pack(anchor=CENTER, side='top', pady=(100, 20))

# --Variablen für Ausgabe Größe--
canvas_width_output = 600
canvas_height_output = 400

canvas_output = Canvas(frm_output, width=canvas_width_output, height=canvas_height_output, bg='lightgrey', highlightthickness=5)
canvas_output.pack()

#-----------------------------------------------------------------------------------------------------------------------

root.mainloop()