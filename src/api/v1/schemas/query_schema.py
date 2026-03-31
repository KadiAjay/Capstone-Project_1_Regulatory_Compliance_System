from pydantic import BaseModel, Field
from typing import Optional, Literal ,Dict, List


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

    # include_full_text: Optional[bool] = Field(
    #     default=False,
    #     description="Include full retrieved text in response"
    # )




class Citation(BaseModel):
    content: str
    metadata: Dict




class QueryResponse(BaseModel):
    query: str
    answer: str
    citations: List[Citation]
    rule_summary: str
    confidence_score: float
    disclaimer: str