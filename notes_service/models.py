from pydantic import BaseModel


class NoteCreate(BaseModel):
    title: str 
    description: str 
    color: str 
    user_id: str

class NoteUpdate(BaseModel):
    title: str 
    description: str 
    color: str 