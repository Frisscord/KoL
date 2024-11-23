import tkinter as tk
from tkinter import ttk, END
import threading
from pgpt_python.client import PrivateGPTApi
import httpx

class UI:
    def __init__(self):
        self.client = PrivateGPTApi(base_url="http://localhost:8001")

        if self.client.health.health().status == 'ok':
            print("pGPT Ist startbereit! Du kannst jetzt Anfragen stellen.")
        else:
            print("pGPT ist nicht startbereit, bitte überprüfe den Server! Das Programm wurde beendet.")
            exit()

        with open(f"output_reden/reden.txt", "rb") as f:
            self.file_doc_id = self.client.ingestion.ingest_file(file=f).data[0].doc_id
            print("Ingested file ID:", self.file_doc_id)

        root = tk.Tk()
        root.title("Bundestagsrede Abfrage")
        root.geometry("800x600")
        root.resizable(False, False)
        root.configure(bg='white')

        frm_quit_btn = tk.Frame(root, bg='lightblue')
        frm_quit_btn.pack(side=tk.BOTTOM, anchor='w', padx=10, pady=10)

        quit_button = tk.Button(frm_quit_btn, text="Quit", command=root.destroy)
        quit_button.pack(side=tk.LEFT)

        quit_button.configure(bg='white')

        # Bind hover events
        quit_button.bind("<Enter>", self.on_enter)
        quit_button.bind("<Leave>", self.on_leave)

        placeholder = 'Stelle eine Frage...'

        frm_question = ttk.Frame(root)
        frm_question.pack(anchor=tk.CENTER, side=tk.BOTTOM)

        entry_width_input = 400
        entry_height_input = 50
        canvas_width_input = entry_width_input + 10
        canvas_height_input = entry_height_input + 10

        canvas_input = tk.Canvas(frm_question, width=canvas_width_input, height=canvas_height_input, bg='white',
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

        self.entry_input = tk.Entry(frm_question, foreground='grey', background='lightgrey', highlightthickness=0,
                            borderwidth=0)
        self.entry_input.insert(0, placeholder)

        canvas_input.create_window(canvas_width_input // 2, canvas_height_input // 2, window=self.entry_input,
                                   width=entry_width_input, height=entry_height_input)

        self.entry_input.bind("<FocusOut>", lambda event: self.add_placeholder(event, placeholder, self.entry_input))
        self.entry_input.bind("<FocusIn>", lambda event: self.remove_placeholder(event, placeholder, self.entry_input))
        self.entry_input.bind('<Return>', lambda event: self.print_input(self.entry_input))

        frm_output = ttk.Frame(root)
        frm_output.pack(anchor=tk.CENTER, side='top', pady=(20, 20), padx=10)

        self.output_text = tk.Text(frm_output, wrap='word', bg='lightgrey', fg='black', width=500, height=500,
                           font=('Arial', 12))
        self.output_text.config(state='disabled')
        self.output_text.pack()

        root.mainloop()

    def add_placeholder(self, event, text, entry_input):
        if entry_input.get() == '':
            entry_input.insert(0, text)
            entry_input.config(foreground='grey')

    def remove_placeholder(self, event, text, entry_input):
        if entry_input.get() == text:
            entry_input.delete(0, tk.END)
            entry_input.config(foreground='black')

    def on_enter(self, event):
        event.widget['background'] = 'lightblue'

    def on_leave(self, event):
        event.widget['background'] = 'white'

    def print_input(self, entry_input):
        input_text = entry_input.get()
        self.entry_input.config(state='disabled')
        self.entry_input.delete(0, tk.END)
        threading.Thread(target=self.send_request, args=(input_text, entry_input,)).start()

    def send_request(self, entry, entry_input):
        try:
            result = self.client.contextual_completions.prompt_completion(
                prompt=entry,
                use_context=True,
                context_filter={"docs_ids": [self.file_doc_id]},
                include_sources=True
            ).choices[0]
            entry_input.config(state='normal')
            self.show_text(result.message.content)
        except httpx.ReadTimeout:
            print("The request timed out. Please try again later.")
            entry_input.config(state='normal')

    def show_text(self, text):
        self.output_text.config(state='normal')
        self.output_text.tag_configure("padded", lmargin1=10, lmargin2=10, rmargin=10)
        self.output_text.insert(END, "AI:    " + text, "padded")
        self.output_text.insert(END, '\n' + "--------------------------------------------------" + '\n')
        self.output_text.config(state='disabled')

if __name__ == "__main__":
    UI()