from qdrant_client import QdrantClient, models
from fastembed.embedding import TextEmbedding
from fastembed.sparse.bm25 import Bm25
from fastembed.late_interaction import LateInteractionTextEmbedding
from config import load_config
import pandas as pd
import tqdm

CONFIG = load_config()
dense_embedding_model = TextEmbedding(CONFIG['qdrant']['dense_embedding'])
sparse_embdding_model = Bm25(CONFIG['qdrant']['sparse_embedding'])
late_interaction_embedding = LateInteractionTextEmbedding(CONFIG['qdrant']['late_interaction_embedding'])


def load_dataset(dataset_path):
    dataset = pd.read_csv(dataset_path)
    return [
        {
            'id': row.Index,
            'title': row.title,
            'text': row.text
        }
        for row in dataset.itertuples(index = True, name = 'Point')
    ]

def batch_creater(data, batch_size):
    for i in range(0, len(data), batch_size):
        yield data[i : i + batch_size]



class QdrantVectorDatabase:
    def __init__(self, dataset_path, batch_size):
        self.dataset = load_dataset(dataset_path)
        self.batch_size = batch_size
    def create_client(self):
        dense_embeddings = list(dense_embedding_model.passage_embed(self.dataset[0]['text']))
        late_interaction_embeddings = list(late_interaction_embedding.passage_embed(self.dataset[0]['text']))
        client = QdrantClient(
            url = CONFIG['qdrant']['url'],
            api_key= CONFIG['qdrant']['api_key']
        )
        vectors_config = {
            'all-MiniLM-L6-v2': models.VectorParams(
                size = len(dense_embeddings[0]),
                distance=models.Distance.COSINE
            ),
            'colbertv2.0': models.VectorParams(
                size= len(late_interaction_embeddings[0][0]),
                distance= models.Distance.COSINE,
                multivector_config= models.MultiVectorConfig(
                    comparator=models.MultiVectorComparator.MAX_SIM
                )
            ),
        }
        sparse_vectors_config = {
            'bm25': models.SparseVectorParams(
                modifier=models.Modifier.IDF
            )
        }
        client.create_collection(
            collection_name = CONFIG['qdrant']['collection_name'],
            vectors_config= vectors_config,
            sparse_vectors_config=sparse_vectors_config
        )
        for batch in tqdm.tqdm(batch_creater(self.dataset, self.batch_size), total= len(self.dataset) // self.batch_size):
            texts = [item['text'] for item in batch]
            titles = [item['title'] for item in batch]
            ids = [str(item['id']) for item in batch]
            dense_embeddings = list(dense_embedding_model.passage_embed(texts))
            bm25_embeddings = list(sparse_embdding_model.passage_embed(texts))
            late_interaction_embeddings = list(late_interaction_embedding.passage_embed(texts))

            client.upload_points(
                collection_name=CONFIG['qdrant']['collection_name'],
                points = [
                    models.PointStruct(
                        id = int(ids[i]),
                        vector = {
                            "all-MiniLM-L6-v2": dense_embeddings[i].tolist(),
                            "bm25": bm25_embeddings[i].as_object(),
                            "colbertv2.0": late_interaction_embeddings[i].tolist(),
                        },
                        payload={
                            'id': ids[i],
                            'title': titles[i],
                            'text': texts[i]
                        }
                    )
                    for i in range(len(ids))
                ],
                batch_size= self.batch_size
            )
        print('Upload data point sucessfully !')
    



