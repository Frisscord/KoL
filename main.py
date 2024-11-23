from dip_client import DIPClient
from ui import UI
import os
import glob

directory = "output_reden"

def print_colored_text(text, fg):
    print(f'\x1b[{fg}m{text}\x1b[0m')

files = glob.glob(os.path.join(directory, "*"))
for file in files:
    try:
        os.remove(file)
        print_colored_text(f"Deleted: {file}", 31)
    except Exception as e:
        print(f"Error deleting {file}: {e}")
def is_non_zero_file():
    return os.stat("output_reden/reden.txt").st_size == 0

if __name__ == "__main__":
    api_key = "I9FKdCn.hbfefNWCY336dL6x62vfwNKpoN2RZ1gp21"
    client = DIPClient(api_key)

    document_number = input("Dokumentnummer eingeben: ")
    print("-" * 50)

    fraktion_name = ""
    redner = ""

    protokoll = client.lade_protokoll(document_number, redner_filter=redner, fraktion_filter=fraktion_name)
    if protokoll:
        for rede in protokoll["reden"]:
            print(f"Redner: {rede['redner']} ({rede['fraktion']})")

        print_colored_text("-" * 50,34)
        print_colored_text(f"Titel: {protokoll['titel']}", 34)
        print_colored_text(f"Datum: {protokoll['datum']}", 34)
        print_colored_text(f"PDF-URL: {protokoll['fundstelle']['pdf_url']}\n", 34)
        print_colored_text("-" * 50, 34)
    else:
        exit()

    fraktion_name = input("Fraktion eingeben (optional): ")
    redner = input("Redner eingeben (optional): ")

    # Lade Plenarprotokoll und Reden
    protokoll = client.lade_protokoll(document_number, redner_filter=redner, fraktion_filter=fraktion_name)

    if protokoll:
        with open("output_reden/reden.txt", "w", encoding="utf-8") as file:
            for rede in protokoll["reden"]:
                file.write(f"Redner: {rede['redner']} ({rede['fraktion']})\n")
                file.write(f"Inhalt: {rede['inhalt']}\n\n")
        if is_non_zero_file():
            print_colored_text("Reden keine gefunden. Bitte Überprüfen Sie die Eingabe.", 31)
        else:
            print_colored_text("Reden wurden erfolgreich gespeichert.", 32)
            client = UI()

