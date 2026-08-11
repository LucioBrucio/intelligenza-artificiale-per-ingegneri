"""Le due dichiarazioni di strumento a confronto: uno strumento
e' un'API il cui utente legge ma non prova.

Capitolo 12, sezione "Tool design".
"""

import json

# CATTIVA: il modello deve indovinare tutto
DICHIARAZIONE_CATTIVA = {
    "name": "query",
    "description": "esegue una query sugli ordini",
    "parameters": {
        "type": "object",
        "properties": {
            "q": {"type": "string"}},
        "required": ["q"]}}

# BUONA: intenzione, vincoli ed esempi nella dichiarazione
DICHIARAZIONE_BUONA = {
    "name": "cerca_ordini",
    "description": (
        "Cerca ordini di acquisto per stato e anzianita'. "
        "Usalo per domande su ordini aperti, bloccati o in "
        "ritardo. Non restituisce ordini archiviati: per "
        "quelli usa cerca_archivio."),
    "parameters": {
        "type": "object",
        "properties": {
            "stato": {
                "type": "string",
                "enum": ["aperto", "bloccato", "evaso"],
                "description": "stato dell'ordine"},
            "giorni_min": {
                "type": "integer",
                "description": ("eta' minima in giorni dello "
                                "stato corrente, es. 7")}},
        "required": ["stato"]}}


if __name__ == "__main__":
    print("# CATTIVA: il modello deve indovinare tutto")
    print(json.dumps(DICHIARAZIONE_CATTIVA, indent=2, ensure_ascii=False))
    print()
    print("# BUONA: intenzione, vincoli ed esempi nella dichiarazione")
    print(json.dumps(DICHIARAZIONE_BUONA, indent=2, ensure_ascii=False))
