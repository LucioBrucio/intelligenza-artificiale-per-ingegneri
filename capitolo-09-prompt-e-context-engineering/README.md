# Capitolo 9 - Prompt e context engineering

Codice e materiali dei listati del capitolo 9, dedicato alle tecniche fondamentali di prompt engineering (zero-shot, few-shot, chain-of-thought sullo stesso compito di estrazione da email d'ordine), al context engineering, al prompt caching e alla prompt injection.

## File

| File | Descrizione |
|---|---|
| `email_ordine.txt` | L'email di riferimento di Meccanica Rossi S.r.l. che accompagna la prima meta' del capitolo. Non e' codice: e' il dato di ingresso dei tre prompt dell'estrattore. Sezione "Tecniche fondamentali". |
| `estrattore_ordini.py` | I tre prompt dell'estrattore di ordini (zero-shot, few-shot, chain-of-thought), assemblati come versioni successive dello stesso programma; legge `email_ordine.txt` e stampa i tre prompt completi, pronti da inviare a un modello. Sezioni "Zero-shot", "Few-shot", "Chain-of-thought". |
| `cache_esplicita_gemini.py` | Gestione esplicita della cache con l'SDK di Google: il prefisso stabile viene caricato una volta sola con `client.caches.create` e riusato dalle richieste successive tramite `cached_content`, con i dati dell'assistente di supporto tecnico del testo. Sezione "Prompt caching". |
| `email_injection_indiretta.txt` | L'email all'apparenza innocua che nasconde, dopo la firma, un'istruzione ostile per l'assistente AI. E' il dato d'attacco dell'injection indiretta: non va eseguita, va studiata. Sezione "Prompt injection". |
| `prompt/antipattern_cortesia.txt` | Primo anti-pattern: la cortesia al posto della precisione ("nel modo migliore possibile", "abbastanza sintetico"). Sezione "Pattern e anti-pattern". |
| `prompt/riscrittura_vincoli_misurabili.txt` | Riscrittura del primo anti-pattern: vincoli misurabili (3-5 punti, 20 parole), criterio di inclusione e specifica del caso vuoto. Sezione "Pattern e anti-pattern". |
| `prompt/antipattern_negazioni.txt` | Secondo anti-pattern: la negazione accumulata, una lista di divieti che non dice cosa fare. Sezione "Pattern e anti-pattern". |
| `prompt/riscrittura_positiva.txt` | Riscrittura del secondo anti-pattern: gli stessi vincoli espressi come comportamento desiderato. Sezione "Pattern e anti-pattern". |

I due listati di output del modello (il JSON prodotto dal prompt zero-shot e il conteggio dei giorni del chain-of-thought) sono trascrizioni di risposte tipiche, non codice, e non sono riprodotti come file.

## Come eseguire

1. Stampare i tre prompt dell'estrattore (nessuna dipendenza, nessuna chiave API):

   ```bash
   python3 estrattore_ordini.py
   ```

   I prompt stampati si possono incollare in qualunque interfaccia di chat o inviare via API per riprodurre gli esperimenti del capitolo.

2. Provare il prompt caching esplicito con Gemini:

   ```bash
   pip install google-genai
   export GOOGLE_API_KEY="la-tua-chiave"
   python3 cache_esplicita_gemini.py
   ```

   La chiave si crea su https://aistudio.google.com/apikey; se manca, lo script stampa le istruzioni ed esce con codice 1. Nota: la creazione esplicita di una cache richiede un contenuto di dimensione minima (migliaia di token a seconda del modello), quindi con i dati d'esempio in miniatura la chiamata puo' essere rifiutata dal servizio; per la prova reale va usato un estratto lungo di documentazione, come descritto nel conto svolto del capitolo.

I file in `prompt/` e le due email sono materiali di testo da leggere o da incollare nei propri esperimenti, in linea con la sezione "Prompt come codice": i prompt vivono in file dedicati e versionati, non annegati tra le stringhe della logica applicativa.

## Requisiti

- Python 3.12
- Solo per `cache_esplicita_gemini.py`: pacchetto pip `google-genai` e variabile d'ambiente `GOOGLE_API_KEY`
