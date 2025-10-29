from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
from bson.objectid import ObjectId

class Project(BaseModel):
    
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True
    )    
    
    id : Optional[ObjectId] = Field(default=None, alias="_id")
    project_id : str = Field(...,min_length=1)
    
    @field_validator("project_id")
    def validate_project_id(cls,value):
        if not value.isalnum():
            raise ValueError("project_id must be alphanumeric")
        return value

    @classmethod
    def get_indexes(cls):
        return [
            {
               "key":[
                   ("project_id", 1)
               ],
               "name": "project_id_index_1",
               "unique": True
            }
        ]