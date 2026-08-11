"""L'adattatore per il modello vero: l'unico pezzo che tocca
google-genai. Il ciclo, la memoria, il budget e il registro
sono quelli di agente_da_zero.py e restano intatti.

Capitolo 12, sezione "Codice: un agente da zero".
"""

import os
import sys

from google import genai
from google.genai import types

from agente_da_zero import Budget, Risposta, esegui_agente, registro

if not (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")):
    print("Manca la variabile d'ambiente GEMINI_API_KEY: crea una chiave "
          "gratuita su https://aistudio.google.com/apikey e poi esegui "
          "export GEMINI_API_KEY=<la-tua-chiave>")
    sys.exit(1)

MODELLO = "gemini-2.5-flash"   # i nomi dei modelli evolvono

SISTEMA = ("Sei l'assistente dell'ufficio acquisti. Usa gli "
           "strumenti per accertare i fatti: mai rispondere "
           "a memoria. Prepara solo bozze: l'invio spetta "
           "a un operatore.")


class ModelloGemini:
    """Adattatore tra il formato neutro e google-genai."""
    def __init__(self, client, modello=MODELLO):
        self._client, self._modello = client, modello

    def genera(self, messaggi, dichiarazioni):
        config = types.GenerateContentConfig(
            system_instruction=SISTEMA,
            tools=[types.Tool(function_declarations=[
                types.FunctionDeclaration(**d)
                for d in dichiarazioni])],
            temperature=0.0)
        r = self._client.models.generate_content(
            model=self._modello,
            contents=self._converti(messaggi),
            config=config)
        chiamate = [(c.name, dict(c.args))
                    for c in (r.function_calls or [])]
        return Risposta(None if chiamate else r.text,
                        chiamate)

    def _converti(self, messaggi):
        contents = []
        for m in messaggi:
            if m["ruolo"] == "utente":
                contents.append(types.Content(role="user",
                    parts=[types.Part.from_text(
                        text=m["testo"])]))
            elif m["ruolo"] == "assistente":
                parti = ([types.Part.from_text(
                             text=m["testo"])]
                         if m.get("testo") else [])
                parti += [types.Part.from_function_call(
                              name=n, args=a)
                          for n, a in m.get("chiamate", [])]
                contents.append(types.Content(role="model",
                                              parts=parti))
            else:   # esito di uno strumento
                contents.append(types.Content(role="user",
                    parts=[types.Part.from_function_response(
                        name=m["nome"],
                        response=m["esito"])]))
        return contents


if __name__ == "__main__":
    client = genai.Client()   # o Vertex AI, come nel capitolo 8
    print(esegui_agente(
        "Trova gli ordini bloccati da piu' di 7 giorni "
        "e prepara i solleciti ai fornitori.",
        ModelloGemini(client), registro, Budget(),
        conferma=lambda nome, argomenti:
            input(f"eseguo {nome}({argomenti})? [s/n] ") == "s"))
