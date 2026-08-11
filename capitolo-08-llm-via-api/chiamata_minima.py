"""Chiamata minima completa a un LLM via API.

Capitolo 8, sezione "Anatomia di una chiamata".
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

# I nomi dei modelli evolvono di mese in mese: vanno tenuti
# in UNA costante di configurazione, non sparsi nel codice.
MODELLO = "gemini-2.5-flash"

# Il client legge la chiave dalla variabile d'ambiente GEMINI_API_KEY.
# Su Vertex AI: genai.Client(vertexai=True, project="...", location="...")
client = genai.Client()

risposta = client.models.generate_content(
    model=MODELLO,
    contents="Spiega in due frasi la differenza tra processo e thread.",
    config=types.GenerateContentConfig(
        system_instruction=(
            "Sei un assistente tecnico per ingegneri del software. "
            "Rispondi in italiano, in modo conciso."
        ),
        temperature=0.3,
    ),
)

print(risposta.text)              # il testo della risposta
print(risposta.usage_metadata)    # token di input e di output
