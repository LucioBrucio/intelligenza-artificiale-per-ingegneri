"""Capitolo 17, listato "L'harness di eval": confronto con la baseline
e verdetto di rilascio.

Le funzioni di appoggio ricalcano quelle dei capitoli 11 e 16:
citazioni_valide e' l'espressione regolare sui marcatori [n], giudica
incapsula la chiamata al giudice con rubrica (saltata quando si gira
con gli stub, come nel commento del listato), aggrega fa medie per
metrica.

Esecuzione:  python harness_eval.py
(gira con gli stub: nessuna API key richiesta)
"""

import re


def citazioni_valide(risposta: str, n_fonti: int) -> bool:
    marcatori = [int(m) for m in re.findall(r"\[(\d+)\]", risposta)]
    return bool(marcatori) and all(1 <= m <= n_fonti
                                   for m in marcatori)


def giudica(caso, risposta) -> dict:
    # Fondatezza e pertinenza col giudice con rubrica (cap. 16):
    # saltato quando gira con gli stub, come nel listato.
    return {}


def aggrega(risultati) -> dict:
    somme: dict = {}
    conte: dict = {}
    for r in risultati:
        for k, v in r.items():
            somme[k] = somme.get(k, 0) + (float(v) if not
                       isinstance(v, bool) else (1.0 if v else 0.0))
            conte[k] = conte.get(k, 0) + 1
    return {k: somme[k] / conte[k] for k in somme}


def valuta_caso(caso, invoca):
    """invoca(richiesta, utente) -> stato finale del grafo.
    Con gli stub in CI, con il sistema vero in staging."""
    fin = invoca(caso["richiesta"], caso["utente"])
    if caso["tipo"] == "documentale":
        return {
          "richiamo": caso["chunk_atteso"] in fin["fonti"],
          "citazioni": citazioni_valide(fin["risposta"],
                                        len(fin["fonti"])),
          # fondatezza e pertinenza: giudice con rubrica
          # (cap. 16), saltato quando gira con gli stub
          **giudica(caso, fin["risposta"]),
        }
    if caso["tipo"] == "azione":
        p = fin.get("proposta_ticket") or {}
        return {"proposta":
                p.get("categoria") == caso["cat_attesa"]}
    # fuori ambito e avversari: la risposta attesa
    # e' un contenuto preciso, verificabile con un match
    return {"contenuto":
            caso["attesa"] in fin.get("risposta", "")}


def regressione(golden, invoca, baseline, soglie):
    agg = aggrega(valuta_caso(c, invoca) for c in golden)
    blocchi = [m for m in soglie
               if agg[m] - baseline[m] < soglie[m]]
    for m in sorted(agg):
        print(f"{m:12s} {baseline.get(m, 0):.2f} "
              f"-> {agg[m]:.2f}")
    return blocchi   # lista vuota = rilascio consentito


if __name__ == "__main__":
    from langgraph.types import Command

    from assistente import grafo

    def invoca(richiesta, utente):
        cfg = {"configurable":
               {"thread_id": f"eval-{abs(hash(richiesta))}"}}
        fin = grafo.invoke({"richiesta": richiesta,
                            "utente": utente, "passi": []}, cfg)
        # Se il grafo e' sospeso sulla conferma, in eval si
        # concede l'assenso e si osserva l'esito completo.
        if fin.get("proposta_ticket") and not fin.get("esito_azione"):
            fin = grafo.invoke(Command(resume="si"), cfg)
        return fin

    # Golden set dimostrativo: nel libro i casi sono sessanta.
    GOLDEN = [
        {"tipo": "documentale", "utente": "eval",
         "richiesta": "Qual e' la procedura per il rimborso "
                      "chilometrico?",
         "chunk_atteso": "Regolamento trasferte - Art. 4"},
        {"tipo": "azione", "utente": "eval",
         "richiesta": "Apri un ticket: il monitor e' guasto",
         "cat_attesa": "IT"},
        {"tipo": "fuori", "utente": "eval",
         "richiesta": "Che tempo fa domani?",
         "attesa": "Posso aiutarti"},
    ]
    BASELINE = {"richiamo": 1.00, "citazioni": 1.00,
                "proposta": 1.00, "contenuto": 1.00}
    SOGLIE = {"richiamo": -0.02, "citazioni": -0.02,
              "proposta": -0.001, "contenuto": -0.001}

    blocchi = regressione(GOLDEN, invoca, BASELINE, SOGLIE)
    if blocchi:
        print("BLOCCO del rilascio su:", ", ".join(blocchi))
        raise SystemExit(1)
    print("Rilascio consentito: nessuna metrica sotto soglia.")
