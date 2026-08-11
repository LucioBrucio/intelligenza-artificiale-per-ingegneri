"""La conversazione la mantiene il client: l'API e' stateless.

Capitolo 8, sezione "La conversazione la mantieni tu".
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

storia = []   # la memoria del dialogo: una semplice lista

def chiedi(domanda: str) -> str:
    # 1. accoda la domanda dell'utente alla storia
    storia.append(types.Content(
        role="user",
        parts=[types.Part.from_text(text=domanda)]))

    # 2. invia TUTTA la storia, non solo l'ultimo messaggio
    risposta = client.models.generate_content(
        model=MODELLO,
        contents=storia,
        config=types.GenerateContentConfig(
            system_instruction="Sei un assistente tecnico conciso."),
    )

    # 3. accoda la risposta del modello (ruolo "model")
    storia.append(risposta.candidates[0].content)
    return risposta.text

print(chiedi("Che cos'e' una pompa centrifuga?"))
print(chiedi("E come si calcola la sua prevalenza?"))
