"""Il test di orchestrazione descritto nel capitolo 17: il grafo gira
per intero con gli stub e l'assert sulla traccia `passi` protegge
topologia e routing in continuous integration, senza API key.

Esecuzione:  python collaudo_orchestrazione.py
"""

from langgraph.types import Command

from assistente import grafo


def esegui(richiesta: str, utente: str, thread: str):
    cfg = {"configurable": {"thread_id": thread}}
    fin = grafo.invoke({"richiesta": richiesta, "utente": utente,
                        "passi": []}, cfg)
    return fin, cfg


# 1) Richiesta documentale: router -> ricerca.
fin, _ = esegui("Qual e' la procedura per il rimborso chilometrico?",
                "mario.rossi", "t1")
assert fin["passi"] == ["router -> SEMPLICE", "ricerca"], fin["passi"]
assert fin["fonti"] == ["Regolamento trasferte - Art. 4"]
print("documentale ok:", fin["passi"])

# 2) Azione con scrittura: router -> operativo -> interrupt -> conferma.
fin, cfg = esegui("Apri un ticket: il monitor e' guasto",
                  "mario.rossi", "t2")
assert fin["passi"] == ["router -> AZIONE", "operativo: proposta"], \
    fin["passi"]
# Il grafo e' sospeso sull'interrupt(): la proposta attende l'assenso.
fin = grafo.invoke(Command(resume="si"), cfg)
assert fin["esito_azione"].startswith("aperto il ticket TCK-"), \
    fin["esito_azione"]
print("azione ok:", fin["passi"], "->", fin["esito_azione"])

# 3) Fuori ambito: il router risponde con la formula di cortesia.
fin, _ = esegui("Che tempo fa domani?", "mario.rossi", "t3")
assert fin["passi"] == ["router -> FUORI"], fin["passi"]
assert fin["risposta"].startswith("Posso aiutarti")
print("fuori ambito ok:", fin["passi"])

# 4) Idempotenza: stessa chiave, stesso ticket (nessun duplicato).
import ticket
a = ticket.crea("IT", "r", "d", "mario.rossi", "chiave-x")
b = ticket.crea("IT", "r", "d", "mario.rossi", "chiave-x")
assert a == b
print("idempotenza ok:", a, "==", b)

print("Collaudo di orchestrazione superato.")
