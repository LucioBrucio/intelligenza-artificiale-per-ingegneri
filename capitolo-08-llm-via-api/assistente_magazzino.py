"""Function calling: assistente di magazzino su database SQLite.

Capitolo 8, sezione "Function calling": i due listati della sezione
(funzione + dichiarazione, poi il ciclo di invocazione) assemblati
in un unico programma.
"""

import os
import sqlite3
import sys

from google import genai
from google.genai import types

if not (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")):
    print("Manca la variabile d'ambiente GEMINI_API_KEY: crea una chiave "
          "gratuita su https://aistudio.google.com/apikey e poi esegui "
          "export GEMINI_API_KEY=<la-tua-chiave>")
    sys.exit(1)

MODELLO = "gemini-2.5-flash"
client = genai.Client()


def giacenza_articolo(codice: str) -> dict:
    """Legge la giacenza di un articolo dal database di magazzino."""
    con = sqlite3.connect("magazzino.db")
    riga = con.execute(
        "SELECT descrizione, quantita, ubicazione "
        "FROM giacenze WHERE codice = ?", (codice,)).fetchone()
    con.close()
    if riga is None:
        # errore LEGGIBILE: il modello lo vedra' e potra' reagire
        return {"errore": f"nessun articolo con codice {codice}"}
    return {"descrizione": riga[0],
            "quantita": riga[1],
            "ubicazione": riga[2]}

dichiarazione = types.FunctionDeclaration(
    name="giacenza_articolo",
    description=("Restituisce descrizione, quantita' disponibile e "
                 "ubicazione di un articolo di magazzino dato il codice."),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "codice": types.Schema(
                type=types.Type.STRING,
                description="codice articolo, per esempio VLV-2041"),
        },
        required=["codice"],
    ),
)
strumenti = [types.Tool(function_declarations=[dichiarazione])]

FUNZIONI = {"giacenza_articolo": giacenza_articolo}

def assistente_magazzino(domanda: str) -> str:
    contents = [types.Content(
        role="user", parts=[types.Part.from_text(text=domanda)])]
    config = types.GenerateContentConfig(
        system_instruction=(
            "Sei l'assistente del magazzino. Per qualunque dato di "
            "giacenza usa SEMPRE lo strumento: mai rispondere a memoria."),
        tools=strumenti,
        temperature=0.0,
    )

    while True:
        risposta = client.models.generate_content(
            model=MODELLO, contents=contents, config=config)
        # la risposta (testo O richieste di invocazione) entra in storia
        contents.append(risposta.candidates[0].content)

        if not risposta.function_calls:
            return risposta.text   # nessuna chiamata: e' la risposta finale

        parti = []
        for chiamata in risposta.function_calls:
            funzione = FUNZIONI[chiamata.name]
            try:
                esito = funzione(**chiamata.args)
            except Exception as errore:
                esito = {"errore": str(errore)}
            parti.append(types.Part.from_function_response(
                name=chiamata.name, response=esito))
        contents.append(types.Content(role="user", parts=parti))


def prepara_database() -> None:
    """Crea magazzino.db con il dato di esempio citato nel capitolo."""
    con = sqlite3.connect("magazzino.db")
    con.execute(
        "CREATE TABLE IF NOT EXISTS giacenze ("
        "codice TEXT PRIMARY KEY, descrizione TEXT, "
        "quantita INTEGER, ubicazione TEXT)")
    con.execute(
        "INSERT OR IGNORE INTO giacenze VALUES (?, ?, ?, ?)",
        ("VLV-2041", "valvola a sfera da 2 pollici", 42, "corsia B3"))
    con.commit()
    con.close()


if __name__ == "__main__":
    prepara_database()
    print(assistente_magazzino(
        "Quante VLV-2041 abbiamo, e dove sono?"))
