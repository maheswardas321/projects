from pydantic import BaseModel

class StoryRequest(BaseModel):
    first_line: str
    genre: str
    creativity: float