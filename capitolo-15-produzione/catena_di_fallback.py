"""Catena di fallback tra modelli e provider, capitolo 15,
sezione "Affidabilita'".

La catena vive nel gateway: prima il modello grande, poi il piccolo
dello stesso provider, infine un provider indipendente. Le costanti
dei modelli sono quelle del listato sul routing per complessita'.
"""

from routing_per_complessita import MODELLO_GRANDE, MODELLO_PICCOLO


class ErroreTransitorio(Exception):
    """Errore temporaneo del provider (quota, capacita', rete):
    ha senso passare al gradino successivo della catena."""


CATENA_FALLBACK = [
    ("vertex", MODELLO_GRANDE),     # percorso primario
    ("vertex", MODELLO_PICCOLO),    # capacita' ridotta, stesso provider
    ("provider_b", "modello-b"),    # provider indipendente
]

def genera_con_fallback(richiesta, chiama, registra):
    """chiama() esegue la chiamata vera; registra() alimenta
    metriche e allarmi. Entrambe iniettate, testabili con stub."""
    ultimo_errore = None
    for provider, modello in CATENA_FALLBACK:
        try:
            risposta = chiama(provider, modello, richiesta)
            registra(provider, modello, ok=True)
            return risposta
        except ErroreTransitorio as errore:
            registra(provider, modello, ok=False)
            ultimo_errore = errore
    raise ultimo_errore


if __name__ == "__main__":
    # Stub dimostrativi: il percorso primario e' fuori servizio,
    # il secondo gradino risponde.
    def chiama_stub(provider, modello, richiesta):
        if modello == MODELLO_GRANDE:
            raise ErroreTransitorio("quota esaurita sul modello di punta")
        return f"[risposta di {provider}/{modello}]"

    def registra_stub(provider, modello, ok):
        esito = "ok" if ok else "fallito"
        print(f"registro: {provider}/{modello} -> {esito}")

    risposta = genera_con_fallback("Qual e' lo stato dell'ordine 812?",
                                   chiama_stub, registra_stub)
    print("risposta:", risposta)
