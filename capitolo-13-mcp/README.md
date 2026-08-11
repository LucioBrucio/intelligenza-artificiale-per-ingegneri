# Capitolo 13 - Il Model Context Protocol

Codice del progetto guidato del capitolo 13: un server MCP per il database ordini di ACME S.p.A., costruito con l'SDK Python ufficiale e collaudato senza alcun modello.

## File

| File | Corrisponde a |
|------|---------------|
| `ordini.py` | Sezione "Costruire un server MCP": modulo di puro accesso ai dati, senza dipendenze da MCP. |
| `server.py` | Sezione "Lo strato MCP": i due listati di `server.py` assemblati in un unico file (tool `stato_ordine` e `ordini_cliente`, poi `apri_reclamo`, la resource `ordini://schema` e il prompt `gestione_reclamo`). |
| `prova_client.py` | Sezione "Collaudo, senza modello": client MCP in memoria che verifica tool, caso buono e caso d'errore. |
| `popola_dati.py` | Dati di esempio citati nel testo ("tre ordini di prova, tra cui ORD-1042 della Rossi Srl, in stato spedito"): popola `ordini.db` per gli esperimenti. |
| `claude_desktop_config.json` | Sezione "Collaudo, senza modello": esempio di configurazione di un host (Claude Desktop) per lanciare il server via stdio. Da adattare con il percorso assoluto reale di `server.py`. |

I listati del capitolo che sono trascrizioni di messaggi JSON-RPC (handshake `initialize`, `tools/list`, `tools/call`, `resources/read`, `prompts/get`) e l'esempio di tool poisoning della sezione sulla sicurezza sono materiale illustrativo, non file eseguibili, e non sono riprodotti qui.

## Requisiti

- Python 3.12
- SDK Python di MCP: `pip install "mcp[cli]"` (l'extra `cli` aggiunge il comando `mcp`, usato dall'Inspector)
- Nessuna chiave API: tutto il collaudo avviene senza modelli

Nota di nomenclatura (dal capitolo): l'API ad alto livello dell'SDK è nata col nome `FastMCP`; nella versione 2 dell'SDK la classe si chiama `MCPServer`, ma il modello di programmazione è lo stesso. Se la vostra versione dell'SDK usa ancora `FastMCP`, adattate l'import in `server.py`.

## Esecuzione

1. Popolare il database di prova (crea `ordini.db` nella directory corrente):

       python3 popola_dati.py

2. Collaudo via protocollo, con il client in memoria:

       python3 prova_client.py

   Atteso: `Tutti i controlli superati.`

3. Esplorazione con MCP Inspector (richiede Node.js):

       mcp dev server.py

4. Avvio del server su stdio (è l'host a lanciarlo, di norma):

       python3 server.py

   Per esporlo via rete: `mcp.run(transport="streamable-http", port=3001)` al posto di `mcp.run()`.

5. Aggancio a Claude Desktop: copiare il blocco di `claude_desktop_config.json` nella configurazione dell'host, con il percorso assoluto di `server.py`.
