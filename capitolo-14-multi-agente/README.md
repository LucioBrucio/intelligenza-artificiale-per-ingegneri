# Capitolo 14 - Sistemi multi-agente

Codice del capitolo 14 di "Intelligenza artificiale per ingegneri": orchestrazione di piu agenti con LangGraph, human-in-the-loop con checkpoint e il progetto finale supervisor + specialisti.

## File

| File | Descrizione |
|---|---|
| `grafo_minimo.py` | Grafo minimo con nodi-stub deterministici: stato tipizzato con reducer, arco condizionale, checkpointer in memoria. Sezione "LangGraph". |
| `approvazione_umana.py` | Nodo di approvazione che sospende il grafo con `interrupt()` e riprende con `Command(resume=...)`; le stampe mostrano il payload dell'interrupt e l'esito. Sezione "Human-in-the-loop". |
| `supervisor_specialisti.py` | Il progetto del capitolo: supervisor che delega ad analista e redattore su un grafo LangGraph con checkpoint, con le chiamate al modello dietro un'unica interfaccia e l'implementazione reale `ModelloVertex` (Gemini via `google-genai`). Sezione "Codice: supervisor e specialisti". |
| `agent-card.json` | La agent card A2A d'esempio, che nel protocollo si pubblica su `/.well-known/agent-card.json`. Sezione "Comunicazione tra agenti". |

Il listato con l'output atteso dell'esecuzione (fine capitolo) e output di console e non e stato trasformato in file.

## Esecuzione

```bash
pip install langgraph google-genai

python3 grafo_minimo.py           # senza API key
python3 approvazione_umana.py     # senza API key
export GEMINI_API_KEY=<chiave>    # da https://aistudio.google.com/apikey
python3 supervisor_specialisti.py
```

`grafo_minimo.py` e `approvazione_umana.py` girano in locale senza API key
(usano nodi-stub deterministici). `supervisor_specialisti.py` chiama Gemini
attraverso `ModelloVertex`: se la chiave manca, lo script lo segnala ed esce
con codice 1. In alternativa, su Vertex AI, si usa
`genai.Client(vertexai=True, project="...", location="...")` come indicato
nel commento nel codice.

## Requisiti

- Python 3.12
- `langgraph` (tutti gli script)
- `typing_extensions` (installato automaticamente con `langgraph`)
- `google-genai` e `GEMINI_API_KEY` (solo per `supervisor_specialisti.py`)
