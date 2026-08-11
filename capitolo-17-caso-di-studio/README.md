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

| File | Origine | Note |
|------|---------|------|
| `assistente.py` | Listati "Lo stato condiviso", "I nodi del grafo", "La costruzione del grafo" | Assemblati nell'ordine del libro |
| `modello.py`, `rag.py`, `operativo.py`, `ticketing.py` | Stub deterministici | Nel libro sono i progetti dei capitoli 11 e 12 iniettati dall'esterno |
| `ticket.py` | Logica pura del ticketing | Con la chiave di idempotenza descritta nel testo |
| `server_ticket.py` | Listato "Il server MCP del ticketing, in sintesi" | Adattatore MCP sopra `ticket.py` |
| `collaudo_orchestrazione.py` | Il test di orchestrazione descritto nel testo | Assert sulla traccia `passi` |
| `harness_eval.py` | Listato "L'harness di eval" | Con golden set dimostrativo di 3 casi (nel libro sono 60) |

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
