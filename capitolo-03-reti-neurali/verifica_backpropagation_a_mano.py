"""Verifica in PyTorch dei calcoli svolti a mano sulla rete 2-3-1.

Costruisce la rete con esattamente i pesi dell'esempio a mano del
capitolo 3, esegue il forward pass e chiede a PyTorch i gradienti,
che coincidono cifra per cifra con quelli della backpropagation su carta.
"""

import torch

# pesi e bias identici all'esempio svolto a mano
W = torch.tensor([[ 0.3, -0.2],
                  [ 0.5,  0.4],
                  [-0.4,  0.6]], requires_grad=True)
b = torch.tensor([ 0.1, -0.3,  0.2], requires_grad=True)
v = torch.tensor([ 0.6, -0.1,  0.8], requires_grad=True)
c = torch.tensor([-0.3], requires_grad=True)

x = torch.tensor([1.0, 0.5])   # ingresso
t = torch.tensor([1.0])        # risposta corretta (target)

h = torch.sigmoid(W @ x + b)   # strato nascosto
y = torch.sigmoid(v @ h + c)   # strato di uscita
L = 0.5 * (y - t)**2           # perdita quadratica

L.backward()                   # backpropagation automatica

print(f"y = {y.item():.4f}   L = {L.item():.4f}")
print(f"dL/dv1  = {v.grad[0].item():.4f}")
print(f"dL/dw11 = {W.grad[0, 0].item():.4f}")
