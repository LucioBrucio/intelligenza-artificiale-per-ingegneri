"""Un agente completo scritto da zero, senza framework.

Registro degli strumenti, budget, memoria di sessione e loop,
piu' il collaudo con un modello finto che rigioca un copione:
gira in un millisecondo, senza chiave API.

Capitolo 12, sezione "Codice: un agente da zero".
"""

from dataclasses import dataclass
from typing import Callable


@dataclass
class Strumento:
    """Dichiarazione piu' funzione eseguibile."""
    nome: str
    descrizione: str
    parametri: dict            # JSON Schema degli argomenti
    esegui: Callable[..., dict]
    scrittura: bool = False    # True se modifica il mondo


class Registro:
    def __init__(self, strumenti):
        self._strumenti = {s.nome: s for s in strumenti}

    def dichiarazioni(self):
        return [{"name": s.nome, "description": s.descrizione,
                 "parameters": s.parametri}
                for s in self._strumenti.values()]

    def richiede_conferma(self, nome):
        s = self._strumenti.get(nome)
        return s is not None and s.scrittura

    def esegui(self, nome, argomenti):
        s = self._strumenti.get(nome)
        # ogni errore e' un messaggio PER IL MODELLO:
        # deve spiegare che cosa fare adesso
        if s is None:
            return {"errore": f"strumento '{nome}' inesistente; "
                    f"disponibili: {sorted(self._strumenti)}"}
        try:
            return s.esegui(**argomenti)
        except TypeError as e:
            return {"errore": f"argomenti non validi "
                              f"per {nome}: {e}"}
        except Exception as e:
            return {"errore": f"{nome} e' fallito: {e}"}


@dataclass
class Budget:
    """La garanzia che l'agente termina per costruzione."""
    max_turni: int = 12
    max_azioni: int = 24
    turni: int = 0
    azioni: int = 0

    def consente_turno(self):
        return self.turni < self.max_turni

    def consente_azione(self):
        return self.azioni < self.max_azioni


class Memoria:
    """Storia della sessione, neutra rispetto al fornitore."""
    def __init__(self, soglia=60):
        self._messaggi = []
        self._soglia = soglia

    def aggiungi(self, messaggio):
        self._messaggi.append(messaggio)

    def messaggi(self):
        if len(self._messaggi) <= self._soglia:
            return list(self._messaggi)
        # compattazione minima: compito + coda recente.
        # Una versione matura riassumerebbe qui la parte
        # scartata con una chiamata dedicata al modello.
        return [self._messaggi[0],
                {"ruolo": "utente", "testo":
                 "[storia troncata: turni vecchi omessi]"},
                *self._messaggi[-(self._soglia - 2):]]


@dataclass
class Risposta:
    testo: str | None   # risposta finale, se il lavoro e' concluso
    chiamate: list      # [(nome, argomenti), ...] altrimenti


def esegui_agente(compito, modello, registro, budget,
                  conferma=lambda nome, argomenti: True):
    memoria = Memoria()
    memoria.aggiungi({"ruolo": "utente", "testo": compito})

    while budget.consente_turno():
        budget.turni += 1
        # osservare e ragionare: una chiamata al modello
        r = modello.genera(memoria.messaggi(),
                           registro.dichiarazioni())
        memoria.aggiungi({"ruolo": "assistente",
                          "testo": r.testo,
                          "chiamate": r.chiamate})
        # nessuna azione richiesta: il compito e' concluso
        if not r.chiamate:
            return r.testo or "(nessuna risposta)"

        # agire: ogni richiesta passa dai guardrail
        for nome, argomenti in r.chiamate:
            if not budget.consente_azione():
                esito = {"errore":
                         "budget di azioni esaurito: concludi "
                         "e riferisci lo stato del lavoro"}
            elif (registro.richiede_conferma(nome)
                  and not conferma(nome, argomenti)):
                esito = {"errore":
                         "azione rifiutata dall'operatore"}
            else:
                budget.azioni += 1
                esito = registro.esegui(nome, argomenti)
            memoria.aggiungi({"ruolo": "strumento",
                              "nome": nome, "esito": esito})

    return ("Interrotto: budget di turni esaurito. "
            "La memoria contiene la traiettoria completa.")


class ModelloFinto:
    """Rigioca un copione: collauda il loop senza API."""
    def __init__(self, copione):
        self._copione = list(copione)

    def genera(self, messaggi, dichiarazioni):
        return self._copione.pop(0)


# due strumenti finti su dati in memoria
def cerca_ordini(stato, giorni_min=0):
    return {"ordini": [{"id": "ORD-1207",
                        "fornitore_id": "F-031",
                        "giorni_blocco": 12}]}


def prepara_sollecito(ordine_id, destinatario, corpo):
    return {"stato": "bozza creata", "bozza_id": "BZ-1"}


# schemi abbreviati per il test: quelli completi si
# scrivono come nella sezione sul tool design
SCHEMA = {"type": "object"}

registro = Registro([
    Strumento("cerca_ordini",
              "Cerca ordini per stato e anzianita'.",
              SCHEMA, cerca_ordini),
    Strumento("prepara_sollecito",
              "Crea la BOZZA di un sollecito (non invia).",
              SCHEMA, prepara_sollecito,
              scrittura=True),
])


if __name__ == "__main__":
    copione = [
        Risposta(None, [("cerca_ordini",
                         {"stato": "bloccato", "giorni_min": 7})]),
        Risposta(None, [("prepara_sollecito",
                         {"ordine_id": "ORD-1207",
                          "destinatario": "ordini@rossi.it",
                          "corpo": "Spett.le fornitore, ..."})]),
        Risposta("Bozza BZ-1 pronta per ORD-1207.", []),
    ]

    budget = Budget(max_turni=5)
    esito = esegui_agente("Prepara i solleciti.",
                          ModelloFinto(copione), registro, budget)
    print(esito)                 # Bozza BZ-1 pronta per ORD-1207.
    assert budget.turni == 3 and budget.azioni == 2
