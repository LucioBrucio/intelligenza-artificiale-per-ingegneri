# Capitolo 17 - Caso di studio: un assistente aziendale completo

Il capitolo finale del libro monta i pezzi costruiti nei capitoli
precedenti in un assistente aziendale: router, agente di ricerca (RAG),
agente operativo con conferma umana, server MCP, valutazione.

Il codice del capitolo e' la "colla" architetturale: i listati mostrano
lo stato condiviso, i nodi, il grafo LangGraph, il server MCP del
ticketing e l'harness di eval. Come dice il libro, il grafo gira per
intero con gli stub (il ModelloFinto del capitolo 14 e il client in
memoria del capitolo 13): e' cosi' che va eseguito qui, senza API key.

## File

| File | Descrizione |
|------|-------------|
| `assistente.py` | Lo stato condiviso, i nodi e la costruzione del grafo LangGraph, assemblati nell'ordine del libro. Listati "Lo stato condiviso", "I nodi del grafo", "La costruzione del grafo". |
| `modello.py`, `rag.py`, `operativo.py`, `ticketing.py` | Stub deterministici: nel libro sono i progetti dei capitoli 11 e 12 iniettati dall'esterno. |
| `ticket.py` | Logica pura del ticketing, con la chiave di idempotenza descritta nel testo. |
| `server_ticket.py` | Adattatore MCP sopra `ticket.py`. Listato "Il server MCP del ticketing, in sintesi". |
| `collaudo_orchestrazione.py` | Il test di orchestrazione descritto nel testo, con assert sulla traccia `passi`. |
| `harness_eval.py` | L'harness di eval con golden set dimostrativo di 3 casi (nel libro sono 60). Listato "L'harness di eval". |

## Esecuzione

```bash
python collaudo_orchestrazione.py   # il grafo con gli stub, senza API key
python harness_eval.py              # la regressione sul golden set demo
```

Entrambi girano offline. `server_ticket.py` richiede il pacchetto
`mcp[cli]`; l'import `from mcp.server import MCPServer` segue il libro,
con SDK che espongono ancora `FastMCP` va adattato (vedi il README del
capitolo 13).

## Requisiti

- `langgraph` (e `typing_extensions`, installata con esso)
- `mcp[cli]` solo per `server_ticket.py`
