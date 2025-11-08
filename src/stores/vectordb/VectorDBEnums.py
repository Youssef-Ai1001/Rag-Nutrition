from enum import Enum


class VectorDBEnums(Enum):
    QDRANT = "QDRANT"
    # PINECONE = "Pinecone"
    # WEAVIATE = "Weaviate"
    # FAISS = "FAISS"
    # CHROMA = "Chroma"
    # VERTEX_AI = "Vertex AI"
    # MILVUS = "Milvus"
    # LANCEDB = "LanceDB"


class DistanceMethodEnums(Enum):
    COSINE = "cosine"
    DOT = "dot"
