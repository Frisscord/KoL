import tkinter as tk
from ui import UI

class SelectionWindow:
    def __init__(self):

        self.root = tk.Tk()
        self.root.title("AI Selection")
        self.root.geometry("300x150")
        self.root.resizable(False, False)
        self.root.configure(bg='white')

        self.selection = tk.StringVar()
        self.selection.set("Option 1")

        self.option1 = tk.Radiobutton(self.root, text="PrivateGPT", variable=self.selection, value="pgpt", font=("Arial", 14), bg="white")
        self.option1.pack(anchor=tk.W)

        self.option2 = tk.Radiobutton(self.root, text="Groq", variable=self.selection, value="groq", font=("Arial", 14), bg="white")
        self.option2.pack(anchor=tk.W)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit, font=("Arial", 14))

        self.submit_button.bind("<Enter>", self.on_enter)
        self.submit_button.bind("<Leave>", self.on_leave)

        self.submit_button.pack()

        self.root.mainloop()

    def submit(self):
        selected_option = self.selection.get()
        self.root.destroy()
        ui = UI(selected_option)


    def on_enter(self, event):
        event.widget['background'] = 'lightblue'

    def on_leave(self, event):
        event.widget['background'] = 'white'

if __name__ == "__main__":
    SelectionWindow()
