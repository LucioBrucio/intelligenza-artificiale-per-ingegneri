"""Routing per complessita', capitolo 15, sezione "Costi".

Un classificatore economico sul modello piccolo smista le richieste:
le semplici al modello piccolo, le complesse al grande. La logica e'
separata dalle chiamate: classifica e genera sono iniettate.
"""

# I nomi dei modelli evolvono: costanti da aggiornare.
MODELLO_GRANDE = "gemini-2.5-pro"
MODELLO_PICCOLO = "gemini-2.5-flash"

PROMPT_ROUTER = """Classifica la richiesta di un utente.
SEMPLICE: domanda su fatti, stati, procedure note.
COMPLESSA: ragionamento su piu' fonti, redazione di testi
articolati, casi ambigui o inusuali.
Nel dubbio rispondi COMPLESSA.
Rispondi con una sola parola: SEMPLICE o COMPLESSA."""

def instrada(richiesta, classifica, genera):
    """Smista la richiesta sul modello adeguato.
    classifica e genera sono iniettate: nei test sono stub,
    in produzione chiamano il gateway."""
    verdetto = classifica(MODELLO_PICCOLO, PROMPT_ROUTER,
                          richiesta[:2000])   # basta l'inizio
    modello = (MODELLO_PICCOLO if verdetto.strip() == "SEMPLICE"
               else MODELLO_GRANDE)
    return genera(modello, richiesta), modello


if __name__ == "__main__":
    # Stub dimostrativi: in produzione le due funzioni
    # chiamano il gateway LLM.
    def classifica_stub(modello, prompt, richiesta):
        indizi_complessi = ("confronta", "analizza", "redigi")
        testo = richiesta.lower()
        if any(indizio in testo for indizio in indizi_complessi):
            return "COMPLESSA"
        return "SEMPLICE"

    def genera_stub(modello, richiesta):
        return f"[risposta di {modello}]"

    richieste = [
        "A che ora apre il magazzino di Verona?",
        "Qual e' lo stato della spedizione 4517?",
        "Confronta le due offerte di trasporto e redigi una raccomandazione.",
    ]
    for richiesta in richieste:
        risposta, modello = instrada(richiesta, classifica_stub, genera_stub)
        print(f"{modello:18} <- {richiesta}")
