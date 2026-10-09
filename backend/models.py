from pydantic import BaseModel

class IssueCreate(BaseModel):
    title: str
    category: str
    location: str
    description: str
