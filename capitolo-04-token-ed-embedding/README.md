# Capitolo 4 — Rappresentare il linguaggio: token ed embedding

Codice del capitolo 4 del libro "Intelligenza artificiale per ingegneri": tokenizzazione BPE in pratica, similarità coseno su vettori giocattolo e su embedding reali, ed esplorazione di uno spazio semantico con `sentence-transformers`.

## File

| File | Listato / sezione del libro |
|------|-----------------------------|
| `conta_token_tiktoken.py` | Listato 4.1 (`lst:cap03_tiktoken`), sezione "Token e costi": conta e ispeziona i token di una frase inglese e di una italiana con `tiktoken`. |
| `similarita_coseno_a_mano.py` | Listato senza numero, sezione "Similarità coseno in pratica": verifica in NumPy dei conti fatti a mano su tre vettori a quattro componenti. |
| `prima_misura_embedding_reali.py` | Listato 4.2 (`lst:cap03_prima_misura`): prima misura di similarità su embedding reali con `sentence-transformers`. |
| `esplora_spazio_embedding.py` | Progetto della sezione "Codice: esplorare uno spazio di embedding". Assembla in un unico programma i listati 4.3 (`lst:cap03_parole`), 4.4 (`lst:cap03_vicini`), 4.5 (`lst:cap03_frasi`), 4.6 (`lst:cap03_ricerca`) e 4.7 (`lst:cap03_pca`). |

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
