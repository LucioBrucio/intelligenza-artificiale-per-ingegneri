"""Esempi PyTorch del capitolo 2 (Fondamenti matematici).

Replica in codice gli esempi svolti a mano: gradiente calcolato con
l'autograd, softmax con temperatura e cross-entropy. I due listati
della sezione "PyTorch: tensori con il gradiente incorporato" formano
un'unica sessione e sono assemblati qui nell'ordine del libro.
"""

import torch
import torch.nn.functional as F

# ------------------------------------------------------------------
# Listato 4: autograd, il gradiente calcolato in automatico
# ------------------------------------------------------------------

p = torch.tensor([4.0, 2.0], requires_grad=True)
f = p[0]**2 + 4 * p[1]**2   # f(4, 2) = 32
f.backward()                # gradiente calcolato in automatico
print(p.grad)               # tensor([ 8., 16.])

# ------------------------------------------------------------------
# Listato 5: softmax, temperatura e cross-entropy
# ------------------------------------------------------------------

z = torch.tensor([2.0, 1.0, 0.5, -1.0])   # i quattro logit

p = torch.softmax(z, dim=0)
print(p)  # tensor([0.6095, 0.2242, 0.1360, 0.0303])

# Effetto della temperatura sui logit
print(torch.softmax(z / 0.5, dim=0))  # T=0.5: distribuzione concentrata
print(torch.softmax(z / 2.0, dim=0))  # T=2:   distribuzione appiattita

# Cross-entropy: il token corretto ha indice 1
vero = torch.tensor([1])
print(F.cross_entropy(z.unsqueeze(0), vero))  # tensor(1.4952)
