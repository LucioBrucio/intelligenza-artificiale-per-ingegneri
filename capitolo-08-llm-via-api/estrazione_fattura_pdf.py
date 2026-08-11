"""Multimodalita': estrazione di dati strutturati da una fattura PDF.

Capitolo 8, sezione "Multimodalita'": input multimodale piu' structured
output, con verifica di coerenza aritmetica a valle.
"""

import os
import sys

from google import genai
from google.genai import types
from pydantic import BaseModel

if not (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")):
    print("Manca la variabile d'ambiente GEMINI_API_KEY: crea una chiave "
          "gratuita su https://aistudio.google.com/apikey e poi esegui "
          "export GEMINI_API_KEY=<la-tua-chiave>")
    sys.exit(1)

MODELLO = "gemini-2.5-flash"
client = genai.Client()


class DatiFattura(BaseModel):
    """Testata di una fattura. I campi dubbi restano None."""
    numero: str | None
    data: str | None            # formato ISO, es. "2026-03-31"
    fornitore: str | None
    imponibile_eur: float | None
    iva_eur: float | None
    totale_eur: float | None


def in_coda_di_revisione(dati: DatiFattura) -> None:
    """Segnaposto: nel sistema reale accoda il documento al controllo umano."""
    print("DOCUMENTO IN CODA DI REVISIONE (dati incompleti o incoerenti):")
    print(dati)


if __name__ == "__main__":
    if not os.path.exists("fattura_1042.pdf"):
        print("File fattura_1042.pdf non trovato: copia nella directory "
              "una fattura PDF con questo nome per provare l'esempio.")
        sys.exit(1)

    with open("fattura_1042.pdf", "rb") as f:
        documento = types.Part.from_bytes(
            data=f.read(), mime_type="application/pdf")

    risposta = client.models.generate_content(
        model=MODELLO,
        contents=[
            documento,
            "Estrai i dati di testata di questa fattura. Se un campo "
            "non e' presente o non e' leggibile con certezza, lascialo "
            "null: MAI dedurlo o inventarlo.",
        ],
        config=types.GenerateContentConfig(
            temperature=0.0,
            response_mime_type="application/json",
            response_schema=DatiFattura,
        ),
    )

    dati = DatiFattura.model_validate_json(risposta.text)
    print(dati)

    # verifica di coerenza aritmetica: un LLM non e' una ALU
    if (None in (dati.imponibile_eur, dati.iva_eur, dati.totale_eur)
            or abs(dati.imponibile_eur + dati.iva_eur
                   - dati.totale_eur) > 0.01):
        in_coda_di_revisione(dati)      # controllo umano, non scarto
