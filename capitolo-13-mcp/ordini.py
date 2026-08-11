# ordini.py: accesso al database ordini di ACME.
# Nessuna dipendenza da MCP: e' Python normale, testabile.
import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS ordini (
    numero        TEXT PRIMARY KEY,
    cliente       TEXT NOT NULL,
    stato         TEXT NOT NULL,   -- ricevuto|spedito|consegnato
    totale        REAL NOT NULL,
    aggiornato_il TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS reclami (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_ordine TEXT NOT NULL,
    motivo        TEXT NOT NULL);
"""

def apri_connessione(percorso="ordini.db"):
    conn = sqlite3.connect(percorso)
    conn.row_factory = sqlite3.Row   # righe leggibili per nome
    conn.executescript(SCHEMA)
    return conn

def stato_ordine(conn, numero):
    """Dati di un ordine, o None se il numero non esiste."""
    riga = conn.execute(
        "SELECT numero, cliente, stato, totale, aggiornato_il "
        "FROM ordini WHERE numero = ?", (numero,)).fetchone()
    return dict(riga) if riga else None

def ordini_di(conn, cliente, limite=10):
    """Gli ordini piu' recenti di un cliente (ricerca parziale)."""
    righe = conn.execute(
        "SELECT numero, stato, totale FROM ordini "
        "WHERE cliente LIKE ? ORDER BY aggiornato_il DESC "
        "LIMIT ?", (f"%{cliente}%", limite)).fetchall()
    return [dict(r) for r in righe]

def apri_reclamo(conn, numero_ordine, motivo):
    """Registra un reclamo; restituisce l'id assegnato."""
    cur = conn.execute(
        "INSERT INTO reclami (numero_ordine, motivo) "
        "VALUES (?, ?)", (numero_ordine, motivo))
    conn.commit()
    return cur.lastrowid
