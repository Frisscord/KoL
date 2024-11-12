from dip_client import DIPClient
import os
import glob

directory = "output_reden"

files = glob.glob(os.path.join(directory, "*"))

# Iterate over the list and delete each file
for file in files:
    try:
        os.remove(file)
        print(f"Deleted: {file}")
    except Exception as e:
        print(f"Error deleting {file}: {e}")

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

        print("-" * 50)
        print(f"Titel: {protokoll['titel']}")
        print(f"Datum: {protokoll['datum']}")
        print(f"PDF-URL: {protokoll['fundstelle']['pdf_url']}\n")
        print("-" * 50)

    fraktion_name = input("Fraktion eingeben (optional): ")
    redner = input("Redner eingeben (optional): ")

    # Lade Plenarprotokoll und Reden
    protokoll = client.lade_protokoll(document_number, redner_filter=redner, fraktion_filter=fraktion_name)

    if protokoll:
        with open("output_reden/reden.txt", "w", encoding="utf-8") as file:
            for rede in protokoll["reden"]:
                file.write(f"Redner: {rede['redner']} ({rede['fraktion']})\n")
                file.write(f"Inhalt: {rede['inhalt']}\n\n")
        print("Reden wurden gespeichert.")