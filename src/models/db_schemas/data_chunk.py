from pydantic import BaseModel,Field,validator, ConfigDict
from typing import Optional
from bson.objectid import ObjectId

class DataChunk(BaseModel):
    
    model_config = ConfigDict(
            arbitrary_types_allowed=True,
            populate_by_name=True
        )      
    
    id : Optional[ObjectId] = Field(default=None, alias="_id")
    chunk_content:str = Field(..., min_length=1)
    chunk_metadata:dict
    chunk_order:int = Field(...,gt=0)
    chunk_project_id:ObjectId
