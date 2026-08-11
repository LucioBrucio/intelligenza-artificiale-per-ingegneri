#!/bin/sh
# Comandi mostrati nel capitolo 7, sezione "Prova pratica: un modello
# sul proprio computer". Richiedono Ollama installato (https://ollama.com).

# scarica il modello (circa 2 GB, quantizzato int4)
ollama pull llama3.2

# avvia una chat interattiva nel terminale
ollama run llama3.2
