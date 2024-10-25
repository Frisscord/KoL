import threading
from tkinter import *
from tkinter import ttk
from pgpt_python.client import PrivateGPTApi
import os
import re
import PyPDF2

pdf = 'pdf/beispiel.pdf'
output_dir = 'txt/'

# -----------------------------------------------------------------------------------------------------------------------

client = PrivateGPTApi(base_url="http://localhost:8001")
muster = r'\(A\)|\(B\)|\(C\)|\(D\)|Gesamtherstellung:.*?\-8333|\(.*?\)'

# -----------------------------------------------------------------------------------------------------------------------

response_words = []

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

    output_txt = os.path.join(output_dir, f'{result}.txt')
    with open(output_txt, 'w', encoding='utf-8') as txt_file:
        txt_file.write(ergebnis)


get_txt(pdf, output_dir)
print(f"Text wurde in '{os.path.join(output_dir, f'{result}.txt')}' geschrieben.")

with open(f"txt/{result}.txt", "rb") as f:
    file_doc_id = client.ingestion.ingest_file(file=f).data[0].doc_id
    print("Ingested file ID:", file_doc_id)

def check_client_health():
    if client.health.health().status == 'ok':
        print("pGPT Ist startbereit! Du kannst jetzt Anfragen stellen.")
    else:
        print("pGPT ist nicht startbereit, bitte überprüfe den Server! Das Programm wurde beendet.")
        os._exit(0)


def insert_text(text):
    output_text.config(state='normal')
    output_text.tag_configure("padded", lmargin1=10, lmargin2=10, rmargin=10)
    output_text.insert(END, "AI:    " + text, "padded")
    output_text.insert(END, '\n' + "--------------------------------------------------" + '\n')
    output_text.config(state='disabled')
    response_words.clear()

def on_enter(e):
    e.widget['background'] = 'lightblue'


def on_leave(e):
    e.widget['background'] = 'SystemButtonFace'


def print_input(event):
    if not request_in_progress.get():
        entry = entry_input.get()
        entry_input.config(state='disabled', disabledbackground='lightgrey')
        request_in_progress.set(True)
        threading.Thread(target=send_input, args=(entry,)).start()
        entry_input.delete(0, END)


def send_input(entry):
    result = client.contextual_completions.prompt_completion(
        prompt=entry,
        use_context=True,
        context_filter={"docs_ids": [file_doc_id]},
        include_sources=True,
    ).choices[0]
    print(result.message.content)
    print(f" # Source: {result.sources[0].document.doc_metadata['file_name']}")
    result = result.message.content



    entry_input.config(state='normal')
    request_in_progress.set(False)
    insert_text(result)


def add_placeholder(event, text):
    if entry_input.get() == '':
        entry_input.insert(0, text)
        entry_input.config(foreground='grey')


def remove_placeholder(event, text):
    if entry_input.get() == text:
        entry_input.delete(0, END)
        entry_input.config(foreground='black')




check_client_health()
# -----------------------------------------------------------------------------------------------------------------------

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

quit_button.bind("<Enter>", on_enter)
quit_button.bind("<Leave>", on_leave)

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
canvas_input.create_arc((0, 0, radius * 2, radius * 2), start=90, extent=90, fill='lightgrey', outline='lightgrey')
canvas_input.create_arc((canvas_width_input - radius * 2, 0, canvas_width_input, radius * 2), start=0, extent=90,
                        fill='lightgrey', outline='lightgrey')
canvas_input.create_arc((0, canvas_height_input - radius * 2, radius * 2, canvas_height_input), start=180, extent=90,
                        fill='lightgrey', outline='lightgrey')
canvas_input.create_arc(
    (canvas_width_input - radius * 2, canvas_height_input - radius * 2, canvas_width_input, canvas_height_input),
    start=270, extent=90, fill='lightgrey', outline='lightgrey')
canvas_input.create_rectangle((radius, 0, canvas_width_input - radius, canvas_height_input), fill='lightgrey',
                              outline='lightgrey')
canvas_input.create_rectangle((0, radius, canvas_width_input, canvas_height_input - radius), fill='lightgrey',
                              outline='lightgrey')

entry_input = Entry(frm_question, foreground='black', background='lightgrey', highlightthickness=0, borderwidth=0)
entry_input.insert(0, placeholder)

canvas_input.create_window(canvas_width_input // 2, canvas_height_input // 2, window=entry_input,
                           width=entry_width_input, height=entry_height_input)

entry_input.bind("<FocusOut>", lambda event: add_placeholder(event, placeholder))
entry_input.bind("<FocusIn>", lambda event: remove_placeholder(event, placeholder))
entry_input.bind("<Return>", print_input)

frm_output = ttk.Frame(root)
frm_output.pack(anchor=CENTER, side='top', pady=(20, 20), padx=10)

output_text = Text(frm_output, wrap='word', bg='lightgrey', fg='black', width=500, height=500, font=('Arial', 12))
output_text.config(state='disabled')
output_text.pack()

# -----------------------------------------------------------------------------------------------------------------------

root.mainloop()