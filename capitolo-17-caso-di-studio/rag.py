"""Stub della pipeline RAG del capitolo 11: risposta fissa con citazione.

Nel sistema vero questo modulo e' il progetto del capitolo 11
(codice/capitolo-11-rag/rag_completo.py) applicato all'indice ibrido
aziendale, con il filtro sui permessi dell'utente.
"""


def rispondi(domanda: str, utente: str, modello: str):
    testo = ("Il rimborso per l'uso dell'auto personale e' di "
             "0,42 euro al chilometro [1]. "
             "(risposta dello stub, non di un modello)")
    estratti = [{"id": "Regolamento trasferte - Art. 4"}]
    return testo, estratti
