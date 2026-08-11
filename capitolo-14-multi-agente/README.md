# Capitolo 14 - Sistemi multi-agente

Codice del capitolo 14 di "Intelligenza artificiale per ingegneri": orchestrazione di piu agenti con LangGraph, human-in-the-loop con checkpoint e il progetto finale supervisor + specialisti.

## File

| File | Sezione del libro | Contenuto |
|---|---|---|
| `grafo_minimo.py` | "LangGraph" (primi due listati, assemblati) | Grafo minimo con nodi-stub deterministici: stato tipizzato con reducer, arco condizionale, checkpointer in memoria. |
| `approvazione_umana.py` | "Human-in-the-loop" | Nodo di approvazione che sospende il grafo con `interrupt()` e riprende con `Command(resume=...)`. Lo `Stato` e la costruzione del grafo attorno al nodo sono aggiunte minime per rendere eseguibile il listato; le stampe mostrano il payload dell'interrupt e l'esito. |
| `supervisor_specialisti.py` | "Codice: supervisor e specialisti" (quattro listati, assemblati) | Il progetto del capitolo: supervisor che delega ad analista e redattore su un grafo LangGraph con checkpoint. Le chiamate al modello passano da un'interfaccia con due implementazioni: `ModelloFinto` (stub deterministico, default) e `ModelloVertex` (Gemini via `google-genai`). |
| `agent-card.json` | "Comunicazione tra agenti" | La agent card A2A d'esempio; nel protocollo si pubblica su `/.well-known/agent-card.json`. Le stringhe spezzate su piu righe nel listato del libro sono state ricongiunte per avere JSON valido. |

Il listato con l'output atteso dell'esecuzione con lo stub (fine capitolo) e output di console e non e stato trasformato in file.

## Esecuzione

```bash
pip install langgraph

python3 grafo_minimo.py
python3 approvazione_umana.py
python3 supervisor_specialisti.py
```

Tutti e tre gli script girano in locale senza API key: `supervisor_specialisti.py` usa di default lo stub `ModelloFinto`.

## Modello reale (opzionale)

Per usare Gemini in `supervisor_specialisti.py`:

1. `pip install google-genai`
2. Esporta la chiave: `export GOOGLE_API_KEY=<chiave>` (si ottiene su https://aistudio.google.com/apikey). Se la variabile manca, lo script lo segnala ed esce con codice 1. In alternativa, su Vertex AI, si usa `genai.Client(vertexai=True, project="...", location="...")` come indicato nel commento nel codice.
3. Sostituisci la riga `modello = ModelloFinto()` con `modello = ModelloVertex()`.

## Requisiti

- Python 3.12
- `langgraph` (tutti gli script)
- `typing_extensions` (installato automaticamente con `langgraph`)
- `google-genai` (solo per `ModelloVertex`)
