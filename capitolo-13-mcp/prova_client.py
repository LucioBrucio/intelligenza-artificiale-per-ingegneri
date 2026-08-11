# prova_client.py: collaudo del server via protocollo,
# senza processi esterni e senza alcun modello.
import asyncio
from mcp import Client

from server import mcp   # il nostro MCPServer

async def main():
    async with Client(mcp) as client:
        # 1. Il server espone cio' che deve?
        elenco = await client.list_tools()
        nomi = [t.name for t in elenco.tools]
        assert "stato_ordine" in nomi
        assert "apri_reclamo" in nomi

        # 2. Il caso buono restituisce i dati giusti?
        r = await client.call_tool("stato_ordine",
                                   {"numero": "ORD-1042"})
        assert r.structured_content["trovato"] is True
        assert r.structured_content["stato"] == "spedito"

        # 3. Il caso d'errore e' parlante?
        r = await client.call_tool("stato_ordine",
                                   {"numero": "ORD-9999"})
        assert r.structured_content["trovato"] is False
        assert "ordini_cliente" in \
            r.structured_content["errore"]

        print("Tutti i controlli superati.")

asyncio.run(main())
