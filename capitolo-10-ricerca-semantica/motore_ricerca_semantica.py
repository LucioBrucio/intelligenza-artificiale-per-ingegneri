"""Motore di ricerca semantica del capitolo 10.

Configurazione e corpus (listato 10.3), motore con indicizzazione e
ricerca esatta con NumPy (listato 10.4), insieme di valutazione e
misura del recall (listato 10.5).

Tutto gira in locale con sentence-transformers: al primo avvio il
modello viene scaricato da Hugging Face (serve la connessione).
"""

from sentence_transformers import SentenceTransformer
import numpy as np

# I nomi dei modelli evolvono: verificare il catalogo aggiornato.
MODELLO_EMBEDDING = "paraphrase-multilingual-MiniLM-L12-v2"

CORPUS = [
    {"id": "garanzia-durata", "tema": "garanzia", "testo":
     "La garanzia copre i difetti di fabbricazione per 24 mesi "
     "dalla data di acquisto."},
    {"id": "garanzia-esclusioni", "tema": "garanzia", "testo":
     "La garanzia non copre i danni causati da uso improprio, "
     "urti, contatto con liquidi o riparazioni non autorizzate."},
    {"id": "reso", "tema": "garanzia", "testo":
     "Il diritto di recesso si esercita entro 14 giorni dalla "
     "consegna, tramite il modulo online."},
    {"id": "avvio", "tema": "hardware", "testo":
     "Se il notebook non da' segni di vita, scollegare batteria "
     "e alimentatore, attendere un minuto e ricollegarli."},
    {"id": "firmware-agg", "tema": "software", "testo":
     "Per aggiornare il firmware scaricare il pacchetto dal sito "
     "del produttore e seguire la procedura guidata."},
    {"id": "firmware-e4013", "tema": "software", "testo":
     "L'errore E-4013 durante l'aggiornamento firmware indica un "
     "pacchetto corrotto: scaricare di nuovo il file e ripetere."},
    {"id": "password", "tema": "account", "testo":
     "Per reimpostare la password usare il collegamento 'recupera "
     "credenziali' nella pagina di accesso."},
    {"id": "assistenza", "tema": "account", "testo":
     "L'assistenza telefonica risponde dal lunedi' al venerdi', "
     "dalle 9 alle 18."},
]


class MotoreRicerca:
    def __init__(self):
        self.modello = SentenceTransformer(MODELLO_EMBEDDING)
        self.chunk = []
        self.M = None          # matrice (n_chunk, 384)

    def indicizza(self, documenti):
        self.chunk = documenti
        testi = [d["testo"] for d in documenti]
        # normalize_embeddings=True: prodotto scalare = coseno
        self.M = self.modello.encode(
            testi, normalize_embeddings=True)

    def cerca(self, query, k=3):
        q = self.modello.encode(
            query, normalize_embeddings=True)
        punteggi = self.M @ q            # una similarita' per chunk
        migliori = np.argsort(-punteggi)[:k]
        return [(self.chunk[i]["id"], float(punteggi[i]))
                for i in migliori]


motore = MotoreRicerca()
motore.indicizza(CORPUS)

PROVE = [
    ("quanto dura la garanzia?",             "garanzia-durata"),
    ("il portatile non si accende",          "avvio"),
    ("ho dimenticato le credenziali",        "password"),
    ("errore E-4013",                        "firmware-e4013"),
    ("come restituisco il prodotto?",        "reso"),
    ("la garanzia copre i danni da liquidi?","garanzia-esclusioni"),
]


def recall_a_k(motore, prove, k):
    centrati = 0
    for query, atteso in prove:
        trovati = [r[0] for r in motore.cerca(query, k=k)]
        if atteso not in trovati:
            print(f"MANCATO @{k}: '{query}' -> {trovati}")
        centrati += int(atteso in trovati)
    return centrati / len(prove)


if __name__ == "__main__":
    # Una prova al volo, con la query simbolo del capitolo.
    print(motore.cerca("il portatile non si accende"))

    print("recall@1:", recall_a_k(motore, PROVE, 1))
    print("recall@3:", recall_a_k(motore, PROVE, 3))
