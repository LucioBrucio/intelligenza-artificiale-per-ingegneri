"""I parametri di generazione viaggiano nella configurazione della chiamata.

Capitolo 8, sezione "Parametri di generazione".
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

config = types.GenerateContentConfig(
    temperature=0.2,          # compito con risposta "giusta"
    top_p=0.95,
    max_output_tokens=1024,   # tetto di sicurezza su costi e latenza
    stop_sequences=["FINE"],  # arresto anticipato opzionale
    # per i modelli di reasoning: quanto "pensiero" concedere
    thinking_config=types.ThinkingConfig(thinking_budget=0),
)

if __name__ == "__main__":
    risposta = client.models.generate_content(
        model=MODELLO,
        contents="Spiega in due frasi la differenza tra processo e thread.",
        config=config,
    )
    print(risposta.text)
