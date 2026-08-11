"""Pipeline di valutazione e regressione per il RAG di ACME.

Capitolo 16, sezione "Codice: una pipeline di eval": golden set con
esiti attesi, verifica programmatica delle citazioni, giudice LLM con
rubrica, report di regressione con soglie di blocco. La funzione di
risposta e' un parametro: si passa la rispondi del capitolo 11 per
valutare il sistema vero (--con-api), o uno stub che rigioca risposte
registrate quando sotto test e' la pipeline stessa.

Uso, dalla directory del capitolo:
    python3 pipeline_eval.py             # CI: giudice stub, nessuna API key
    python3 pipeline_eval.py --con-api   # giudice Gemini (GEMINI_API_KEY)

Codice di uscita: 0 se il rilascio puo' procedere, 1 se e' bloccato.
"""

import re, json

from google import genai
from google.genai import types

# Configurazione. Il giudice e' uno strumento di misura:
# il suo modello e la sua versione si congelano durante
# i confronti e si registrano accanto ai risultati.
MODELLO_GIUDICE  = "gemini-2.5-flash"  # i nomi evolvono
VERSIONE_GIUDICE = "giudice-v2"

SOGLIE = {  # peggioramento massimo tollerato per metrica
    "richiamo": 0.02, "citazioni": 0.02,
    "fondata": 0.02, "pertinente": 0.04,
}

RIFIUTO = ("Non ho trovato questa informazione "
           "nei documenti disponibili.")

GOLDEN_SET = [
    {"id": "G01",
     "domanda": ("Qual e' il rimborso per l'uso "
                 "dell'auto personale?"),
     "chunk_atteso": "Regolamento trasferte - Art. 5",
     "tipo": "normale"},
    {"id": "G02",
     "domanda": ("Posso lavorare in smart working "
                 "dall'estero?"),
     "chunk_atteso": None,   # non e' nei documenti:
     "tipo": "senza_risposta"},  # atteso il rifiuto
    # ... 50 casi, campionati dal traffico e annotati
    # come descritto nella sezione sugli eval set
]


def citazioni_valide(risposta, n_estratti):
    """Ogni [n] citato deve corrispondere a un estratto
    davvero fornito. Verifica esatta, senza modello."""
    if risposta.strip() == RIFIUTO:
        return True   # il rifiuto non cita, ed e' corretto
    numeri = {int(n) for n in re.findall(r"\[(\d+)\]",
                                         risposta)}
    return (len(numeri) > 0 and
            all(1 <= n <= n_estratti for n in numeri))


RUBRICA = """Valuta la risposta di un assistente
documentale.
Domanda: {domanda}
Estratti forniti all'assistente:
{estratti}
Risposta da valutare: {risposta}

Criteri, in ordine di priorita':
1. FONDATA: ogni affermazione e' sostenuta dagli
   estratti. Un rifiuto esplicito conta come fondato.
   Una sola affermazione non sostenuta rende la
   risposta non fondata. La lunghezza non e' un merito.
2. PERTINENTE: la risposta affronta cio' che la
   domanda chiede.
Prima elenca le eventuali affermazioni non sostenute,
poi rispondi SOLO in JSON:
{{"non_sostenute": [...], "fondata": true|false,
  "pertinente": true|false}}"""


class GiudiceGemini:
    """Il giudice vero: LLM con rubrica, JSON in uscita."""

    def __init__(self, client, modello=MODELLO_GIUDICE):
        self.client, self.modello = client, modello

    def valuta(self, domanda, estratti, risposta):
        prompt = RUBRICA.format(
            domanda=domanda,
            estratti="\n".join(c["testo"] for c in estratti),
            risposta=risposta)
        r = self.client.models.generate_content(
            model=self.modello, contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.0,
                response_mime_type="application/json"))
        v = json.loads(r.text)
        return {"fondata": bool(v["fondata"]),
                "pertinente": bool(v["pertinente"])}

