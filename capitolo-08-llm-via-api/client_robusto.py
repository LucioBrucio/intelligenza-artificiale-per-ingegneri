"""Client robusto: timeout, classificazione degli errori, retry con
backoff esponenziale e jitter, controllo del troncamento, log dei consumi.

Capitolo 8, sezione "Guasti, retry e backoff".
"""

import logging
import os
import random
import sys
import time
from google import genai
from google.genai import errors, types

if not (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")):
    print("Manca la variabile d'ambiente GEMINI_API_KEY: crea una chiave "
          "gratuita su https://aistudio.google.com/apikey e poi esegui "
          "export GEMINI_API_KEY=<la-tua-chiave>")
    sys.exit(1)

MODELLO = "gemini-2.5-flash"      # i nomi dei modelli evolvono
CODICI_TRANSITORI = {429, 500, 502, 503, 504}
log = logging.getLogger("client_llm")

# timeout esplicito: mai attendere all'infinito (valore in ms)
client = genai.Client(
    http_options=types.HttpOptions(timeout=60_000))

def genera(contents, config,
           max_tentativi: int = 5,
           attesa_max: float = 30.0) -> types.GenerateContentResponse:
    """Chiamata con retry, backoff esponenziale e controlli d'esito."""
    for tentativo in range(max_tentativi):
        try:
            risposta = client.models.generate_content(
                model=MODELLO, contents=contents, config=config)

            # risposta arrivata ma tagliata: per noi e' un errore
            motivo = risposta.candidates[0].finish_reason
            if motivo != types.FinishReason.STOP:
                raise RuntimeError(f"generazione interrotta: {motivo}")

            uso = risposta.usage_metadata
            log.info("token input=%s output=%s",
                     uso.prompt_token_count,
                     uso.candidates_token_count)
            return risposta

        except errors.APIError as errore:
            if errore.code not in CODICI_TRANSITORI:
                raise                     # permanente: inutile riprovare
            if tentativo == max_tentativi - 1:
                raise                     # tentativi esauriti
            attesa = min(2 ** tentativo, attesa_max)
            attesa += random.uniform(0, attesa)     # jitter
            log.warning("errore %s, riprovo tra %.1f s",
                        errore.code, attesa)
            time.sleep(attesa)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    risposta = genera(
        contents="Spiega il colpo d'ariete in un impianto idraulico.",
        config=types.GenerateContentConfig(temperature=0.4),
    )
    print(risposta.text)
