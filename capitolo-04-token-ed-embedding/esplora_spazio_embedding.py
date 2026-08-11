# Progetto di chiusura del capitolo 4: esplorare uno spazio di embedding.
# Assembla i listati 4.3-4.6 (lst:cap03_parole, lst:cap03_vicini,
# lst:cap03_frasi, lst:cap03_ricerca, lst:cap03_pca) nell'ordine del libro.

# --- Listato 4.3: dodici parole, tre campi semantici ---
from sentence_transformers import SentenceTransformer
import numpy as np

modello = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2")

parole = ["gatto", "cane", "cavallo", "pappagallo",
          "automobile", "camion", "bicicletta", "treno",
          "pane", "formaggio", "pasta", "vino"]

# normalize_embeddings=True: vettori riportati a norma 1
V = modello.encode(parole, normalize_embeddings=True)
print(V.shape)   # (12, 384)

# --- Listato 4.4: i vicini piu' prossimi di ogni parola ---
S = V @ V.T   # matrice 12 x 12 delle similarita' coseno

for i, parola in enumerate(parole):
    ordine = np.argsort(-S[i])       # indici per similarita' decrescente
    vicini = [f"{parole[j]} {S[i, j]:.2f}"
              for j in ordine[1:4]]  # il primo e' la parola stessa
    print(f"{parola:12s} -> {vicini}")

# --- Listato 4.5: similarita' tra frasi, parafrasi contro intruso ---
frasi = [
    "Il tecnico ha riavviato il server dopo l'aggiornamento.",
    "Dopo l'update, il sistemista ha fatto ripartire la macchina.",
    "La carbonara si prepara con guanciale, uova e pecorino.",
]
F = modello.encode(frasi, normalize_embeddings=True)
print((F @ F.T).round(2))

# --- Listato 4.6: ricerca semantica in miniatura ---
documenti = [
    "Per reimpostare la password accedere al pannello utente.",
    "Il contratto si rinnova automaticamente ogni dodici mesi.",
    "In caso di surriscaldamento il dispositivo si spegne.",
    "La garanzia copre i difetti di fabbricazione per due anni.",
    "L'app si sincronizza con il cloud ogni quindici minuti.",
]
D = modello.encode(documenti, normalize_embeddings=True)

domanda = "Ho dimenticato le credenziali di accesso"
q = modello.encode(domanda, normalize_embeddings=True)

punteggi = D @ q                      # una similarita' per documento
for i in np.argsort(-punteggi):
    print(f"{punteggi[i]:.2f}  {documenti[i]}")

# --- Listato 4.7: proiezione 2D dello spazio con la PCA ---
from sklearn.decomposition import PCA

XY = PCA(n_components=2).fit_transform(V)
for (x, y), parola in zip(XY, parole):
    print(f"{parola:12s} {x:6.2f} {y:6.2f}")
