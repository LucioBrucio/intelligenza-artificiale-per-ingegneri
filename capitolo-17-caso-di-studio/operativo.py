"""Stub dell'agente operativo del capitolo 12: nessun modello, esiti da
copione. Se la richiesta parla di ticket produce una proposta strutturata
(che il grafo sottopone a conferma umana); altrimenti risponde in sola
lettura sullo stato di un ordine.

Nel sistema vero questo modulo e' il loop del capitolo 12
(codice/capitolo-12-agenti/agente_da_zero.py) equipaggiato con i tool
dei due server MCP.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Esito:
    testo: str = ""
    proposta_ticket: Optional[dict] = None


def esegui(richiesta: str, utente: str) -> Esito:
    if "ticket" in richiesta.lower():
        return Esito(proposta_ticket={
            "categoria": "IT",
            "riassunto": "Monitor guasto",
            "descrizione": richiesta,
            "richiedente": utente,
            "chiave": f"{utente}-demo-1",   # idempotenza (cap. 15)
        })
    return Esito(testo="L'ordine ORD-1042 risulta spedito, "
                       "aggiornato al 2026-08-02. (stub)")
