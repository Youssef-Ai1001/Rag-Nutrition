from .nutrition_rag_base import SQLAlchemyBase
from sqlalchemy import Column, INTEGER, DateTime, func, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from sqlalchemy.orm import relationship
from sqlalchemy import Index
from pydantic import BaseModel


class DataChunk(SQLAlchemyBase):

    __tablename__ = "chunks"

    chunk_id = Column(INTEGER, primary_key=True, autoincrement=True)
    chunk_uuid = Column(
        UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False
    )

    chunk_content = Column(String, nullable=False)
    chunk_metadata = Column(JSONB, nullable=True)
    chunk_order = Column(INTEGER, nullable=False)

    chunk_project_id = Column(INTEGER, ForeignKey("projects.id"), nullable=False)
    chunk_asset_id = Column(INTEGER, ForeignKey("assets.asset_id"), nullable=False)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    project = relationship("Project", back_populates="chunks")
    asset = relationship("Asset", back_populates="chunks")

    __table_args__ = (
        Index("idx_chunk_project_id", chunk_project_id),
        Index("idx_chunk_asset_id", chunk_asset_id),
    )


class RetrievedDocument(BaseModel):
    text: str
    score: float
