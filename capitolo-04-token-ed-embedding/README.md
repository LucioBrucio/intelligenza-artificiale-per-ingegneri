# Capitolo 4 — Rappresentare il linguaggio: token ed embedding

Codice del capitolo 4 del libro "Intelligenza artificiale per ingegneri": tokenizzazione BPE in pratica, similarità coseno su vettori giocattolo e su embedding reali, ed esplorazione di uno spazio semantico con `sentence-transformers`.

## File

| File | Descrizione |
|------|-------------|
| `conta_token_tiktoken.py` | Conta e ispeziona i token di una frase inglese e di una italiana con `tiktoken`. Listato 4.1, sezione "Token e costi". |
| `similarita_coseno_a_mano.py` | Verifica in NumPy dei conti fatti a mano sulla similarità coseno di tre vettori a quattro componenti. Sezione "Similarità coseno in pratica". |
| `prima_misura_embedding_reali.py` | Prima misura di similarità su embedding reali con `sentence-transformers`. Listato 4.2. |
| `esplora_spazio_embedding.py` | Esplorazione di uno spazio di embedding: parole vicine, frasi, ricerca semantica e proiezione PCA. Listati 4.3-4.7, sezione "Codice: esplorare uno spazio di embedding". |

## Come eseguire

Richiede Python 3.12. Installare le dipendenze:

```bash
pip install numpy tiktoken sentence-transformers scikit-learn
```

Poi lanciare i singoli script:

```bash
python3 conta_token_tiktoken.py
python3 similarita_coseno_a_mano.py
python3 prima_misura_embedding_reali.py
python3 esplora_spazio_embedding.py
```

## Requisiti

- Nessuna credenziale o chiave API.
- `similarita_coseno_a_mano.py` gira completamente offline.
- `conta_token_tiktoken.py` scarica alla prima esecuzione i dati del tokenizzatore `cl100k_base` (serve la connessione a internet una volta sola, poi resta in cache).
- `prima_misura_embedding_reali.py` ed `esplora_spazio_embedding.py` scaricano alla prima esecuzione il modello `paraphrase-multilingual-MiniLM-L12-v2` da Hugging Face (circa 470 MB, poi in cache locale); il modello gira comodamente su CPU.

I valori numerici stampati possono differire leggermente da quelli riportati nel libro a seconda della versione del modello: la graduatoria delle similarità, come spiegato nel testo, resta la stessa.
