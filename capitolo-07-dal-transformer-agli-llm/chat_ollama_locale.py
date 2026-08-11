"""Dialoga da Python con un modello locale servito da Ollama.

Listato del capitolo 7, sezione "Prova pratica: un modello sul proprio
computer". Richiede Ollama in esecuzione (il server locale ascolta sulla
porta 11434) e il modello scaricato con: ollama pull llama3.2
"""

import sys

import requests


def main():
    # il server locale di Ollama ascolta sulla porta 11434
    try:
        risposta = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "llama3.2",
                "messages": [
                    {"role": "system",
                     "content": "Sei un assistente tecnico conciso."},
                    {"role": "user",
                     "content": "Spiega in due frasi cos'e' la quantizzazione."}
                ],
                "stream": False
            }
        )
    except requests.exceptions.ConnectionError:
        print("Impossibile raggiungere Ollama su http://localhost:11434.")
        print("Installa Ollama da https://ollama.com, poi esegui:")
        print("  ollama pull llama3.2")
        print("e assicurati che il server sia attivo (ollama serve).")
        sys.exit(1)

    print(risposta.json()["message"]["content"])


if __name__ == "__main__":
    main()
