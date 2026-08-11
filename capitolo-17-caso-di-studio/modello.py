"""Stub deterministico dell'interfaccia verso i modelli: il ModelloFinto
del capitolo 14. Nessuna chiamata di rete, verdetti da copione, cosi' il
grafo gira in continuous integration senza API key.

In produzione al suo posto c'e' l'adattatore verso Vertex AI dietro il
gateway del capitolo 15, iniettato con la stessa interfaccia genera().
"""


def genera(nome_modello: str, prompt: str, testo: str) -> str:
    """Router di comodo: classifica con poche parole chiave."""
    t = testo.lower()
    if "ticket" in t or "ordine" in t or "ordini" in t:
        return "AZIONE"
    if any(p in t for p in ("rimborso", "procedura", "manuale",
                            "circolare", "ferie", "errore")):
        return "SEMPLICE"
    if any(p in t for p in ("confronta", "differenza", "quale norma")):
        return "COMPLESSA"
    return "FUORI"
