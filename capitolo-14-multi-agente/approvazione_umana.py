# Capitolo 14, sezione "Human-in-the-loop": sospensione del grafo con
# interrupt() e ripresa con Command(resume=...) sullo stesso thread_id.
# Il nodo "approvazione" e le due invocazioni sono il listato del libro;
# lo Stato e la costruzione del grafo attorno al nodo sono il minimo
# necessario per renderlo eseguibile. Si esegue senza API key.
# pip install langgraph
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command

class Stato(TypedDict):
    riepilogo: str
    esito: str

def approvazione(stato):
    """Nodo di approvazione: sospende il grafo prima
    dell'azione irreversibile."""
    verdetto = interrupt({
        "domanda": "Confermi la spedizione internazionale?",
        "riepilogo": stato["riepilogo"],
    })
    if verdetto != "si":
        return {"esito": "annullato dall'operatore"}
    return {"esito": "approvato"}

builder = StateGraph(Stato)
builder.add_node("approvazione", approvazione)
builder.add_edge(START, "approvazione")
builder.add_edge("approvazione", END)
grafo = builder.compile(checkpointer=InMemorySaver())

# Prima invocazione: il grafo arriva al nodo di
# approvazione, si sospende e restituisce il payload.
config = {"configurable": {"thread_id": "ordine-7"}}
sospeso = grafo.invoke({"riepilogo": "..."}, config)
print("Grafo sospeso. Payload dell'interrupt:",
      sospeso["__interrupt__"][0].value)

# Ore dopo, anche da un altro processo: la risposta
# dell'operatore riprende l'esecuzione dal checkpoint.
finale = grafo.invoke(Command(resume="si"), config)
print("Esito:", finale["esito"])
