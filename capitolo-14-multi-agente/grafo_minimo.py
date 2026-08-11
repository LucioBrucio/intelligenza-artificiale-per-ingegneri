# Capitolo 14, sezione "LangGraph": un grafo minimo con nodi-stub
# deterministici, arco condizionale, reducer e checkpointer.
# Si esegue senza API key.
# pip install langgraph
from typing import Annotated
from typing_extensions import TypedDict
from operator import add

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

class Stato(TypedDict):
    richiesta: str
    urgente: bool
    passi: Annotated[list[str], add]  # reducer: accumula

def classifica(stato: Stato):
    """Nodo-stub deterministico: in un sistema reale qui
    ci sarebbe una chiamata al modello."""
    urgente = "urgente" in stato["richiesta"].lower()
    return {"urgente": urgente, "passi": ["classifica"]}

def gestione_rapida(stato: Stato):
    return {"passi": ["gestione_rapida"]}

def gestione_standard(stato: Stato):
    return {"passi": ["gestione_standard"]}

def smista(stato: Stato) -> str:
    """Routing dell'arco condizionale: restituisce
    il nome del prossimo nodo."""
    if stato["urgente"]:
        return "gestione_rapida"
    return "gestione_standard"

builder = StateGraph(Stato)
builder.add_node("classifica", classifica)
builder.add_node("gestione_rapida", gestione_rapida)
builder.add_node("gestione_standard", gestione_standard)

builder.add_edge(START, "classifica")
builder.add_conditional_edges("classifica", smista)
builder.add_edge("gestione_rapida", END)
builder.add_edge("gestione_standard", END)

grafo = builder.compile(checkpointer=InMemorySaver())

config = {"configurable": {"thread_id": "pratica-42"}}
finale = grafo.invoke(
    {"richiesta": "URGENTE: il sito e' giu'", "passi": []},
    config)
print(finale["passi"])  # ['classifica', 'gestione_rapida']
