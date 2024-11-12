import xml.etree.ElementTree as ET
import requests

class DIPClient:
    BASE_URL = "https://search.dip.bundestag.de/api/v1"

    def __init__(self, api_key):
        self.api_key = api_key

    def lade_protokoll(self, dokumentnummer, redner_filter=None, fraktion_filter=None):
        """
        Lädt das Plenarprotokoll einschließlich der Reden basierend auf der Dokumentnummer.
        Optional können Redner und Fraktion gefiltert werden.
        """
        # Abrufen der Metadaten und der XML-URL
        url = f"{self.BASE_URL}/plenarprotokoll"
        params = {
            "apikey": self.api_key,
            "f.dokumentnummer": dokumentnummer,
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            print("Fehler bei der Anfrage:", response.status_code)
            return None

        # Prüfen, ob Dokumente in der Antwort vorhanden sind
        documents = response.json().get("documents")
        if not documents:
            print("Keine Dokumente gefunden.")
            return None

        plenarprotokoll = documents[0]
        xml_url = plenarprotokoll["fundstelle"].get("xml_url")
        if not xml_url:
            print("Keine XML-URL gefunden.")
            return None

        # XML-Inhalt laden und Reden extrahieren
        root = self._get_xml_content(xml_url)
        if not root:
            return None

        reden = self._extract_reden(root, redner_filter, fraktion_filter)
        plenarprotokoll["reden"] = reden
        return plenarprotokoll

    def _get_xml_content(self, xml_url):
        """
        Lädt die XML-Datei von der angegebenen URL und gibt den geparsten Inhalt zurück.
        """
        response = requests.get(xml_url)
        if response.status_code != 200:
            print(f"Fehler beim Laden der XML-Datei: {response.status_code}")
            return None

        try:
            root = ET.fromstring(response.content)
            return root
        except ET.ParseError as e:
            print(f"Fehler beim Parsen der XML-Datei: {e}")
            return None

    def _extract_reden(self, root, redner_filter=None, fraktion_filter=None):
        """
        Extrahiert alle Reden aus dem XML-Dokument und filtert nach Redner und Fraktion.
        """
        reden_liste = []

        for rede in root.findall(".//rede"):
            redner_element = rede.find(".//p[@klasse='redner']")

            if redner_element is not None:
                redner_tag = redner_element.find(".//redner")
                if redner_tag is not None:
                    vorname = redner_tag.findtext(".//vorname", "")
                    nachname = redner_tag.findtext(".//nachname", "")
                    redner = f"{vorname} {nachname}".strip()
                    fraktion = redner_tag.findtext(".//fraktion", "Unbekannte Fraktion")
                else:
                    redner = "Unbekannter Redner"
                    fraktion = "Unbekannte Fraktion"
            else:
                redner = "Unbekannter Redner"
                fraktion = "Unbekannte Fraktion"

            # Rede-Inhalt extrahieren
            rede_inhalt = []
            for absatz in rede.findall(".//p"):
                if absatz.text:
                    rede_inhalt.append(absatz.text.strip())

            # Filter anwenden
            if (not redner_filter or redner_filter in redner) and (not fraktion_filter or fraktion_filter in fraktion):
                reden_liste.append(
                    {
                        "redner": redner,
                        "fraktion": fraktion,
                        "inhalt": " ".join(rede_inhalt),
                    }
                )

        return reden_liste