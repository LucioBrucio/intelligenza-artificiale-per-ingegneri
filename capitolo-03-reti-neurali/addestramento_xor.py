"""Ciclo di addestramento completo della rete 2-3-1 sulla funzione XOR.

La rete densa 2-3-1 del capitolo 3, costruita con i moduli di PyTorch,
viene addestrata sui quattro casi della funzione XOR: il problema
non linearmente separabile che il percettrone singolo non puo' risolvere.
"""

import torch
from torch import nn

# dataset giocattolo: i quattro casi della funzione XOR
X = torch.tensor([[0., 0.], [0., 1.], [1., 0.], [1., 1.]])
T = torch.tensor([[0.], [1.], [1.], [0.]])

torch.manual_seed(0)   # inizializzazione ripetibile

# la stessa architettura 2-3-1 dell'esempio a mano
modello = nn.Sequential(
    nn.Linear(2, 3),   # strato nascosto: W e b
    nn.Sigmoid(),
    nn.Linear(3, 1),   # strato di uscita: v e c
    nn.Sigmoid()
)

perdita = nn.BCELoss()   # cross-entropy binaria
ottimizzatore = torch.optim.SGD(modello.parameters(), lr=1.0)

for epoca in range(10001):
    y = modello(X)               # 1. forward pass sui 4 esempi
    L = perdita(y, T)            # 2. calcolo della perdita media
    ottimizzatore.zero_grad()    # 3. azzera i gradienti precedenti
    L.backward()                 # 4. backpropagation
    ottimizzatore.step()         # 5. aggiornamento dei parametri
    if epoca % 2000 == 0:
        print(f"epoca {epoca:5d}   perdita {L.item():.4f}")

# risposte della rete addestrata
print(modello(X).detach().numpy().round(3))
