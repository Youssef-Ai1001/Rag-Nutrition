from enum import Enum


class VectorDBEnums(Enum):
    PINECONE = "Pinecone"
    WEAVIATE = "Weaviate"
    FAISS = "FAISS"
    CHROMA = "Chroma"
    VERTEX_AI = "Vertex AI"
    MILVUS = "Milvus"
    QDRANT = "Qdrant"
    LANCEDB = "LanceDB"


class DistanceMethodEnums(Enum):
    COSINE = "cosine"
    DOT = "dot"
