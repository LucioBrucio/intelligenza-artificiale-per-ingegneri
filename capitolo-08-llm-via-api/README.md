# Capitolo 8 - Usare gli LLM via API

Codice dei listati del capitolo 8: chiamate a un LLM tramite l'SDK Python `google-genai` (Gemini API), dalla chiamata minima fino a structured output, function calling, streaming, client robusto e input multimodale.

## File

| File | Descrizione |
|---|---|
| `chiamata_minima.py` | La chiamata minima completa a un LLM. Sezione "Anatomia di una chiamata". |
| `conversazione_stateless.py` | La storia del dialogo mantenuta dal client. Sezione "La conversazione la mantieni tu". |
| `troncamento_storia.py` | Funzione `tronca_storia` con `count_tokens` per restare nel context window. Sezione "Il context window come risorsa". |
| `parametri_generazione.py` | Configurazione con temperature, top_p, max_output_tokens, stop_sequences e thinking_budget. Sezione "Parametri di generazione". |
| `estrazione_ordine.py` | Structured output: schema Pydantic e chiamata vincolata, poi retry con feedback, assemblati in un unico programma. Sezione "Structured output". |
| `assistente_magazzino.py` | Function calling: funzione e dichiarazione, poi il ciclo di invocazione; crea da solo `magazzino.db` con il dato di esempio del capitolo. Sezione "Function calling". |
| `streaming.py` | Generazione in streaming. Sezione "Streaming e robustezza". |
| `client_robusto.py` | Timeout, classificazione degli errori e backoff esponenziale con jitter. Sottosezione "Guasti, retry e backoff". |
| `estrazione_fattura_pdf.py` | PDF in input, JSON validato in uscita e verifica aritmetica a valle. Sezione "Multimodalita'". |

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
