# Capitolo 7 - Dal Transformer agli LLM

Codice e materiali dei listati del capitolo 7, dedicato al ciclo di vita di un LLM (pretraining, instruction tuning, allineamento, LoRA, quantizzazione) e alla prova pratica di un modello aperto in locale con Ollama.

## File

| File | Listato / sezione del libro | Descrizione |
|---|---|---|
| `esempio_chat_template.txt` | Sezione "I formati di chat" | Esempio di dialogo serializzato nel chat template con i ruoli `system`, `user`, `assistant` e i token speciali di delimitazione. Non è codice eseguibile: mostra il formato testuale in cui il server converte i messaggi prima di darli al modello. |
| `comandi_ollama.sh` | Sezione "Prova pratica: un modello sul proprio computer" | I due comandi da terminale per scaricare (`ollama pull llama3.2`) e avviare in chat interattiva (`ollama run llama3.2`) un modello locale quantizzato. |
| `chat_ollama_locale.py` | Sezione "Prova pratica: un modello sul proprio computer" | Script Python che dialoga con il modello locale tramite il server HTTP di Ollama sulla porta 11434, usando i ruoli `system` e `user` visti nell'instruction tuning. |

## Come eseguire

Prerequisito comune: [Ollama](https://ollama.com) installato sulla propria macchina (Linux, macOS o Windows). Non servono chiavi API né connessione a servizi cloud: tutto gira in locale.

1. Scaricare il modello e provare la chat da terminale:

   ```bash
   sh comandi_ollama.sh
   ```

   oppure eseguire i due comandi a mano. Il download è di circa 2 GB (modello quantizzato int4 in formato GGUF).

2. Dialogare con il modello da Python (il server di Ollama deve essere attivo):

   ```bash
   pip install requests
   python3 chat_ollama_locale.py
   ```

   Se il server non è raggiungibile, lo script stampa le istruzioni per avviarlo ed esce con codice 1.

## Requisiti

- Python 3.12
- Pacchetto pip: `requests`
- Ollama installato e in esecuzione, con il modello `llama3.2` scaricato (circa 2 GB su disco)
