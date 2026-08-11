"""Streaming: i token arrivano man mano che il modello li genera.

Capitolo 8, sezione "Streaming e robustezza".
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

flusso = client.models.generate_content_stream(
    model=MODELLO,
    contents="Spiega il colpo d'ariete in un impianto idraulico.",
    config=types.GenerateContentConfig(temperature=0.4),
)

testo_completo = []
for frammento in flusso:
    if frammento.text:                      # alcuni frammenti sono vuoti
        print(frammento.text, end="", flush=True)
        testo_completo.append(frammento.text)

risposta_intera = "".join(testo_completo)   # da salvare nella storia
