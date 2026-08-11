"""Esempi NumPy del capitolo 2 (Fondamenti matematici).

Replica in codice i conti svolti a mano nel capitolo: similarita coseno,
prodotto matrice per vettore, broadcasting e discesa del gradiente.
I tre listati della sezione "Gli strumenti: NumPy e PyTorch" formano
un'unica sessione e sono assemblati qui nell'ordine del libro.
"""

import numpy as np

# ------------------------------------------------------------------
# Listato 1: tensori, array e operazioni vettorializzate
# ------------------------------------------------------------------

# I tre documenti dell'esempio svolto a mano:
# conteggi delle parole (antenna, transistor, ricetta)
d1 = np.array([3.0, 2.0, 0.0])
d2 = np.array([2.0, 3.0, 0.0])
d3 = np.array([0.0, 0.0, 4.0])

print(np.dot(d1, d2))        # 12.0
print(np.linalg.norm(d1))    # 3.605551... = radice di 13

def similarita_coseno(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

print(similarita_coseno(d1, d2))      # 0.9230769...
print(similarita_coseno(d1, d3))      # 0.0
print(similarita_coseno(2 * d1, d2))  # 0.9230769...: scala irrilevante

# ------------------------------------------------------------------
# Listato 2: broadcasting
# ------------------------------------------------------------------

# Prodotto matrice per vettore dell'esempio svolto a mano
W = np.array([[ 1.0, 0.0, 2.0],
              [-1.0, 3.0, 1.0]])
x = np.array([2.0, 1.0, 0.5])
print(W @ x)          # [3.  1.5]: un prodotto scalare per riga

# Broadcasting: centrare le colonne di una matrice
X = np.array([[1.0, 2.0],
              [3.0, 4.0],
              [5.0, 6.0]])
m = X.mean(axis=0)    # media di ogni colonna: [3. 4.]
print(X - m)          # la riga m viene sottratta a ogni riga di X

# ------------------------------------------------------------------
# Listato 3: la discesa del gradiente in codice
# ------------------------------------------------------------------

def gradiente(p):
    x, y = p
    return np.array([2 * x, 8 * y])  # gradiente di x^2 + 4y^2

p = np.array([4.0, 2.0])             # punto di partenza
eta = 0.1                            # learning rate
for k in range(3):
    p = p - eta * gradiente(p)       # regola di aggiornamento
    f = p[0]**2 + 4 * p[1]**2
    print(k + 1, p, round(f, 6))

# 1 [3.2 0.4] 10.88
# 2 [2.56 0.08] 6.5792
# 3 [2.048 0.016] 4.195328
