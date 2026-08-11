"""Structured output con schema Pydantic e retry con feedback.

Capitolo 8, sezione "Structured output": i due listati della sezione
(schema + chiamata vincolata, poi il pattern completo con retry)
assemblati in un unico programma.
"""

import os
import sys

from google import genai
from google.genai import types
from pydantic import BaseModel, Field, ValidationError

if not (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")):
    print("Manca la variabile d'ambiente GEMINI_API_KEY: crea una chiave "
          "gratuita su https://aistudio.google.com/apikey e poi esegui "
          "export GEMINI_API_KEY=<la-tua-chiave>")
    sys.exit(1)

MODELLO = "gemini-2.5-flash"
client = genai.Client()


class RigaOrdine(BaseModel):
    codice: str = Field(description="codice articolo, es. VLV-2041")
    quantita: int = Field(ge=1)
    prezzo_unitario_eur: float = Field(ge=0)

class Ordine(BaseModel):
    """Schema dell'ordine estratto da una email del cliente."""
    cliente: str
    righe: list[RigaOrdine]
    urgente: bool
    note: str | None = None


# piccolo catalogo di esempio per le regole di business del validatore
CATALOGO = {"VLV-2041"}

MAX_TENTATIVI = 3

def estrai_ordine(testo_email: str) -> Ordine:
    """Estrae un ordine validato, con retry in caso di errore."""
    contents = [f"Estrai l'ordine da questa email:\n\n{testo_email}"]

    for tentativo in range(MAX_TENTATIVI):
        risposta = client.models.generate_content(
            model=MODELLO,
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=0.0,
                response_mime_type="application/json",
                response_schema=Ordine,
            ),
        )
        try:
            ordine = Ordine.model_validate_json(risposta.text)
            # regole di business oltre lo schema
            if not all(r.codice in CATALOGO for r in ordine.righe):
                raise ValueError("codice articolo non a catalogo")
            return ordine
        except (ValidationError, ValueError) as errore:
            # si rimanda indietro l'output errato e l'errore:
            # al tentativo successivo il modello vede il proprio sbaglio
            contents.append(risposta.text)
            contents.append(
                f"L'output precedente non e' valido: {errore}. "
                "Correggilo e restituisci solo il JSON.")

    raise RuntimeError(f"estrazione fallita dopo {MAX_TENTATIVI} tentativi")


if __name__ == "__main__":
    # email di esempio coerente con il caso del capitolo
    testo_email = (
        "Buongiorno,\n"
        "vi chiediamo di spedirci con urgenza 12 valvole codice VLV-2041 "
        "al prezzo concordato di 45,50 euro l'una.\n"
        "Cordiali saluti,\n"
        "Officine Rossi S.r.l."
    )
    ordine = estrai_ordine(testo_email)
    print(ordine.righe[0].codice, ordine.righe[0].quantita)
    print(ordine)
