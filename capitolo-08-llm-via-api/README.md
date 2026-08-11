# Capitolo 8 - Usare gli LLM via API

Codice dei listati del capitolo 8: chiamate a un LLM tramite l'SDK Python `google-genai` (Gemini API), dalla chiamata minima fino a structured output, function calling, streaming, client robusto e input multimodale.

## File

| File | Listato / sezione del libro |
|---|---|
| `chiamata_minima.py` | Sezione "Anatomia di una chiamata": la chiamata minima completa |
| `conversazione_stateless.py` | Sezione "La conversazione la mantieni tu": la storia del dialogo gestita dal client |
| `troncamento_storia.py` | Sezione "Il context window come risorsa": funzione `tronca_storia` con `count_tokens` |
| `parametri_generazione.py` | Sezione "Parametri di generazione": la configurazione con temperature, top_p, max_output_tokens, stop_sequences e thinking_budget |
| `estrazione_ordine.py` | Sezione "Structured output": i due listati (schema Pydantic + chiamata vincolata, poi retry con feedback) assemblati in un programma unico |
| `assistente_magazzino.py` | Sezione "Function calling": i due listati (funzione e dichiarazione, poi il ciclo di invocazione) assemblati; crea da solo `magazzino.db` con il dato di esempio del capitolo |
| `streaming.py` | Sezione "Streaming e robustezza": generazione in streaming |
| `client_robusto.py` | Sottosezione "Guasti, retry e backoff": timeout, classificazione errori, backoff esponenziale con jitter |
| `estrazione_fattura_pdf.py` | Sezione "Multimodalita'": PDF in input, JSON validato in uscita, verifica aritmetica a valle |

## Come eseguire

Requisiti: Python 3.12 e i pacchetti

```bash
pip install google-genai pydantic
```

Tutti gli script chiamano la Gemini API e leggono la chiave dalla variabile d'ambiente `GEMINI_API_KEY` (chiave gratuita su https://aistudio.google.com/apikey):

```bash
export GEMINI_API_KEY=<la-tua-chiave>
python3 chiamata_minima.py
```

Se la variabile manca, ogni script lo segnala ed esce con codice 1.

Note particolari:

- `assistente_magazzino.py` crea al primo avvio il database `magazzino.db` con l'articolo di esempio VLV-2041 (42 pezzi in corsia B3), come nel testo del capitolo.
- `estrazione_fattura_pdf.py` richiede un file `fattura_1042.pdf` nella directory corrente; senza, si ferma con un messaggio.
- Per usare Vertex AI al posto della Gemini API, costruire il client come indicato nei commenti: `genai.Client(vertexai=True, project="...", location="...")`.

## Dipendenze

- `google-genai` (SDK ufficiale Google per Gemini)
- `pydantic` (schemi e validazione in `estrazione_ordine.py` e `estrazione_fattura_pdf.py`)
