"""Cache semantica delle risposte, capitolo 15, sezione "Latenza".

La scansione lineare e' scelta per chiarezza: in produzione l'indice
delle domande vive in uno dei vector database del capitolo 10.
"""

import math


class CacheSemantica:
    """Cache di risposte indicizzata per similarita'
    semantica della domanda."""
    def __init__(self, embed, soglia=0.92):
        self.embed = embed    # funzione testo -> vettore normalizzato
        self.soglia = soglia
        self.voci = []        # coppie (vettore, risposta)

    def cerca(self, domanda):
        v = self.embed(domanda)
        migliore, punteggio = None, 0.0
        for vettore, risposta in self.voci:
            # coseno = prodotto scalare: vettori normalizzati
            s = sum(a * b for a, b in zip(v, vettore))
            if s > punteggio:
                migliore, punteggio = risposta, s
        return migliore if punteggio >= self.soglia else None

    def salva(self, domanda, risposta):
        self.voci.append((self.embed(domanda), risposta))


def embed_dimostrativo(testo):
    """Embedding giocattolo a sacco di parole, normalizzato.
    Serve solo a rendere eseguibile l'esempio: in produzione
    embed e' un modello di embedding vero (capitolo 10)."""
    dimensioni = 64
    v = [0.0] * dimensioni
    for parola in testo.lower().split():
        v[hash(parola) % dimensioni] += 1.0
    norma = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / norma for x in v]


if __name__ == "__main__":
    cache = CacheSemantica(embed_dimostrativo)
    cache.salva("quali sono gli orari di apertura del negozio",
                "Il negozio e' aperto dal lunedi' al sabato, 9-19.")

    # Stessa domanda con ordine diverso delle parole: hit.
    domanda_simile = "gli orari di apertura del negozio quali sono"
    print("domanda simile  ->", cache.cerca(domanda_simile))

    # Domanda diversa: sotto soglia, nessuna risposta dalla cache.
    domanda_diversa = "posso pagare alla consegna?"
    print("domanda diversa ->", cache.cerca(domanda_diversa))
