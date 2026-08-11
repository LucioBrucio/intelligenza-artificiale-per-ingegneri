# Capitolo 11 - Retrieval-Augmented Generation

Codice del progetto di fine capitolo: un assistente documentale per l'immaginaria ACME S.p.A. che risponde alle domande dei dipendenti sui regolamenti interni, cita le fonti e si valuta con le tre metriche del capitolo (richiamo, fondatezza, pertinenza).

## File

| File | Corrisponde a |
|---|---|
| `rag_completo.py` | i cinque listati della sezione "Codice: un RAG completo", assemblati in un unico programma: configurazione e client, ingestion con chunking strutturale, motore di ricerca in memoria (dal capitolo 10), pipeline di interrogazione (riscrittura, retrieval, generazione), valutazione con LLM giudice |
| `prompt_generazione.txt` | il prompt completo della sezione "Il prompt di generazione" (le cinque regole con gli estratti di esempio), riportato come riferimento: nel programma compare in forma abbreviata nella costante `ISTRUZIONI` |
| `dati/regolamento_trasferte.txt` | base documentale di esempio citata nel capitolo (articoli 3-7 richiamati nella prova dal vivo e nel prompt di esempio) |
| `dati/regolamento_ferie.txt` | base documentale di esempio (l'art. 4 sul preavviso è il chunk atteso della seconda domanda dell'eval set) |
| `dati/policy_sicurezza.txt` | base documentale di esempio (terzo documento indicizzato) |

I documenti in `dati/` non compaiono per intero nel libro: sono ricostruiti in forma minima dai passaggi citati nel testo (rimborso chilometrico di 0,42 euro/km, massimale pasti di 50 euro in Italia e 80 all'estero, preavviso di 30 giorni per ferie di due settimane), con il formato ad articoli `Art. N: Titolo` richiesto dal chunking strutturale.

## Come eseguire

```bash
pip install google-genai numpy
export GEMINI_API_KEY=<la-tua-chiave>   # gratuita su https://aistudio.google.com/apikey
cd codice/capitolo-11-rag
python3 rag_completo.py
```

Lo script va lanciato dalla directory del capitolo, perché legge i documenti con percorsi relativi (`dati/...`). All'esecuzione indicizza i tre documenti, fa la prova dal vivo della domanda sull'auto personale (con la mappa delle citazioni) e lancia `valuta` sull'eval set di esempio, stampando richiamo@5, fondatezza e pertinenza. Nel libro l'eval set conta 30 domande; qui ne sono incluse le due mostrate nel listato.

## Requisiti

- Python 3.12
- pacchetti: `google-genai`, `numpy`
- variabile d'ambiente `GEMINI_API_KEY` (o `GOOGLE_API_KEY`): senza chiave lo script stampa come ottenerla ed esce
