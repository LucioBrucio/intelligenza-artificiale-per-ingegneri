# Intelligenza artificiale per ingegneri — il codice

Tutto il codice sorgente del libro **"Intelligenza artificiale per
ingegneri. Transformer, LLM, RAG e agenti AI: dai fondamenti al codice"**
di Luciano Salemme, organizzato per capitolo e pronto da eseguire.

Ogni directory corrisponde a un capitolo del libro e contiene un README
con la mappa tra i file e i listati, le istruzioni di esecuzione e i
requisiti specifici.

## Struttura

| Directory | Capitolo | Gira offline? |
|-----------|----------|---------------|
| `capitolo-02-fondamenti-matematici` | 2. Fondamenti matematici | si |
| `capitolo-03-reti-neurali` | 3. Reti neurali | si |
| `capitolo-04-token-ed-embedding` | 4. Token ed embedding | si (download modello al primo avvio) |
| `capitolo-05-attention` | 5. Il meccanismo di attention | si |
| `capitolo-06-transformer` | 6. L'architettura Transformer (mini-GPT) | si |
| `capitolo-07-dal-transformer-agli-llm` | 7. Dal Transformer agli LLM | serve Ollama in locale |
| `capitolo-08-llm-via-api` | 8. Usare gli LLM via API | serve `GEMINI_API_KEY` |
| `capitolo-09-prompt-e-context-engineering` | 9. Prompt e context engineering | in parte (caching: API key) |
| `capitolo-10-ricerca-semantica` | 10. Ricerca semantica e vector database | si (download modello al primo avvio) |
| `capitolo-11-rag` | 11. Retrieval-Augmented Generation | serve `GEMINI_API_KEY` |
| `capitolo-12-agenti` | 12. Agenti | si (adattatore Gemini: API key) |
| `capitolo-13-mcp` | 13. Il Model Context Protocol | si |
| `capitolo-14-multi-agente` | 14. Sistemi multi-agente | si (percorso Vertex: API key) |
| `capitolo-15-produzione` | 15. LLM in produzione | si |
| `capitolo-16-observability` | 16. Observability e valutazione | si (tracing: LangSmith) |
| `capitolo-17-caso-di-studio` | 17. Caso di studio | si (con gli stub, come nel libro) |

## Prerequisiti

- **Python 3.12 o superiore** (il codice e' testato con Python 3.12)
- circa 3 GB di spazio disco per le dipendenze (PyTorch e' la piu'
  pesante) e circa 500 MB per il modello di embedding scaricato al
  primo avvio dei capitoli 4 e 10

## Installazione

```bash
git clone https://github.com/LucioBrucio/intelligenza-artificiale-per-ingegneri.git
cd intelligenza-artificiale-per-ingegneri
python3 -m venv .venv
source .venv/bin/activate        # su Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Le versioni con cui il codice e' stato testato sono in
`requirements.txt`.

## Credenziali (solo per i capitoli che chiamano le API)

I capitoli 8, 9 (caching), 11, 12 (adattatore Gemini) e 14 (percorso
Vertex) chiamano l'API Gemini. Serve una chiave, gratuita per gli
esperimenti del libro, da <https://aistudio.google.com>:

```bash
export GEMINI_API_KEY="la-tua-chiave"
```

Ogni script controlla la variabile all'avvio: se manca, spiega come
ottenerla ed esce senza errori criptici. Il capitolo 7 usa invece
[Ollama](https://ollama.com) in locale (nessuna chiave); il tracing del
capitolo 16 richiede un account [LangSmith](https://smith.langchain.com)
gratuito.

## Da dove cominciare

```bash
cd capitolo-06-transformer
python mini_gpt.py        # un GPT-2 completo in 150 righe, su CPU
```

## Errori e miglioramenti

Se trovi un errore o hai un'idea per migliorare un esempio, apri una
issue o una pull request: sara' un contributo prezioso per chi legge
dopo di te.
