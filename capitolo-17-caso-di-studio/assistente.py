"""Capitolo 17, listati "Lo stato condiviso", "I nodi del grafo" e
"La costruzione del grafo": l'orchestrazione completa dell'assistente
aziendale.

I moduli rag, operativo, ticketing e modello sono qui stub deterministici
(vedi i rispettivi file): il libro li descrive come i progetti dei
capitoli 11 e 12 iniettati dall'esterno. Il grafo gira per intero con gli
stub, senza API key, come descritto nella sezione sull'architettura:
e' il test di orchestrazione eseguito da collaudo_orchestrazione.py.
"""

# Costanti dei modelli, come nei capitoli 11 e 15:
# sono la parte del codice che invecchia prima.
MODELLO_GRANDE  = "gemini-2.5-pro"
MODELLO_PICCOLO = "gemini-2.5-flash"

from typing import Annotated, Optional
from typing_extensions import TypedDict
from operator import add

class Stato(TypedDict):
    richiesta: str      # la domanda del dipendente
    utente: str         # identita': guida permessi e tracce
    categoria: str      # verdetto del router
    risposta: str       # testo finale, con citazioni
    fonti: list[str]    # identificatori dei chunk citati
    proposta_ticket: Optional[dict]  # bozza in attesa di ok
    esito_azione: str   # esito dell'azione confermata
    passi: Annotated[list[str], add] # traccia ad accumulo


# --- I nodi del grafo: ogni nodo richiama un pezzo costruito ---
# --- nei capitoli precedenti.                                 ---
from langgraph.types import interrupt

import rag         # pipeline RAG del capitolo 11 (qui: stub)
import operativo   # loop agentico del capitolo 12 (qui: stub)
import ticketing   # client del server MCP del ticketing (qui: stub)
import modello     # interfaccia iniettata verso i modelli (qui: stub)

PROMPT_ROUTER = """Classifica la richiesta di un dipendente.
SEMPLICE: domanda documentale su un fatto o una procedura.
COMPLESSA: domanda documentale su piu' fonti o casi ambigui.
AZIONE: chiede un ticket o lo stato di un ordine.
FUORI: tutto il resto. Nel dubbio tra SEMPLICE e COMPLESSA
scegli COMPLESSA. Rispondi con una sola parola."""

CORTESIA = ("Posso aiutarti sui documenti aziendali, "
            "sui ticket e sullo stato degli ordini.")

def nodo_router(stato: Stato):
    v = modello.genera(MODELLO_PICCOLO, PROMPT_ROUTER,
                       stato["richiesta"][:2000]).strip()
    out = {"categoria": v, "passi": [f"router -> {v}"]}
    if v == "FUORI":   # risposta standard di cortesia
        out["risposta"] = CORTESIA
    return out

def nodo_ricerca(stato: Stato):
    m = (MODELLO_PICCOLO if stato["categoria"] == "SEMPLICE"
         else MODELLO_GRANDE)
    testo, estratti = rag.rispondi(
        stato["richiesta"], utente=stato["utente"], modello=m)
    return {"risposta": testo,
            "fonti": [c["id"] for c in estratti],
            "passi": ["ricerca"]}

def nodo_operativo(stato: Stato):
    esito = operativo.esegui(stato["richiesta"],
                             utente=stato["utente"])
    if esito.proposta_ticket:   # bozza: serve la conferma
        return {"proposta_ticket": esito.proposta_ticket,
                "passi": ["operativo: proposta"]}
    return {"risposta": esito.testo,   # sola lettura
            "passi": ["operativo: lettura"]}

def nodo_conferma(stato: Stato):
    ok = interrupt({"da_confermare": stato["proposta_ticket"]})
    if ok != "si":
        return {"esito_azione": "annullato dall'utente",
                "passi": ["conferma: no"]}
    # La scrittura avviene QUI, dopo l'interrupt e fuori
    # dal controllo del modello (capitoli 12 e 14).
    r = ticketing.apri_ticket(**stato["proposta_ticket"])
    return {"esito_azione": f"aperto il ticket {r['id']}",
            "passi": ["conferma: si"]}


# --- La costruzione del grafo. ---
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

def smista(stato: Stato) -> str:
    if stato["categoria"] in ("SEMPLICE", "COMPLESSA"):
        return "ricerca"
    if stato["categoria"] == "AZIONE":
        return "operativo"
    return END    # FUORI: la risposta l'ha scritta il router

def serve_conferma(stato: Stato) -> str:
    return "conferma" if stato.get("proposta_ticket") else END

builder = StateGraph(Stato)
builder.add_node("router", nodo_router)
builder.add_node("ricerca", nodo_ricerca)
builder.add_node("operativo", nodo_operativo)
builder.add_node("conferma", nodo_conferma)

builder.add_edge(START, "router")
builder.add_conditional_edges("router", smista)
builder.add_conditional_edges("operativo", serve_conferma)
builder.add_edge("ricerca", END)
builder.add_edge("conferma", END)

saver = InMemorySaver()   # aggiunta minima per l'esecuzione
grafo = builder.compile(checkpointer=saver)
# saver: InMemorySaver nei test, Postgres in produzione,
# come nel capitolo 14; il thread_id e' la conversazione.
