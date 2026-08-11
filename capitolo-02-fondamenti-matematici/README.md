# Capitolo 2 - Fondamenti matematici

Codice della sezione "Gli strumenti: NumPy e PyTorch" del capitolo 2: gli esempi svolti a mano nel capitolo (similarita coseno, prodotto matriciale, discesa del gradiente, softmax e cross-entropy) tradotti in NumPy e PyTorch, cosi che ogni risultato possa essere verificato riga per riga.

## File

| File | Contenuto | Listati del libro |
|------|-----------|-------------------|
| `esempi_numpy.py` | Prodotto scalare, norma e similarita coseno sui tre documenti di esempio; prodotto matrice per vettore e broadcasting; tre passi di discesa del gradiente su f(x, y) = x^2 + 4y^2 | Listati delle sottosezioni "Tensori, array e operazioni vettorializzate", "Broadcasting" e "La discesa del gradiente in codice" (assemblati: nel libro formano un'unica sessione NumPy) |
| `esempi_pytorch.py` | Gradiente automatico con autograd; softmax con temperatura e cross-entropy sui quattro logit di esempio | Listati della sottosezione "PyTorch: tensori con il gradiente incorporato" (assemblati: il secondo listato prosegue la stessa sessione) |

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
