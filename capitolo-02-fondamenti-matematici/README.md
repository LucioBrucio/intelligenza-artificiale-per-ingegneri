# Capitolo 2 - Fondamenti matematici

Codice della sezione "Gli strumenti: NumPy e PyTorch" del capitolo 2: gli esempi svolti a mano nel capitolo (similarita coseno, prodotto matriciale, discesa del gradiente, softmax e cross-entropy) tradotti in NumPy e PyTorch, cosi che ogni risultato possa essere verificato riga per riga.

## File

| File | Descrizione |
|------|-------------|
| `esempi_numpy.py` | Prodotto scalare, norma e similarita coseno, prodotto matrice-vettore, broadcasting e tre passi di discesa del gradiente in NumPy. Sottosezioni "Tensori, array e operazioni vettorializzate", "Broadcasting" e "La discesa del gradiente in codice". |
| `esempi_pytorch.py` | Gradiente automatico con autograd, softmax con temperatura e cross-entropy in PyTorch. Sottosezione "PyTorch: tensori con il gradiente incorporato". |

## Come eseguirli

```bash
pip install numpy torch

python3 esempi_numpy.py
python3 esempi_pytorch.py
```

## Requisiti

- Python 3.12
- `numpy` per `esempi_numpy.py`
- `torch` per `esempi_pytorch.py`

Nessuna credenziale o servizio esterno: tutti gli script girano in locale e stampano gli stessi numeri calcolati a mano nel capitolo.
