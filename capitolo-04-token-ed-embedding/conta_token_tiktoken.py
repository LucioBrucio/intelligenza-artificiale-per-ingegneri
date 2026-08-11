# Listato 4.1 (lst:cap03_tiktoken): contare e ispezionare i token di una frase.
# pip install tiktoken
import tiktoken

# il tokenizzatore usato dai modelli GPT-4 (~100k voci)
enc = tiktoken.get_encoding("cl100k_base")

frasi = [
    "The engineer measures the output voltage.",
    "L'ingegnere misura la tensione di uscita.",
]
for frase in frasi:
    indici = enc.encode(frase)
    pezzi = [enc.decode([i]) for i in indici]
    print(f"{len(indici):3d} token  {pezzi}")
