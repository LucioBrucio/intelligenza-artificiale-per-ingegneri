# Sezione "Similarità coseno in pratica": verifica in codice del conto a mano.
import numpy as np

def similarita_coseno(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

gatto = np.array([0.8, 0.6, 0.1, 0.1])
cane  = np.array([0.7, 0.7, 0.2, 0.1])
auto  = np.array([0.1, 0.2, 0.9, 0.7])

print(similarita_coseno(gatto, cane))   # 0.9853...
print(similarita_coseno(gatto, auto))   # 0.3067...
print(similarita_coseno(cane, auto))    # 0.3900...
