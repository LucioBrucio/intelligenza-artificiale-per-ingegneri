"""Strumentazione LangSmith del RAG del capitolo 11.

Capitolo 16, sezione "Tracing": il decoratore @traceable applicato
alla pipeline. Come nel libro, i corpi di riscrivi e rispondi sono
omessi perche' identici al capitolo 11: il listato mostra la
strumentazione, non la pipeline. L'attivazione avviene per variabili
d'ambiente, senza toccare il codice:

    export LANGSMITH_TRACING=true
    export LANGSMITH_API_KEY=...
    export LANGSMITH_PROJECT=assistente-acme
"""

# pip install langsmith
from langsmith import traceable

TOP_K = 5       # dal RAG del capitolo 11
motore = None   # il motore di ricerca in memoria del capitolo 11


@traceable(run_type="llm", name="riscrivi")
def riscrivi(domanda, cronologia=""):
    ...   # corpo identico al capitolo 11


@traceable(run_type="retriever", name="cerca")
def cerca(query, k=TOP_K):
    return motore.cerca(query, k)


@traceable(name="rispondi")   # run di tipo chain
def rispondi(domanda, cronologia=""):
    ...   # corpo identico al capitolo 11


if __name__ == "__main__":
    import os
    import sys
    if not os.environ.get("LANGSMITH_API_KEY"):
        print("Manca la variabile d'ambiente LANGSMITH_API_KEY: crea una "
              "chiave su https://smith.langchain.com (Settings -> API Keys) "
              "e imposta LANGSMITH_TRACING=true, LANGSMITH_API_KEY e "
              "LANGSMITH_PROJECT come mostrato nel capitolo.")
        sys.exit(1)
    print("Strumentazione pronta: ogni chiamata a rispondi produce un "
          "albero di trace nel project configurato. Per trace complete "
          "i corpi di riscrivi e rispondi vanno ripresi dal codice del "
          "capitolo 11 (codice/capitolo-11-rag/rag_completo.py).")
