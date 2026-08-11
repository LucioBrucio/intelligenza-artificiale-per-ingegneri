"""Lo stesso motore su Qdrant, con un filtro sui metadati (listato 10.6).

Usa la modalita' in memoria del client Qdrant: nessun server da
installare. Per un'istanza reale basta sostituire ":memory:" con
l'indirizzo del servizio.

Importa il motore gia' indicizzato di motore_ricerca_semantica.py:
all'import viene caricato il modello di embedding e codificato il
corpus.
"""

from qdrant_client import QdrantClient, models

from motore_ricerca_semantica import motore

client = QdrantClient(":memory:")   # oppure url="http://..."

client.create_collection(
    collection_name="assistenza",
    vectors_config=models.VectorParams(
        size=384, distance=models.Distance.DOT),
)
client.upsert(
    collection_name="assistenza",
    points=[models.PointStruct(
                id=i,
                vector=motore.M[i].tolist(),
                payload={"id_chunk": c["id"], "tema": c["tema"]})
            for i, c in enumerate(motore.chunk)],
)

q = motore.modello.encode("il portatile non si accende",
                          normalize_embeddings=True)
risposta = client.query_points(
    collection_name="assistenza",
    query=q.tolist(),
    query_filter=models.Filter(must=[
        models.FieldCondition(key="tema",
            match=models.MatchValue(value="hardware"))]),
    limit=3,
)
for p in risposta.points:
    print(p.payload["id_chunk"], round(p.score, 2))
