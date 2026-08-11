# Capitolo 10: ricerca semantica e vector database

Codice del progetto finale del capitolo: un motore di ricerca semantica completo e misurabile, dalla scansione esatta con NumPy al trasloco su Qdrant.

## File

| File | Listati del libro | Contenuto |
|---|---|---|
| `motore_ricerca_semantica.py` | 10.3 (corpus), 10.4 (motore), 10.5 (recall) | Corpus di otto chunk, classe `MotoreRicerca` con indicizzazione e ricerca esatta via NumPy, insieme di valutazione `PROVE` e funzione `recall_a_k`. Il main esegue la prova con la query "il portatile non si accende" e stampa recall@1 e recall@3. |
| `motore_qdrant.py` | 10.6 (Qdrant) | Lo stesso motore trasferito su Qdrant in modalita' `:memory:`, con upsert dei vettori e query filtrata sul metadato `tema`. Importa il motore gia' indicizzato dal file precedente. |

I listati 10.1 e 10.2 (taglio a dimensione fissa e taglio strutturale) sono esempi illustrativi di chunking, non codice, e non compaiono qui.

## Come eseguire

```bash
pip install sentence-transformers numpy qdrant-client

python3 motore_ricerca_semantica.py
python3 motore_qdrant.py
```

## Requisiti

- Python 3.12.
- Nessuna credenziale o chiave API: tutto gira in locale.
- Al primo avvio `sentence-transformers` scarica il modello `paraphrase-multilingual-MiniLM-L12-v2` da Hugging Face (serve la connessione a internet una volta sola; poi resta in cache).
- Qdrant gira in memoria dentro il processo: nessun server da installare. Per una istanza reale sostituire `":memory:"` con l'URL del servizio.
