# Capitolo 12 - Agenti

Codice del capitolo 12 di "Intelligenza artificiale per ingegneri": un agente costruito da zero, senza framework, con registro degli strumenti, budget, memoria, loop e adattatore per il modello vero.

## File

| File | Sezione del libro | Contenuto |
|---|---|---|
| `tool_design_dichiarazioni.py` | Tool design | Le due dichiarazioni a confronto: quella cattiva (`query`) e quella buona (`cerca_ordini`). |
| `skills/solleciti-fornitori/SKILL.md` | Le skill: conoscenza procedurale su richiesta | La skill dei solleciti come file reale, con frontmatter YAML e procedura (listato "Il file SKILL.md della skill solleciti-fornitori"). |
| `skills/solleciti-fornitori/template_sollecito.md` | Le skill: conoscenza procedurale su richiesta | Il template citato al passo 3 della skill. |
| `agente_da_zero.py` | Codice: un agente da zero | I listati del nucleo assemblati in ordine: `Strumento` e `Registro`, `Budget`, `Memoria`, `Risposta`, il loop `esegui_agente`, e il collaudo con `ModelloFinto` che rigioca un copione. |
| `agente_gemini.py` | Codice: un agente da zero | L'adattatore `ModelloGemini` tra il formato neutro e google-genai, con la conferma umana da console per gli strumenti di scrittura. |

I due listati della traiettoria del sollecito (turni 1-4, sezione "Il loop agentico") sono trascrizioni dello scambio tra modello e strumenti, non codice: non sono riprodotti come file.

## Esecuzione

Senza credenziali, il collaudo del loop con il modello finto:

```bash
python3 agente_da_zero.py
```

Stampa `Bozza BZ-1 pronta per ORD-1207.` e verifica con un assert che il budget conti 3 turni e 2 azioni.

Le dichiarazioni della sezione sul tool design:

```bash
python3 tool_design_dichiarazioni.py
```

L'agente con il modello vero (richiede la chiave API e il pacchetto `google-genai`):

```bash
pip install google-genai
export GEMINI_API_KEY=<la-tua-chiave>   # https://aistudio.google.com/apikey
python3 agente_gemini.py
```

Prima di ogni `prepara_sollecito` la console chiede conferma, perché lo strumento è marcato `scrittura=True`. In alternativa alla chiave, il client si può creare su Vertex AI come nel capitolo 8: `genai.Client(vertexai=True, project="...", location="...")`.

## Requisiti

- Python 3.12
- `agente_da_zero.py` e `tool_design_dichiarazioni.py`: solo libreria standard, nessuna credenziale.
- `agente_gemini.py`: pacchetto `google-genai` e variabile d'ambiente `GEMINI_API_KEY` (o `GOOGLE_API_KEY`).
