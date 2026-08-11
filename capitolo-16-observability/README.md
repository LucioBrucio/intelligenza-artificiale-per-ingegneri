# Capitolo 16 - Observability e valutazione

Codice del progetto di fine capitolo: la pipeline di valutazione e regressione per il RAG di ACME del capitolo 11, con golden set, verifica programmatica delle citazioni, giudice LLM con rubrica (e stub deterministico per la continuous integration), report di regressione con soglie di blocco; più la strumentazione di tracing con LangSmith e i materiali dell'esempio sul giudice con rubrica.

## File

| File | Corrisponde a |
|---|---|
| `pipeline_eval.py` | i sei listati della sezione "Codice: una pipeline di eval", assemblati in un unico programma nell'ordine del libro: configurazione e golden set, `citazioni_valide`, la rubrica del giudice, `GiudiceGemini` e `GiudiceStub`, `valuta_sistema`, `report_regressione` con il blocco main |
| `tracing_langsmith.py` | il listato della sezione "Tracing": la strumentazione con il decoratore `@traceable`; i corpi di `riscrivi` e `rispondi` sono omessi come nel libro perché identici al capitolo 11 |
| `rubrica_confronto.txt` | il prompt con rubrica della sezione "Metriche di valutazione", per il confronto tra due risposte: criteri in ordine di priorità, motivazione prima del verdetto, uscita in JSON |
| `risposte_confronto.txt` | le risposte A e B dell'esempio della stessa sezione (la B contiene il massimale di 800 km che negli estratti non esiste: il caso che il bias di verbosità premia e la rubrica smaschera) |
| `eval/registrazioni.json` | le risposte registrate che la pipeline rigioca quando gira senza API key, come previsto dal listato; due casi coerenti con il golden set, con gli estratti nel formato dei chunk del capitolo 11 |
| `eval/baseline_v1_4.json` | la baseline archiviata che `report_regressione` confronta con la candidata, allineata alle registrazioni così che la passata dimostrativa termini senza blocchi (codice di uscita 0) |

Nel libro il golden set conta 50 casi; qui ne sono inclusi i due mostrati nel listato (G01 e G02). Il listato con gli `export LANGSMITH_*` è riportato sotto, quello con l'output del report di regressione è solo output e non è stato trasformato in file.

## Come eseguire

```bash
pip install google-genai
cd codice/capitolo-16-observability
python3 pipeline_eval.py
```

Senza argomenti la pipeline usa il giudice stub e le risposte registrate: nessuna API key, come in CI. Stampa il report di regressione (metrica, base, cand, delta, esito), scrive `eval/candidata.json` ed esce con 0 se il rilascio può procedere, con 1 se è bloccato. Va lanciata dalla directory del capitolo, perché legge `eval/...` con percorsi relativi. I valori assoluti delle metriche in questa modalità vengono dalle euristiche dello stub (per esempio il rifiuto atteso di G02 conta come non pertinente): come dice il libro, lo stub non sostituisce il giudice, sostituisce l'API key, e la passata dimostra la meccanica del confronto con la baseline.

```bash
export GEMINI_API_KEY=<la-tua-chiave>   # gratuita su https://aistudio.google.com/apikey
python3 pipeline_eval.py --con-api
```

Con `--con-api` il giudice è Gemini con la rubrica e temperatura a zero; per valutare il sistema vero serve anche la funzione `rispondi` del capitolo 11 (`codice/capitolo-11-rag/rag_completo.py`), da importare nel file: senza, lo script spiega ed esce.

Il tracing si attiva per variabili d'ambiente, senza toccare il codice:

```bash
pip install langsmith
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY=<la-tua-chiave>   # https://smith.langchain.com
export LANGSMITH_PROJECT=assistente-acme
python3 tracing_langsmith.py
```

`tracing_langsmith.py` mostra la strumentazione: per produrre trace complete i corpi delle funzioni vanno ripresi dal codice del capitolo 11.

## Requisiti

- Python 3.12
- pacchetti: `google-genai` (per `pipeline_eval.py`), `langsmith` (per `tracing_langsmith.py`)
- nessuna credenziale per la passata di default di `pipeline_eval.py`; `GEMINI_API_KEY` (o `GOOGLE_API_KEY`) per `--con-api`; `LANGSMITH_API_KEY` per il tracing. In entrambi i casi, se la variabile manca lo script stampa come ottenerla ed esce con codice 1
