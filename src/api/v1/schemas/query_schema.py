from pydantic import BaseModel, Field
from typing import Optional, Literal ,Dict


class QueryRequest(BaseModel):
    query: str = Field(
        ...,
        description="User compliance question",
        min_length=3
    )

    regulation_type: Optional[
        Literal["RBI", "SEBI", "Basel", "Internal"]
    ] = Field(
        default=None,
        description="Filter by regulation type"
    )


class Citation(BaseModel):
    content: str
    metadata: Dict


class QueryResponse(BaseModel):
    query: str
    answer:str
    raw_output:dict
    
