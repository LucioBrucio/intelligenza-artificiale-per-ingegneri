"""Capitolo 17, listato "Il server MCP del ticketing, in sintesi":
l'adattatore MCP sopra la logica pura di ticket.py.

Le due lezioni del listato: la chiave di idempotenza (derivata dal
thread_id della conversazione) e gli errori parlanti, che spiegano al
modello le alternative invece di sollevare un'eccezione anonima.

Nota sull'SDK: l'import segue il libro (from mcp.server import
MCPServer); con versioni dell'SDK che espongono ancora FastMCP,
adattare l'import come documentato nel README del capitolo 13.
"""

# server_ticket.py: adattatore MCP sopra ticket.py.
from mcp.server import MCPServer
import ticket    # logica pura: crea(), stato(); test unitari

mcp = MCPServer("azienda-ticket")

CATEGORIE = ("IT", "MANUTENZIONE", "FACILITY")

@mcp.tool()
def apri_ticket(categoria: str, riassunto: str,
                descrizione: str, richiedente: str,
                chiave: str) -> dict[str, object]:
    """Apre un ticket di assistenza interna. Categorie
    ammesse: IT, MANUTENZIONE, FACILITY. Operazione con
    effetti permanenti: chiamala solo dopo la conferma
    esplicita dell'utente. 'chiave' e' l'identificatore
    di idempotenza della richiesta."""
    if categoria not in CATEGORIE:
        return {"aperto": False,
                "errore": f"Categoria '{categoria}' non "
                          "valida: usa IT, MANUTENZIONE "
                          "o FACILITY."}
    id_ = ticket.crea(categoria, riassunto, descrizione,
                      richiedente, chiave)
    return {"aperto": True, "id": id_}

@mcp.tool()
def stato_ticket(id: str) -> dict[str, object]:
    """Stato e assegnatario di un ticket esistente,
    dato il suo identificatore nel formato TCK-XXXX."""
    dati = ticket.stato(id)
    if dati is None:
        return {"trovato": False,
                "errore": f"Nessun ticket {id}: verifica "
                          "il formato TCK-XXXX."}
    return {"trovato": True, **dati}


if __name__ == "__main__":
    mcp.run()   # trasporto stdio, come nel capitolo 13
