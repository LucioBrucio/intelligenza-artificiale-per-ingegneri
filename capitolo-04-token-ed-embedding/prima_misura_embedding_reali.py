# Listato 4.2 (lst:cap03_prima_misura): prima misura su embedding reali.
# pip install sentence-transformers
from sentence_transformers import SentenceTransformer, util

modello = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2")

vettori = modello.encode(["gatto", "cane", "automobile"])
print(vettori.shape)   # (3, 384): tre vettori a 384 componenti

print(util.cos_sim(vettori, vettori))
