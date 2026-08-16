# Capitolo 6 — Architettura Transformer (mini-GPT)

Codice del capitolo 6 del libro *Intelligenza artificiale per ingegneri*: un GPT-2 in miniatura, completo e funzionante, scritto in PyTorch componente per componente.

## File

| File | Descrizione |
|------|-------------|
| `mini_gpt.py` | Il mini-GPT completo: configurazione (`ConfigGPT`), multi-head attention causale (`CausalSelfAttention`), feed-forward e blocco Transformer (`MLP`, `Blocco`), modello con weight tying (`MiniGPT`), forward pass con cross-entropy, generazione autoregressiva (`genera`) e collaudo finale. Mini-GPT parti 1-6, sezione "Scrivere un mini-GPT completo". |

I sei listati del libro sono parti dello stesso programma e sono assemblati qui in un unico file, nell'ordine del capitolo. Il collaudo (parte 6) è racchiuso in un blocco `if __name__ == "__main__":`. Il listato con l'output di esecuzione non è un file di codice e non è riprodotto.

## Come eseguire

```bash
pip install torch
python3 mini_gpt.py
```

Gira su una CPU qualunque, in pochi secondi. L'output atteso (con il seed 42 del listato):

```
parametri: 834304
perdita iniziale: 5.5538   attesa: 5.5452
[0, 95, 196, 49, 75, 157, 86, 79, 160]
[0, 216, 216, 216, 216, 216, 216, 216, 216]
```

Le tre verifiche del capitolo: il conteggio dei parametri, la perdita iniziale vicina a ln(256) ≈ 5,5452 (il controllo di sanità della testa di output), e le due generazioni del modello non addestrato: byte a caso con il campionamento, ripetizione del token 216 con il greedy (T = 0).

I valori esatti dei token generati possono variare tra versioni di PyTorch e piattaforme diverse, per le ragioni discusse nel capitolo a proposito del non determinismo in virgola mobile.

## Requisiti

- Python 3.12
- `torch` (PyTorch), unica dipendenza esterna
- Nessuna credenziale API, nessun servizio esterno: tutto gira in locale
