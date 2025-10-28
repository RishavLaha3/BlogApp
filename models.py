from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class BlogPost(BaseModel):
    title: str = Field(..., example="My First Blog Post")
    content: str = Field(..., example="This is the content of the post.")
    author: str = Field(..., example="John Doe")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UpdateBlogPost(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None
