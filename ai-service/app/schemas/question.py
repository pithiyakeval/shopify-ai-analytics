from pydantic import BaseModel

class QuestionRequest(BaseModel):
    store_id:str
    question:str
    