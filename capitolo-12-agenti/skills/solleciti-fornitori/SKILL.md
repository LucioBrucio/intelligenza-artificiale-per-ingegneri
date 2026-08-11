---
name: solleciti-fornitori
description: Procedura per preparare i solleciti ai
  fornitori con ordini bloccati. Usala quando viene
  chiesto di sollecitare ordini fermi o in ritardo.
---

# Procedura

1. Cerca gli ordini con cerca_ordini(stato="bloccato",
   giorni_min=7): sotto i 7 giorni non si sollecita.
2. Per ogni ordine recupera i contatti con fornitore().
   Se manca l'email non inventare recapiti: segnala
   il caso a un operatore nel riepilogo finale.
3. Prepara ogni bozza con prepara_sollecito() partendo
   da template_sollecito.md, in questa cartella. Oltre
   i 30 giorni di blocco cita il riferimento
   contrattuale e chiedi una data di sblocco precisa.
4. Chiudi con il riepilogo: bozze create, con id, e
   casi che richiedono un operatore.
