from qdrant_client import QdrantClient, models
from fastembed.embedding import TextEmbedding
from fastembed.sparse.bm25 import Bm25
from fastembed.late_interaction import LateInteractionTextEmbedding
from config import load_config



CONFIG = load_config()

dense_embedding_model = TextEmbedding(CONFIG['qdrant']['dense_embedding'])
sparse_embedding_model = Bm25(CONFIG['qdrant']['sparse_embedding'])
late_interaction_embedding_model = LateInteractionTextEmbedding(CONFIG['qdrant']['late_interaction_embedding'])



class HybridSearch:
    def __init__(self):
        self.client = QdrantClient(
            url = CONFIG['qdrant']['url'],
            api_key=CONFIG['qdrant']['api_key']
        )
    def query_docs(self, query_text):
        dense_embedding_query = next(dense_embedding_model.query_embed(query_text))
        sparse_embedding_query = next(sparse_embedding_model.query_embed(query_text))
        late_interaction_embedding_query = next(late_interaction_embedding_model.query_embed(query_text))
        prefetch = [
            models.Prefetch(
                query=dense_embedding_query,
                using = 'all-MiniLM-L6-v2',
                limit = 20
            ),
            models.Prefetch(
                query=models.SparseVector(**sparse_embedding_query.as_object()),
                using = 'bm25',
                limit = 20
            ),
            models.Prefetch(
                query = late_interaction_embedding_query,
                using = 'colbertv2.0',
                limit = 20
            )
        ]
        responses = self.client.query_points(
            collection_name=CONFIG['qdrant']['collection_name'],
            prefetch=prefetch,
            query = models.FusionQuery(
                fusion=models.Fusion.RRF
            ),
            with_payload=True,
            limit = 10
        )
        score_threshold = CONFIG['qdrant']['thresh_score']
        docs = ''
        for i, response in enumerate(responses.points):
            if response.score >= score_threshold:
                docs += f'Example{i+1}:\nTitle:{response.payload['title']}\nParagraph: {response.payload['text']}\n'
        return docs