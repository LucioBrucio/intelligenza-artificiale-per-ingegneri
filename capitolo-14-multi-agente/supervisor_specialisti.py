# Capitolo 14, sezione "Codice: supervisor e specialisti": un supervisor
# che coordina due specialisti (analista e redattore) su un grafo
# LangGraph con stato condiviso tipizzato e checkpoint. Le chiamate al
# modello passano da un'interfaccia con due implementazioni: quella vera
# su Vertex AI (ModelloVertex) e uno stub deterministico (ModelloFinto)
# che permette di eseguire e testare l'intero grafo senza API key.
# pip install langgraph google-genai
import os
import sys
from typing import Annotated
from typing_extensions import TypedDict
from operator import add

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

MODELLO = "gemini-2.5-flash"

class ModelloVertex:
    """Implementazione reale: Gemini via google-genai,
    come nel capitolo 8."""
    def __init__(self):
        if not os.environ.get("GOOGLE_API_KEY"):
            print("Manca la variabile GOOGLE_API_KEY: crea una chiave "
                  "API su https://aistudio.google.com/apikey e "
                  "impostala con: export GOOGLE_API_KEY=<chiave>")
            sys.exit(1)
        from google import genai
        # su Vertex AI: genai.Client(vertexai=True,
        #   project="...", location="...")
        self.client = genai.Client()

    def genera(self, prompt: str) -> str:
        r = self.client.models.generate_content(
            model=MODELLO, contents=prompt)
        return r.text

class ModelloFinto:
    """Stub deterministico: risposte plausibili cablate.
    L'intelligenza e' finta, la struttura del sistema
    e' quella vera, ed e' cio' che qui vogliamo testare."""
    def genera(self, prompt: str) -> str:
        if prompt.startswith("Sei il supervisor"):
            # Politica di delega minima: prima l'analisi,
            # poi la bozza, poi fine.
            if "analisi: mancante" in prompt:
                return "analista\nRaccogli i punti chiave."
            if "bozza: mancante" in prompt:
                return "redattore\nScrivi usando l'analisi."
            return "FINE"
        if prompt.startswith("Sei l'analista"):
            return "Punti chiave: A, B, C. (analisi finta)"
        return "Testo che sviluppa A, B e C. (bozza finta)"

modello = ModelloFinto()  # in produzione: ModelloVertex()

class Stato(TypedDict):
    richiesta: str   # il compito dell'utente
    analisi: str     # prodotto dell'analista
    bozza: str       # prodotto del redattore
    prossimo: str    # decisione del supervisor
    delega: str      # istruzione per lo specialista
    passi: Annotated[list[str], add]  # traccia

def nodo_supervisor(stato: Stato):
    # Al supervisor va una fotografia dello stato,
    # non i contenuti interi.
    analisi = "pronta" if stato["analisi"] else "mancante"
    bozza = "pronta" if stato["bozza"] else "mancante"
    prompt = (
        "Sei il supervisor di una squadra di agenti.\n"
        "Specialisti disponibili:\n"
        "- analista: raccoglie e sintetizza i fatti\n"
        "- redattore: scrive il testo finale\n"
        f"Compito: {stato['richiesta']}\n"
        "Stato del lavoro:\n"
        f"- analisi: {analisi}\n"
        f"- bozza: {bozza}\n"
        "Rispondi con il nome dello specialista da attivare "
        "e, a capo, l'istruzione per lui; oppure FINE.")
    righe = modello.genera(prompt).strip().splitlines()
    prossimo = righe[0].strip().lower()
    delega = "\n".join(righe[1:]).strip()
    return {"prossimo": prossimo, "delega": delega,
            "passi": [f"supervisor -> {prossimo}"]}

def nodo_analista(stato: Stato):
    prompt = ("Sei l'analista. Istruzione del supervisor: "
              f"{stato['delega']}\n"
              f"Compito generale: {stato['richiesta']}")
    return {"analisi": modello.genera(prompt),
            "passi": ["analista"]}

def nodo_redattore(stato: Stato):
    prompt = ("Sei il redattore. Istruzione del supervisor: "
              f"{stato['delega']}\n"
              f"Analisi disponibile:\n{stato['analisi']}")
    return {"bozza": modello.genera(prompt),
            "passi": ["redattore"]}

def smista(stato: Stato) -> str:
    """Arco condizionale: dal supervisor allo specialista
    scelto, o alla fine."""
    if stato["prossimo"] == "fine":
        return END
    return stato["prossimo"]

builder = StateGraph(Stato)
builder.add_node("supervisor", nodo_supervisor)
builder.add_node("analista", nodo_analista)
builder.add_node("redattore", nodo_redattore)

builder.add_edge(START, "supervisor")
builder.add_conditional_edges("supervisor", smista)
builder.add_edge("analista", "supervisor")
builder.add_edge("redattore", "supervisor")

grafo = builder.compile(checkpointer=InMemorySaver())

config = {"configurable": {"thread_id": "nota-2026-081"}}
finale = grafo.invoke(
    {"richiesta": ("una nota di sintesi sui sistemi "
                   "multi-agente per il comitato tecnico"),
     "analisi": "", "bozza": "",
     "prossimo": "", "delega": "", "passi": []},
    config)

print("Traccia:", " | ".join(finale["passi"]))
print("Bozza finale:", finale["bozza"])
