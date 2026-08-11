# server.py: lo strato MCP sopra la logica di ordini.py.
from mcp.server import MCPServer

import ordini

mcp = MCPServer("acme-ordini")

@mcp.tool()
def stato_ordine(numero: str) -> dict[str, object]:
    """Restituisce stato, cliente, totale e data di ultimo
    aggiornamento di un ordine dato il suo numero, nel
    formato ORD-XXXX. Usalo quando l'utente chiede di un
    ordine specifico."""
    conn = ordini.apri_connessione()
    try:
        dati = ordini.stato_ordine(conn, numero)
    finally:
        conn.close()
    if dati is None:
        # Errore di esecuzione parlante: il modello lo legge,
        # capisce e puo' correggersi (capitolo 12).
        return {"trovato": False,
                "errore": f"Nessun ordine con numero {numero}. "
                          "Verifica il formato ORD-XXXX o cerca "
                          "per cliente con ordini_cliente."}
    return {"trovato": True, **dati}

@mcp.tool()
def ordini_cliente(cliente: str, limite: int = 10) -> list[dict]:
    """Elenca gli ordini piu' recenti di un cliente, cercato
    per nome anche parziale. Restituisce al massimo 'limite'
    ordini con numero, stato e totale."""
    conn = ordini.apri_connessione()
    try:
        return ordini.ordini_di(conn, cliente, limite)
    finally:
        conn.close()

@mcp.tool()
def apri_reclamo(numero_ordine: str,
                 motivo: str) -> dict[str, object]:
    """Apre un reclamo formale su un ordine. Operazione con
    effetti permanenti: usala solo dopo che l'utente ha
    confermato esplicitamente di voler procedere."""
    conn = ordini.apri_connessione()
    try:
        if ordini.stato_ordine(conn, numero_ordine) is None:
            return {"aperto": False,
                    "errore": f"Ordine {numero_ordine} "
                              "inesistente: nessun reclamo "
                              "aperto."}
        id_reclamo = ordini.apri_reclamo(conn, numero_ordine,
                                         motivo)
    finally:
        conn.close()
    return {"aperto": True, "id_reclamo": id_reclamo}

@mcp.resource("ordini://schema")
def schema_database() -> str:
    """Schema del database ordini: tabelle, campi e stati
    possibili di un ordine."""
    return ordini.SCHEMA

@mcp.prompt(title="Gestione reclamo")
def gestione_reclamo(numero_ordine: str) -> str:
    """Istruisce l'assistente sulla prassi ACME per i reclami."""
    return (f"Gestisci un reclamo per l'ordine {numero_ordine} "
            "seguendo la prassi ACME: 1) verifica lo stato "
            "con lo strumento stato_ordine; 2) se risulta "
            "consegnato da piu' di 30 giorni, informa che il "
            "reclamo va inoltrato all'assistenza post-vendita; "
            "3) altrimenti riassumi il problema all'utente, "
            "chiedi conferma esplicita e solo dopo usa "
            "apri_reclamo.")

if __name__ == "__main__":
    mcp.run()   # comunicazione via stdio; il server ora e' in ascolto
