# Capitolo 5 — Il meccanismo di attention

Codice del capitolo 5 di *Intelligenza artificiale per ingegneri*: la scaled dot-product attention implementata da zero in PyTorch, che replica cifra per cifra l'esempio numerico svolto a mano nel capitolo sulla frase "il gatto dorme".

## File

| File | Contenuto | Listati del libro |
|------|-----------|-------------------|
| `attention_da_zero.py` | Embedding e proiezioni Q, K, V; scaled dot-product attention; funzione `attention` con maschera causale opzionale; verifica sull'esempio a mano | 5.1, 5.2, 5.3 e 5.4 (sezione "Implementazione da zero in PyTorch") |

I quattro listati del capitolo sono parti dello stesso programma e sono assemblati in un unico file, nell'ordine in cui compaiono nel libro. I listati di solo output di console non sono riprodotti: sono ciò che lo script stampa.

## Come eseguire

```bash
pip install torch
python3 attention_da_zero.py
```

Lo script stampa, nell'ordine: le matrici Q, K e V; la matrice dei pesi di attention e gli output Z dell'attention bidirezionale; la matrice dei pesi e gli output della variante causale. I valori coincidono con quelli calcolati a mano nel capitolo (ad esempio i pesi di "dorme": 0,2840, 0,5760, 0,1400).

## Requisiti

- Python 3.12
- `torch` (PyTorch)

Nessuna chiave API o servizio esterno: tutto gira in locale su CPU.
