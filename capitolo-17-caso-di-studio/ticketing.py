"""Stub del client verso il server MCP del ticketing: il client in
memoria del capitolo 13. Delega alla logica pura di ticket.py, cosi'
anche l'idempotenza della chiave e' esercitata nel collaudo.
"""

import ticket


def apri_ticket(categoria: str, riassunto: str, descrizione: str,
                richiedente: str, chiave: str) -> dict:
    id_ = ticket.crea(categoria, riassunto, descrizione,
                      richiedente, chiave)
    return {"aperto": True, "id": id_}
