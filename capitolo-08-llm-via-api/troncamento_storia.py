"""Troncamento della storia: il context window come risorsa da amministrare.

Capitolo 8, sezione "Il context window come risorsa".
"""

import os
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

SOGLIA_TOKEN = 50_000   # budget che ci imponiamo, non il limite del modello

def tronca_storia(storia: list) -> list:
    """Scarta i turni piu' vecchi finche' la storia rientra nel budget.

    Rimuove i messaggi a coppie (domanda + risposta) per non
    lasciare la conversazione con un turno spaiato.
    """
    while len(storia) > 2:
        conteggio = client.models.count_tokens(
            model=MODELLO, contents=storia)
        if conteggio.total_tokens <= SOGLIA_TOKEN:
            break
        del storia[0:2]   # elimina lo scambio piu' vecchio
    return storia


if __name__ == "__main__":
    # piccola storia di esempio per vedere la funzione all'opera
    scambi = [
        ("Che cos'e' una pompa centrifuga?",
         "E' una macchina che trasferisce energia a un liquido "
         "tramite una girante in rotazione."),
        ("E come si calcola la sua prevalenza?",
         "Dalla differenza di carico totale tra mandata e aspirazione."),
    ]
    storia = []
    for domanda, risposta in scambi:
        storia.append(types.Content(
            role="user", parts=[types.Part.from_text(text=domanda)]))
        storia.append(types.Content(
            role="model", parts=[types.Part.from_text(text=risposta)]))

    storia = tronca_storia(storia)
    conteggio = client.models.count_tokens(model=MODELLO, contents=storia)
    print(f"messaggi in storia: {len(storia)}, "
          f"token totali: {conteggio.total_tokens} "
          f"(budget: {SOGLIA_TOKEN})")
