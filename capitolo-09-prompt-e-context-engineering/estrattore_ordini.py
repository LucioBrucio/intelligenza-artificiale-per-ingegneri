"""Costruisce i tre prompt dell'estrattore di ordini del capitolo 9.

Listati della sezione "Tecniche fondamentali": lo stesso compito, estrarre
i dati strutturati da un'email d'ordine, affrontato con un prompt zero-shot,
uno few-shot e uno chain-of-thought. Il libro presenta i tre prompt come
versioni successive dello stesso programma ("stesse istruzioni del prompt
zero-shot, piu': ...", "istruzioni ed esempio come nel prompt few-shot,
piu': ..."), quindi qui sono assemblati in un unico file nell'ordine del
capitolo. Lo script legge l'email di riferimento da email_ordine.txt e
stampa i tre prompt pronti da inviare a un modello.
"""

from pathlib import Path

# Istruzioni del prompt zero-shot (sezione "Zero-shot: la sola istruzione").
ISTRUZIONI = """\
Estrai i dati dell'ordine dalla seguente email e
restituiscili come oggetto JSON con questi campi:
"cliente", "riferimento_offerta", "righe" (lista di
oggetti con "descrizione", "codice", "quantita"),
"consegna" (oggetto con "termine" e "indirizzo").
Rispondi solo con il JSON, senza altro testo."""

# Aggiunta few-shot (sezione "Few-shot: le convenzioni si mostrano"):
# le convenzioni e un esempio costruito apposta sui casi limite.
CONVENZIONI_ED_ESEMPIO = """\
Convenzioni: "codice" e' il codice articolo del
fornitore, null se assente; "quantita" e' sempre un
numero; l'unita' va nel campo "unita" ("pz" se pezzi).

Esempio.
Email:
<<<
Buongiorno, ordiniamo 2 matasse di corda (50 m l'una)
e n. 10 moschettoni cod. MK-77. Consegna in settimana
in via Roma 1, Pavia.
>>>
Risposta:
{"cliente": null, "riferimento_offerta": null,
 "righe": [
   {"descrizione": "corda, matasse da 50 m",
    "codice": null, "quantita": 2, "unita": "matasse"},
   {"descrizione": "moschettoni", "codice": "MK-77",
    "quantita": 10, "unita": "pz"}],
 "consegna": {"termine": "in settimana",
   "indirizzo": "via Roma 1, Pavia"}}"""

# Aggiunta chain-of-thought (sezione "Chain-of-thought: il procedimento
# prima del risultato"): il calcolo della data limite in giorni lavorativi.
ISTRUZIONI_DATA_LIMITE = """\
Aggiungi al JSON il campo "data_limite" (formato
AAAA-MM-GG): la data di ricezione e' lunedi' 2 marzo
2026 e il termine va calcolato in giorni lavorativi
(sabato e domenica esclusi, il conteggio parte dal
giorno successivo alla ricezione).

Prima del JSON, mostra il conteggio dei giorni uno
per uno. Poi scrivi === e il JSON su una riga nuova."""


def prompt_zero_shot(email):
    """La sola istruzione, seguita dall'email tra delimitatori."""
    return f"{ISTRUZIONI}\n\nEmail:\n<<<\n{email}\n>>>"


def prompt_few_shot(email):
    """Stesse istruzioni del prompt zero-shot, piu' convenzioni ed esempio."""
    return (
        f"{ISTRUZIONI}\n\n{CONVENZIONI_ED_ESEMPIO}\n\n"
        f"Ora estrai i dati da questa email:\n<<<\n{email}\n>>>"
    )


def prompt_chain_of_thought(email):
    """Istruzioni ed esempio come nel few-shot, piu' il calcolo della data."""
    return (
        f"{ISTRUZIONI}\n\n{CONVENZIONI_ED_ESEMPIO}\n\n"
        f"{ISTRUZIONI_DATA_LIMITE}\n\n"
        f"Ora estrai i dati da questa email:\n<<<\n{email}\n>>>"
    )


def main():
    percorso = Path(__file__).parent / "email_ordine.txt"
    email = percorso.read_text(encoding="utf-8").strip()

    prompt = [
        ("PROMPT ZERO-SHOT", prompt_zero_shot(email)),
        ("PROMPT FEW-SHOT", prompt_few_shot(email)),
        ("PROMPT CHAIN-OF-THOUGHT", prompt_chain_of_thought(email)),
    ]
    for titolo, testo in prompt:
        print("=" * 60)
        print(titolo)
        print("=" * 60)
        print(testo)
        print()


if __name__ == "__main__":
    main()
