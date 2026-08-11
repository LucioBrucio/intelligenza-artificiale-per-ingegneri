"""Scaled dot-product attention da zero in PyTorch.

Replica, cifra per cifra, l'esempio numerico del capitolo 5 sulla frase
"il gatto dorme": proiezioni query/chiave/valore, punteggi, softmax,
media pesata e variante causale.
"""

import math

import torch

# --- Listato 5.1: gli embedding della frase e le proiezioni Q, K, V ---

# embedding della frase "il gatto dorme", un token per riga
X = torch.tensor([[1.,  0.],
                  [0.,  1.],
                  [1., -1.]])

# le tre matrici di proiezione dell'esempio a mano
W_Q = torch.tensor([[1., 0.], [1., 1.]])
W_K = torch.tensor([[0., 1.], [1., 1.]])
W_V = torch.tensor([[1., 1.], [1., 0.]])

Q = X @ W_Q.T    # riga i = W_Q x_i
K = X @ W_K.T
V = X @ W_V.T
print(Q, K, V, sep="\n")

# --- Listato 5.2: la scaled dot-product attention in quattro righe ---

d_k = Q.shape[-1]                 # dimensione delle chiavi: 2
S = Q @ K.T / math.sqrt(d_k)      # punteggi riscalati, 3x3
A = torch.softmax(S, dim=-1)      # una distribuzione per riga
Z = A @ V                         # medie pesate dei valori
print(A)
print(Z)

# --- Listato 5.3: la funzione completa, con maschera causale opzionale ---


def attention(Q, K, V, causale=False):
    """Scaled dot-product attention; se causale=True
    ogni token vede solo se stesso e i precedenti."""
    d_k = Q.shape[-1]
    S = Q @ K.transpose(-2, -1) / math.sqrt(d_k)
    if causale:
        n = S.shape[-1]
        # True sopra la diagonale: le posizioni future
        futuro = torch.triu(torch.ones(n, n, dtype=torch.bool),
                            diagonal=1)
        S = S.masked_fill(futuro, float("-inf"))
    A = torch.softmax(S, dim=-1)
    return A @ V, A


# --- Listato 5.4: verifica dell'attention causale sull'esempio a mano ---

Z_c, A_c = attention(Q, K, V, causale=True)
print(A_c)
print(Z_c)
