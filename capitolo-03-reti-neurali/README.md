# Capitolo 3 — Reti neurali

Codice del capitolo 3 di *Intelligenza artificiale per ingegneri*: la rete densa 2-3-1 (due ingressi, tre neuroni nascosti a sigmoide, una uscita a sigmoide) su cui il capitolo svolge a mano forward pass e backpropagation, e il suo addestramento completo sulla funzione XOR.

## File

| File | Descrizione |
|------|-------------|
| `verifica_backpropagation_a_mano.py` | Costruisce la rete 2-3-1 con i pesi dell'esempio a mano, esegue il forward pass e stampa uscita, perdita e i gradienti `dL/dv1` e `dL/dw11`, identici a quelli calcolati su carta. Sezione "Il ciclo di addestramento in PyTorch". |
| `addestramento_xor.py` | Addestra la rete 2-3-1 con `nn.Sequential`, `BCELoss` e `SGD` sui quattro casi della XOR per 10 000 epoche, stampando la perdita e le risposte finali. Sezione "Il ciclo di addestramento in PyTorch". |

I due listati con solo output di console riportati nel capitolo non sono file: mostrano il risultato atteso dell'esecuzione di questi script.

## Come eseguirli

```bash
pip install torch
python3 verifica_backpropagation_a_mano.py
python3 addestramento_xor.py
```

Output atteso del primo script:

```
y = 0.5998   L = 0.0801
dL/dv1  = -0.0552
dL/dw11 = -0.0141
```

Il secondo script porta la perdita da circa 0.69 a circa 0.001 e risponde `0.001` / `0.999` sui quattro casi della XOR (i valori esatti dipendono dall'inizializzazione; il seed fissato li rende ripetibili).

## Requisiti

- Python 3.12
- PyTorch (`pip install torch`)

Nessuna credenziale o servizio esterno: entrambi gli script girano interamente in locale su CPU.