class GiudiceStub:
    """Giudice deterministico per CI e sviluppo: fondata
    se ogni numero della risposta compare negli estratti,
    pertinente se la risposta non e' un rifiuto."""

    def valuta(self, domanda, estratti, risposta):
        if risposta.strip() == RIFIUTO:
            return {"fondata": True, "pertinente": False}
        testo = " ".join(c["testo"] for c in estratti)
        numeri = re.findall(r"\d+(?:,\d+)?", risposta)
        return {"fondata": all(n in testo for n in numeri),
                "pertinente": True}


def valuta_sistema(rispondi_fn, golden_set, giudice):
    """Esegue il sistema su ogni caso e calcola le
    metriche, per caso e aggregate."""
    casi = []
    for caso in golden_set:
        risposta, estratti = rispondi_fn(caso["domanda"])
        giudizio = giudice.valuta(caso["domanda"],
                                  estratti, risposta)
        casi.append({
            "id": caso["id"],
            "richiamo": (caso["chunk_atteso"] is None or
                         any(c["id"] == caso["chunk_atteso"]
                             for c in estratti)),
            "citazioni": citazioni_valide(risposta,
                                          len(estratti)),
            "fondata": giudizio["fondata"],
            "pertinente": giudizio["pertinente"],
        })
    n = len(casi)
    metriche = {m: sum(c[m] for c in casi) / n
                for m in SOGLIE}
    return {"giudice": VERSIONE_GIUDICE,
            "casi": casi, "metriche": metriche}


def report_regressione(baseline, candidata, soglie):
    """Confronta due esecuzioni sullo stesso golden set.
    Restituisce True se il rilascio puo' procedere."""
    assert baseline["giudice"] == candidata["giudice"], \
        "giudici diversi: confronto non valido"
    blocco = False
    print(f"{'metrica':<12}{'base':>6}{'cand':>6}"
          f"{'delta':>8}   esito")
    for m, base in baseline["metriche"].items():
        cand = candidata["metriche"][m]
        delta = cand - base
        ko = delta < -soglie[m]
        blocco = blocco or ko
        print(f"{m:<12}{base:>6.2f}{cand:>6.2f}"
              f"{delta:>+8.2f}   "
              f"{'BLOCCO' if ko else 'ok'}")
    # diff per caso: chi ha cambiato esito, e dove
    for b, c in zip(baseline["casi"], candidata["casi"]):
        for m in soglie:
            if b[m] and not c[m]:
                print(f"  peggiorato {c['id']} su {m}")
    return not blocco

if __name__ == "__main__":
    import os
    import sys
    if "--con-api" in sys.argv:
        if not (os.environ.get("GEMINI_API_KEY")
                or os.environ.get("GOOGLE_API_KEY")):
            print("Manca la variabile d'ambiente GEMINI_API_KEY: crea una "
                  "chiave gratuita su https://aistudio.google.com/apikey "
                  "e imposta export GEMINI_API_KEY=<la-tua-chiave>")
            sys.exit(1)
        client = genai.Client()
        giudice = GiudiceGemini(client)
        try:
            esegui = rispondi          # dal capitolo 11
        except NameError:
            print("Con --con-api serve la funzione rispondi del RAG del "
                  "capitolo 11 (codice/capitolo-11-rag/rag_completo.py): "
                  "importala in questo file per valutare il sistema vero.")
            sys.exit(1)
    else:                          # CI: nessuna API key
        giudice = GiudiceStub()
        reg = json.load(open("eval/registrazioni.json"))
        esegui = lambda d: (reg[d]["risposta"],
                            reg[d]["estratti"])
    candidata = valuta_sistema(esegui, GOLDEN_SET, giudice)
    baseline = json.load(open("eval/baseline_v1_4.json"))
    ok = report_regressione(baseline, candidata, SOGLIE)
    json.dump(candidata, open("eval/candidata.json", "w"))
    sys.exit(0 if ok else 1)
