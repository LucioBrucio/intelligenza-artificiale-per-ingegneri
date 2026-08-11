"""Logica pura del ticketing, senza protocollo: crea() e stato(),
testabili con unit test ordinari (il metodo del capitolo 13).

La chiave di idempotenza fa cio' che il capitolo 17 descrive: se un retry
del gateway o una ripresa del grafo recapita la chiamata due volte,
crea() riconosce la chiave gia' vista e restituisce il ticket esistente
invece di duplicarlo.
"""

_ticket: dict[str, dict] = {}       # id -> dati
_per_chiave: dict[str, str] = {}    # chiave idempotenza -> id


def crea(categoria: str, riassunto: str, descrizione: str,
         richiedente: str, chiave: str) -> str:
    if chiave in _per_chiave:           # richiesta gia' vista
        return _per_chiave[chiave]
    id_ = f"TCK-{1000 + len(_ticket) + 1}"
    _ticket[id_] = {"stato": "aperto", "assegnatario": None,
                    "categoria": categoria, "riassunto": riassunto,
                    "descrizione": descrizione,
                    "richiedente": richiedente}
    _per_chiave[chiave] = id_
    return id_


def stato(id: str):
    dati = _ticket.get(id)
    if dati is None:
        return None
    return {"stato": dati["stato"],
            "assegnatario": dati["assegnatario"]}
