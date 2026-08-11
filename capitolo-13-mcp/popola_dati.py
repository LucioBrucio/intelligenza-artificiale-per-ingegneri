# popola_dati.py: inserisce i tre ordini di prova citati nel
# capitolo, tra cui ORD-1042 della Rossi Srl in stato "spedito"
# (aggiornato il 2026-08-02, totale 149,00 euro).
import ordini

ORDINI_DI_PROVA = [
    ("ORD-1042", "Rossi Srl", "spedito", 149.00, "2026-08-02"),
    ("ORD-1039", "Bianchi SpA", "consegnato", 89.90, "2026-07-21"),
    ("ORD-1051", "Rossi Srl", "ricevuto", 320.00, "2026-08-05"),
]

def main():
    conn = ordini.apri_connessione()
    try:
        for riga in ORDINI_DI_PROVA:
            conn.execute(
                "INSERT OR REPLACE INTO ordini "
                "(numero, cliente, stato, totale, aggiornato_il) "
                "VALUES (?, ?, ?, ?, ?)", riga)
        conn.commit()
    finally:
        conn.close()
    print(f"Inseriti {len(ORDINI_DI_PROVA)} ordini di prova "
          "in ordini.db.")

if __name__ == "__main__":
    main()
