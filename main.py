from dip_client import DIPClient
from ai_selection import SelectionWindow
import os
import glob
from dotenv import load_dotenv

load_dotenv()

dictionary = "output_reden"


def print_colored_text(text, fg):
    print(f'\x1b[{fg}m{text}\x1b[0m')


files = glob.glob(os.path.join(dictionary, "*"))
for file in files:
    try:
        os.remove(file)
        print_colored_text(f"Gelöscht: {file}", 31)
    except Exception as e:
        print_colored_text(f"Fehler beim Löschen von: {file}: {e}", 31)


def is_file_zero():
    return os.stat("output_reden/reden.txt").st_size == 0


if __name__ == "__main__":
    api_key = os.environ.get("DIP_API_KEY")
    client = DIPClient(api_key)

    document_number = input("\033[33mDokumentnummer eingeben: \033[0m")
    print_colored_text("-" * 50, 34)

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

    fraktion_name = input("\033[33mFraktion eingeben (optional): \033[0m")
    redner = input("\033[33mRedner eingeben (optional): \033[0m")

    # Lade Plenarprotokoll und Reden
    protokoll = client.lade_protokoll(document_number, redner_filter=redner, fraktion_filter=fraktion_name)

    if protokoll:
        with open("output_reden/reden.txt", "w", encoding="utf-8") as file:
            for rede in protokoll["reden"]:
                file.write(f"Redner: {rede['redner']} ({rede['fraktion']})\n")
                file.write(f"Inhalt: {rede['inhalt']}\n\n")
        if is_file_zero():
            print_colored_text("Keine Reden gefunden. Bitte Überprüfen Sie die Eingabe.", 31)
        else:
            print_colored_text("Reden wurden erfolgreich gespeichert.", 32)
            selection_window = SelectionWindow()

