"""Prompt caching esplicito con l'SDK di Google (google-genai).

Listato del capitolo 9, sezione "Prompt caching": il prefisso stabile
(istruzioni e documentazione di prodotto) viene caricato nella cache una
volta sola con una durata di vita esplicita, e ogni richiesta successiva
paga a prezzo pieno solo i token nuovi. Richiede la variabile d'ambiente
GOOGLE_API_KEY.
"""

import os
import sys

if not (os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")):
    print("Variabile d'ambiente GOOGLE_API_KEY mancante: crea una chiave su")
    print("https://aistudio.google.com/apikey e poi esegui:")
    print('  export GOOGLE_API_KEY="la-tua-chiave"')
    sys.exit(1)

from google import genai
from google.genai import types

# I nomi dei modelli evolvono: verificare il listino corrente.
MODELLO = "gemini-2.5-flash"

# Dati di esempio: il contesto stabile dell'assistente di supporto tecnico
# descritto nel testo. Nella pratica la documentazione e' un estratto lungo:
# la cache conviene sui prefissi lunghi e caldi, e i provider richiedono una
# dimensione minima del contenuto per crearla.
istruzioni_stabili = (
    "Sei l'assistente di supporto tecnico di un produttore di componenti "
    "industriali. Rispondi solo sulla base della documentazione fornita; "
    "se un'informazione non e' presente, dillo esplicitamente."
)
documentazione_prodotto = (
    "Pompa centrifuga CP-40. Portata massima: 40 m3/h. Prevalenza "
    "massima: 32 m. Attacco flangiato DN 50. Manutenzione ordinaria: "
    "controllo della tenuta meccanica ogni 2000 ore di esercizio."
)
domanda_utente = "Ogni quante ore va controllata la tenuta della CP-40?"

client = genai.Client()

# Il prefisso stabile viene caricato nella cache una volta sola,
# con una durata di vita esplicita.
cache = client.caches.create(
    model=MODELLO,
    config=types.CreateCachedContentConfig(
        system_instruction=istruzioni_stabili,
        contents=[documentazione_prodotto],
        ttl="3600s",   # un'ora di validita'
    ),
)

# Ogni richiesta paga a prezzo pieno solo i token nuovi.
risposta = client.models.generate_content(
    model=MODELLO,
    contents=domanda_utente,
    config=types.GenerateContentConfig(cached_content=cache.name),
)

print(risposta.text)
