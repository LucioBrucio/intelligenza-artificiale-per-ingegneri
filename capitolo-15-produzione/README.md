# Capitolo 15 - LLM in produzione

Codice del capitolo 15 del libro "Intelligenza artificiale per ingegneri": le tre tecniche mostrate nei listati del capitolo, con la logica separata dalle chiamate e le dipendenze iniettate, come nel testo.

## File

| File | Listato del libro | Contenuto |
|---|---|---|
| `cache_semantica.py` | sezione "Latenza" | la classe `CacheSemantica`, che indicizza le risposte per similarita' semantica della domanda |
| `routing_per_complessita.py` | sezione "Costi" | le costanti dei modelli, il `PROMPT_ROUTER` e la funzione `instrada` che smista le richieste tra modello piccolo e grande |
| `catena_di_fallback.py` | sezione "Affidabilita'" | la `CATENA_FALLBACK` e la funzione `genera_con_fallback` che percorre i gradini fino al provider indipendente |

`catena_di_fallback.py` importa le costanti `MODELLO_GRANDE` e `MODELLO_PICCOLO` da `routing_per_complessita.py`, come nel capitolo, dove il listato sul fallback riusa i nomi definiti nel listato sul routing.

## Come eseguirli

Ogni file e' autonomo e contiene un blocco dimostrativo con stub al posto delle chiamate vere (nel libro le funzioni `embed`, `classifica`, `genera`, `chiama` e `registra` sono iniettate e in produzione parlano con il gateway LLM):

```
python3 cache_semantica.py
python3 routing_per_complessita.py
python3 catena_di_fallback.py
```

## Requisiti

Python 3.12, nessuna libreria esterna, nessuna credenziale: gli esempi usano solo la libreria standard e stub dimostrativi.
